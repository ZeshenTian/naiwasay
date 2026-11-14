"""Cowsay-compatible text bubbles with terminal-width-aware Unicode text.

Adapted from cowsay 6.1 by Vaasudevan Srinivasan, licensed under GPL-3.0:
https://github.com/VaasuDevanS/cowsay-python/blob/main/cowsay/main.py
"""

from __future__ import annotations

import re
import unicodedata

from .characters import CHARS

__version__ = "0.1.0"

CHARS: dict[str, str] = dict(sorted(CHARS.items()))
char_names: list[str] = list(CHARS)


class CowsayError(LookupError):
    """Invalid text or an unknown character, matching cowsay's error type."""


NaiwasayError = CowsayError


def _char_width(char: str) -> int:
    """Return terminal columns for ordinary text, CJK, and combining marks.

    Ambiguous-width characters use one column, as in most Western terminals.
    Emoji sequences can vary by terminal and are not a grapheme-width engine.
    """
    if unicodedata.combining(char) or unicodedata.category(char) in {
        "Mn", "Me", "Cf"
    }:
        return 0
    return 2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1


def _display_width(text: str) -> int:
    return sum(_char_width(char) for char in text)


def wrap_lines(lines: list[str], max_width: int = 49) -> list[str]:
    """Hard-wrap at terminal columns without separating combining marks."""
    if max_width <= 0:
        raise ValueError("max_width must be greater than zero")

    wrapped = []
    for line in lines:
        chunk: list[str] = []
        columns = 0
        for char in line:
            char_width = _char_width(char)
            if chunk and columns + char_width > max_width:
                wrapped.append("".join(chunk))
                chunk = []
                columns = 0
            chunk.append(char)
            columns += char_width
        if chunk:
            wrapped.append("".join(chunk))
    return wrapped


def generate_bubble(text: str) -> list[str]:
    lines = [line.strip() for line in text.split("\n")]
    lines = wrap_lines([line for line in lines if line])
    text_width = max(_display_width(line) for line in lines)

    output = ["  " + "_" * text_width]
    if len(lines) > 1:
        output.append(" /" + " " * text_width + "\\")
    for line in lines:
        output.append(
            "| " + line + " " * (text_width - _display_width(line) + 1) + "|"
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
    text_width = max(_display_width(line) for line in output) - 4
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
