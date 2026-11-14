"""Public command-line contract, exercised in a separate Python process."""

import os
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CommandLineTests(unittest.TestCase):
    def run_cli(self, *args):
        env = os.environ.copy()
        existing = env.get("PYTHONPATH")
        env["PYTHONPATH"] = str(ROOT / "src") + (
            os.pathsep + existing if existing else ""
        )
        env["PYTHONIOENCODING"] = "utf-8"
        return subprocess.run(
            [sys.executable, "-m", "naiwasay", *args],
            env=env,
            cwd=str(ROOT),
            capture_output=True,
            encoding="utf-8",
            timeout=10,
        )

    def test_default_character_and_english_bubble(self):
        result = self.run_cli("-t", "Hello World")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertTrue(result.stdout.startswith(
            "  ___________\n| Hello World |\n  ===========\n"
        ))
        self.assertGreater(len(result.stdout.splitlines()), 35)
        self.assertTrue(result.stdout.endswith("\n"))
        self.assertFalse(result.stdout.endswith("\n\n"))

    def test_explicit_character_and_long_flags_match_defaults(self):
        default = self.run_cli("-t", "Hello")
        explicit = self.run_cli("--text", "Hello", "--character", "naiwa")
        self.assertEqual(explicit.returncode, 0, explicit.stderr)
        self.assertEqual(explicit.stdout, default.stdout)

    def test_chinese_uses_terminal_columns(self):
        result = self.run_cli("-t", "你好，奶蛙！")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.startswith(
            "  ____________\n| 你好，奶蛙！ |\n  ============\n"
        ))

    def test_missing_text_is_an_argument_error(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("--text", result.stderr)

    def test_positional_text_does_not_replace_required_option(self):
        result = self.run_cli("Hello")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")

    def test_unknown_character_fails(self):
        result = self.run_cli("-t", "Hello", "-c", "missing")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("Available Characters", result.stderr)
        self.assertIn("naiwa", result.stderr)

    def test_whitespace_text_fails(self):
        result = self.run_cli("-t", " \n\t ")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("CowsayError", result.stderr)

    def test_version_does_not_require_text(self):
        result = self.run_cli("--version")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"^\d+\.\d+\.\d+\n$")
        self.assertEqual(result.stderr, "")

    def test_help_lists_supported_options(self):
        result = self.run_cli("-h")
        self.assertEqual(result.returncode, 0, result.stderr)
        for flag in ("--text", "--character", "--version", "--help"):
            self.assertIn(flag, result.stdout)
        self.assertIn("naiwa", result.stdout)
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
