#!/usr/bin/env python3
"""Render Naiwa for a terminal or Markdown, using only the standard library."""

import argparse
from pathlib import Path
import re
import sys
import unicodedata


ASSET = Path(__file__).resolve().parent.parent / "assets" / "naiwa.txt"


def cell_width(text):
    """Count ordinary terminal cells, including CJK and combining marks."""
    return sum(
        0 if unicodedata.category(char) in {"Mn", "Me", "Cf"}
        else 2 if unicodedata.east_asian_width(char) in {"W", "F"}
        else 1
        for char in text
    )


def wrap_lines(text, width):
    if not 2 <= width <= 80:
        raise ValueError("width must be between 2 and 80")
    if any(unicodedata.category(c) == "Cc" and c not in "\n\r\t" for c in text):
        raise ValueError("text must not contain terminal control characters")
    lines = []
    for source in text.expandtabs(4).splitlines():
        line = ""
        current_width = 0
        tokens = re.findall(r"[ ]+|[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*|.", source.strip())
        for token in tokens:
            token_width = cell_width(token)
            if line and current_width + token_width > width and token_width <= width:
                lines.append(line.rstrip())
                line = ""
                current_width = 0
            if not line and token.isspace():
                continue
            for char in token:
                char_width = cell_width(char)
                if line and current_width + char_width > width:
                    lines.append(line.rstrip())
                    line = ""
                    current_width = 0
                line += char
                current_width += char_width
        if line:
            lines.append(line.rstrip())
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
    source.add_argument("--text", help="Short answer or summary for the speech bubble")
    source.add_argument("--stdin", action="store_true", help="Read the message from standard input")
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
