#!/usr/bin/env python3
"""Sync src/naiwasay/_textlayout.py into the portable skill renderer.

The skill script must remain a single dependency-free file, so it embeds a
verbatim copy of the shared layout module between markers. Edit the module
under src/naiwasay/, then run this script and commit both files. Pass
--check to verify without writing; the test suite runs the same comparison.
"""

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "naiwasay" / "_textlayout.py"
TARGET = ROOT / "skills" / "naiwa" / "scripts" / "render_naiwa.py"
BEGIN = "# --- shared:naiwasay/_textlayout.py begin ---"
END = "# --- shared:naiwasay/_textlayout.py end ---"


def splice(source_text: str, target_text: str) -> str:
    """Return target_text with the marked region replaced by source_text.

    Raises ValueError when either marker is missing from the target.
    """
    begin = target_text.index(BEGIN) + len(BEGIN)
    end = target_text.index(END, begin)
    return (
        target_text[:begin]
        + "\n" + source_text.rstrip("\n") + "\n"
        + target_text[end:]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true",
        help="exit non-zero when the embedded copy differs; do not write",
    )
    args = parser.parse_args()

    try:
        source_text = SOURCE.read_text(encoding="utf-8")
        target_text = TARGET.read_text(encoding="utf-8")
        updated = splice(source_text, target_text)
    except (OSError, ValueError) as error:
        print(f"cannot sync: {error}", file=sys.stderr)
        return 2

    if updated == target_text:
        print("shared layout module is in sync")
        return 0
    if args.check:
        print(
            "shared layout module is out of sync; "
            "run scripts/sync_skill_layout.py",
            file=sys.stderr,
        )
        return 1
    TARGET.write_text(updated, encoding="utf-8")
    print(f"updated {TARGET.relative_to(ROOT)} from {SOURCE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
