"""The skill renderer must embed a verbatim copy of the shared layout module.

skills/naiwa/scripts/render_naiwa.py stays a single dependency-free file, so
it cannot import naiwasay. Instead it embeds src/naiwasay/_textlayout.py
between markers; scripts/sync_skill_layout.py refreshes the copy. These
checks fail when the two versions drift apart.
"""

import ast
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "naiwasay" / "_textlayout.py"
TARGET = ROOT / "skills" / "naiwa" / "scripts" / "render_naiwa.py"
SYNC = ROOT / "scripts" / "sync_skill_layout.py"
BEGIN = "# --- shared:naiwasay/_textlayout.py begin ---"
END = "# --- shared:naiwasay/_textlayout.py end ---"


def embedded_block(target_text: str) -> str:
    begin = target_text.index(BEGIN) + len(BEGIN)
    end = target_text.index(END, begin)
    return target_text[begin:end].strip("\n")


class SharedLayoutSyncTests(unittest.TestCase):
    def test_markers_appear_exactly_once_in_order(self):
        text = TARGET.read_text(encoding="utf-8")
        self.assertEqual(text.count(BEGIN), 1)
        self.assertEqual(text.count(END), 1)
        self.assertLess(text.index(BEGIN), text.index(END))

    def test_embedded_block_matches_package_module_byte_for_byte(self):
        source = SOURCE.read_text(encoding="utf-8").rstrip("\n")
        text = TARGET.read_text(encoding="utf-8")
        self.assertEqual(embedded_block(text), source)

    def test_module_has_no_relative_imports_or_future_statements(self):
        # The module is embedded mid-file, so it must not rely on package
        # context or syntax that is only valid at the top of a file.
        tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                self.assertNotEqual(node.module, "__future__")
                self.assertEqual(node.level, 0, "relative import found")
        source_text = SOURCE.read_text(encoding="utf-8")
        self.assertNotIn(BEGIN, source_text)
        self.assertNotIn(END, source_text)

    def test_sync_check_passes_on_synced_tree(self):
        result = subprocess.run(
            [sys.executable, str(SYNC), "--check"],
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("in sync", result.stdout)


if __name__ == "__main__":
    unittest.main()
