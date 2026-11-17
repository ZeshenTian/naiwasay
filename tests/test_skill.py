"""Check the portable skill renderer against the approved character and outputs."""

import importlib.util
from pathlib import Path
import shutil
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
        self.assertEqual(result.stdout, renderer.render("奶家人，Hello!") + "\n")
        self.assertEqual(result.stderr, "")

    def test_markdown_flag_preserves_literal_backticks_and_chinese(self):
        message = "奶家人，保留 ``` 和 `code`。"
        result = subprocess.run(
            [sys.executable, "-I", str(SCRIPT), "--format", "markdown", "--stdin"],
            input=message, text=True, capture_output=True, check=True, timeout=10,
        )
        self.assertEqual(result.stdout, renderer.markdown(message) + "\n")
        self.assertEqual(result.stderr, "")

    def test_explicit_plain_output_has_no_markdown_or_ansi(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--format", "plain", "--text", "Build 通过！"],
            text=True, capture_output=True, check=True, timeout=10,
        )
        self.assertEqual(result.stdout, renderer.render("Build 通过！") + "\n")
        self.assertNotIn("```", result.stdout)
        self.assertNotIn("\x1b", result.stdout)

    def test_width_flag_wraps_chinese_without_changing_art(self):
        message = "奶家人，Build 通过了！下一步继续。"
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--width", "12", "--stdin"],
            input=message, text=True, capture_output=True, check=True, timeout=10,
        )
        self.assertEqual(result.stdout, renderer.render(message, 12) + "\n")
        rows = [row for row in result.stdout.splitlines() if row.startswith("| ")]
        self.assertTrue(all(renderer.cell_width(row) <= 16 for row in rows))

    def test_copied_skill_runs_from_path_with_spaces_without_package(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / "AI skills" / "naiwa"
            shutil.copytree(
                SCRIPT.parents[1], destination,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            copied_script = destination / "scripts" / SCRIPT.name
            result = subprocess.run(
                [sys.executable, "-I", str(copied_script), "--stdin"],
                input="复制后也能说中文！", text=True, capture_output=True,
                cwd=folder, check=True, timeout=10,
            )
        self.assertEqual(result.stdout, renderer.render("复制后也能说中文！") + "\n")

    def test_stdin_keeps_shell_metacharacters_literal(self):
        with tempfile.TemporaryDirectory() as folder:
            message = "$(touch NAIWA_SHOULD_NOT_EXIST) `echo hello` '奶蛙' \"ok\""
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--stdin"],
                input=message, text=True, capture_output=True,
                cwd=folder, check=True, timeout=10,
            )
            self.assertFalse((Path(folder) / "NAIWA_SHOULD_NOT_EXIST").exists())
        self.assertEqual(result.stdout, renderer.render(message) + "\n")

    def test_invalid_arguments_fail_without_partial_art(self):
        cases = [
            (["--stdin"], ""),
            (["--stdin"], "hello\x1b[31m"),
            (["--text", "Hello", "--width", "1"], None),
            (["--text", "Hello", "--width", "81"], None),
            (["--text", "Hello", "--format", "unknown"], None),
            (["--text", "Hello", "--stdin"], "Hello"),
        ]
        for args, message in cases:
            with self.subTest(args=args, message=message):
                result = subprocess.run(
                    [sys.executable, str(SCRIPT), *args], input=message,
                    text=True, capture_output=True, timeout=10,
                )
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("error:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_missing_asset_reports_actionable_error(self):
        with tempfile.TemporaryDirectory() as folder:
            script = Path(folder) / "scripts" / SCRIPT.name
            script.parent.mkdir()
            shutil.copyfile(SCRIPT, script)
            result = subprocess.run(
                [sys.executable, "-I", str(script), "--text", "Hello"],
                text=True, capture_output=True, timeout=10,
            )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("naiwa.txt", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
