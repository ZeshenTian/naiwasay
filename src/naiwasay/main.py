"""Cowsay-compatible text bubbles with terminal-width-aware Unicode text.

Adapted from cowsay 6.1 by Vaasudevan Srinivasan, licensed under GPL-3.0:
https://github.com/VaasuDevanS/cowsay-python/blob/main/cowsay/main.py

Display-width and wrapping primitives live in ._textlayout, which is shared
verbatim with skills/naiwa/scripts/render_naiwa.py. Edit that module, then
run scripts/sync_skill_layout.py to refresh the embedded copy.
"""

from __future__ import annotations

import re

from ._textlayout import char_width, display_width, hard_wrap
from .characters import CHARS

__version__ = "0.1.0"

CHARS: dict[str, str] = dict(sorted(CHARS.items()))
char_names: list[str] = list(CHARS)

# Historical names kept for compatibility with cowsay's module layout.
_char_width = char_width
_display_width = display_width
wrap_lines = hard_wrap


class CowsayError(LookupError):
    """Invalid text or an unknown character, matching cowsay's error type."""


NaiwasayError = CowsayError


def generate_bubble(text: str) -> list[str]:
    lines = [line.strip() for line in text.split("\n")]
    lines = wrap_lines([line for line in lines if line])
    text_width = max(display_width(line) for line in lines)

    output = ["  " + "_" * text_width]
    if len(lines) > 1:
        output.append(" /" + " " * text_width + "\\")
    for line in lines:
        output.append(
            "| " + line + " " * (text_width - display_width(line) + 1) + "|"
        )
    if len(lines) > 1:
        output.append(" \\" + " " * text_width + "/")
    output.append("  " + "=" * text_width)
    return output


def generate_char(char_lines: str, text_width: int) -> list[str]:
    """Keep artwork unchanged apart from cowsay's bubble-relative indent."""
    return [
        " " * text_width + line
        for line in char_lines.split("\n")
        if line != ""
    ]


def draw(text: str, char_lines: str, to_console: bool = True) -> None | str:
    """Print a bubble and artwork, or return them when to_console is False."""
    if len(re.sub(r"\s", "", text)) == 0:
        raise CowsayError("Pass something meaningful to naiwasay")

    output = generate_bubble(text)
    text_width = max(display_width(line) for line in output) - 4
    output += generate_char(char_lines, text_width)
    if to_console:
        for line in output:
            print(line)
        return None
    return "\n".join(output)


def get_output_string(char: str, text: str) -> str:
    """Return a named character speaking text, without a trailing newline."""
    if char not in CHARS:
        raise CowsayError(f"Available Characters: {char_names}")
    return draw(text, CHARS[char], to_console=False)
