#!/usr/bin/env python3
"""Render Naiwa for a terminal or Markdown, using only the standard library."""

import argparse
from pathlib import Path
import re
import sys
import unicodedata

# The region between the shared markers is a verbatim copy of
# src/naiwasay/_textlayout.py, the single source of truth for display-width
# and wrapping logic. Edit that module, then run scripts/sync_skill_layout.py;
# tests/test_layout_sync.py fails when the two copies drift apart.
# --- shared:naiwasay/_textlayout.py begin ---
"""Shared display-width and wrapping primitives, standard library only.

This module is the single source of truth for terminal text layout. The
naiwasay package imports it directly, and the exact same source is embedded
between markers in skills/naiwa/scripts/render_naiwa.py, which must stay a
single dependency-free file. After editing here, run
scripts/sync_skill_layout.py; tests/test_layout_sync.py fails when the two
copies drift apart.

Constraints for this file: no ``from __future__`` imports, no relative
imports, and no marker-comment strings, so it can be embedded verbatim in
the middle of another module and still run under Python 3.9+.

Adapted in part from cowsay 6.1 by Vaasudevan Srinivasan (GPL-3.0); see
NOTICE.
"""

import re
import unicodedata


def char_width(char: str) -> int:
    """Return terminal columns for ordinary text, CJK, and combining marks.

    Ambiguous-width characters use one column, as in most Western terminals.
    Emoji sequences can vary by terminal and are not a grapheme-width engine.
    """
    if unicodedata.combining(char) or unicodedata.category(char) in {
        "Mn", "Me", "Cf"
    }:
        return 0
    return 2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1


def display_width(text: str) -> int:
    """Return the total terminal columns occupied by text."""
    return sum(char_width(char) for char in text)


def hard_wrap(lines: list[str], max_width: int = 49) -> list[str]:
    """Hard-wrap at terminal columns without separating combining marks.

    This is the cowsay-compatible policy: lines break exactly at the width
    limit, even inside words.
    """
    if max_width <= 0:
        raise ValueError("max_width must be greater than zero")

    wrapped = []
    for line in lines:
        chunk: list[str] = []
        columns = 0
        for char in line:
            width = char_width(char)
            if chunk and columns + width > max_width:
                wrapped.append("".join(chunk))
                chunk = []
                columns = 0
            chunk.append(char)
            columns += width
        if chunk:
            wrapped.append("".join(chunk))
    return wrapped


def word_wrap(text: str, width: int) -> list[str]:
    """Wrap prose at word boundaries, preserving paragraphs and indentation.

    Ordinary English words, including hyphenated and apostrophed tokens,
    stay together when they fit. Tokens wider than the limit, CJK runs, and
    code fall back to a character fill that never separates combining
    marks. Blank lines are preserved and tabs expand to four spaces.
    """
    lines = []
    for source in text.expandtabs(4).splitlines():
        line = ""
        current_width = 0
        seen_content = False
        tokens = re.findall(r"[ ]+|[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*|.", source.rstrip())
        for token in tokens:
            token_width = display_width(token)
            if line and current_width + token_width > width and token_width <= width:
                lines.append(line.rstrip())
                line = ""
                current_width = 0
            if not line and token.isspace() and seen_content:
                continue
            for char in token:
                step = char_width(char)
                if line and current_width + step > width:
                    lines.append(line.rstrip())
                    line = ""
                    current_width = 0
                line += char
                current_width += step
            if not token.isspace():
                seen_content = True
        if line or not source.strip():
            lines.append(line.rstrip())
    return lines
# --- shared:naiwasay/_textlayout.py end ---

ASSET = Path(__file__).resolve().parent.parent / "assets" / "naiwa.txt"

cell_width = display_width


def wrap_lines(text, width):
    """Validate skill input policy, then word-wrap with the shared primitive."""
    if not 2 <= width <= 80:
        raise ValueError("width must be between 2 and 80")
    if any(unicodedata.category(c) == "Cc" and c not in "\n\r\t" for c in text):
        raise ValueError("text must not contain terminal control characters")
    if not text.strip():
        raise ValueError("text must not be empty")
    lines = word_wrap(text, width)
    if not lines:
        raise ValueError("text must not be empty")
    return lines


def render(text, width=36):
    lines = wrap_lines(text, width)
    bubble_width = max(cell_width(line) for line in lines)
    rows = ["  " + "_" * bubble_width]
    if len(lines) > 1:
        rows.append(" /" + " " * bubble_width + " " + chr(92))
    rows.extend("| " + line + " " * (bubble_width - cell_width(line)) + " |" for line in lines)
    if len(lines) > 1:
        rows.append(" " + chr(92) + " " * bubble_width + " /")
    rows.append("  " + "=" * bubble_width)
    rows.extend("    " + line for line in ASSET.read_text(encoding="utf-8").splitlines())
    return "\n".join(rows)


def markdown(text, width=36):
    art = render(text, width)
    longest = max((len(match) for match in re.findall(r"`+", art)), default=0)
    fence = "`" * max(3, longest + 1)
    return fence + "text\n" + art + "\n" + fence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Complete reply to display in the speech bubble")
    source.add_argument("--stdin", action="store_true", help="Read the complete reply from standard input")
    parser.add_argument("--width", type=int, default=36, help="Maximum speech-bubble width in cells")
    parser.add_argument(
        "--format", choices=("plain", "markdown"), default="plain",
        help="Output format: plain for terminal stdout (default), markdown for AI chat replies",
    )
    args = parser.parse_args()
    try:
        message = sys.stdin.read() if args.stdin else args.text
        formatter = markdown if args.format == "markdown" else render
        print(formatter(message, args.width))
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
