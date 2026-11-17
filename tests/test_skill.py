"""Check the portable skill renderer against the approved character and outputs."""

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from naiwasay.characters import NAIWA


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "skills" / "naiwa" / "scripts" / "render_naiwa.py"
SPEC = importlib.util.spec_from_file_location("naiwa_skill_renderer", SCRIPT)
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)


class SkillRendererTests(unittest.TestCase):
    def test_approved_character_is_preserved(self):
        expected = NAIWA.strip("\n").splitlines()
        actual = renderer.render("Hello!").splitlines()
        self.assertEqual(actual[-len(expected):], ["    " + line for line in expected])

    def test_chinese_and_english_borders_align(self):
        art = renderer.render("奶家人，我来了！\nHello, Naiwa!")
        rows = [line for line in art.splitlines() if line.startswith("| ")]
        self.assertEqual(len({renderer.cell_width(row) for row in rows}), 1)

    def test_mixed_text_wrap_preserves_content(self):
        message = "Hello奶家人" * 12
        lines = renderer.wrap_lines(message, 12)
        self.assertEqual("".join(lines), message)
        self.assertTrue(all(renderer.cell_width(line) <= 12 for line in lines))

    def test_combining_mark_stays_with_its_letter(self):
        self.assertEqual(renderer.wrap_lines("abe\u0301中", 3), ["abe\u0301", "中"])

    def test_english_wrap_keeps_ordinary_words_together(self):
        message = "A CLI (command-line interface) lets you interact with a computer by typing text commands."
        lines = renderer.wrap_lines(message, 36)
        self.assertEqual(" ".join(lines), message)
        self.assertTrue(any("typing" in line for line in lines))
        self.assertTrue(all(renderer.cell_width(line) <= 36 for line in lines))

    def test_markdown_backticks_do_not_escape_fence(self):
        output = renderer.markdown("Literal ``` and `code`")
        self.assertEqual(output.splitlines()[0], "````text")
        self.assertEqual(output.splitlines()[-1], "````")

    def test_empty_or_control_text_is_rejected(self):
        for message in ["", "\n  \n", "hello\x1b[31m"]:
            with self.subTest(message=message), self.assertRaises(ValueError):
                renderer.render(message)

    def test_renderer_runs_outside_source_without_package(self):
        with tempfile.TemporaryDirectory() as folder:
            result = subprocess.run(
                [sys.executable, "-I", str(SCRIPT), "--stdin"],
                input="奶家人，Hello!", text=True, capture_output=True, cwd=folder, check=True,
            )
        self.assertEqual(result.stdout, renderer.markdown("奶家人，Hello!") + "\n")


if __name__ == "__main__":
    unittest.main()
