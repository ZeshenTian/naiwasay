"""Let Naiwa say something, using the familiar Python cowsay interface."""

from .main import CHARS, CowsayError, __version__, char_names, draw, get_output_string


def naiwa(text, char_lines=CHARS["naiwa"]):
    """Print Naiwa saying ``str(text)``; return None, just like cowsay.cow."""
    draw(str(text), char_lines)


char_funcs = {"naiwa": naiwa}

__all__ = [
    "naiwa", "draw", "get_output_string", "char_names", "char_funcs",
    "CHARS", "CowsayError", "__version__",
]

