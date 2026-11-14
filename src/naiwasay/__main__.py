"""Command-line entry point, following cowsay 6.1's command interface.

Adapted from VaasuDevanS/cowsay-python (GPL-3.0); see NOTICE.
"""

import argparse

from . import CowsayError, __version__, char_funcs, char_names


def cli():
    """Print a text bubble and Naiwa; accept the same flags as cowsay."""
    parser = argparse.ArgumentParser(
        prog="naiwasay",
        description=(
            "CLI tool to display text in ASCII art. "
            "Available Characters: {}".format(char_names)
        ),
    )
    parser.add_argument("-c", "--character", default="naiwa")
    parser.add_argument("-t", "--text", required=True)
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args()

    if args.character not in char_names:
        raise CowsayError("Available Characters: {}".format(char_names))
    char_funcs[args.character](args.text)


if __name__ == "__main__":
    cli()

