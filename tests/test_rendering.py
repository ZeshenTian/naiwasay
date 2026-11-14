"""Behavioral checks for cowsay compatibility and Unicode terminal alignment."""

import contextlib
import io
import unittest
from unittest.mock import patch

from naiwasay import main


class BubbleRenderingTests(unittest.TestCase):
    def test_single_line_matches_cowsay_61_exactly(self):
        self.assertEqual(
            main.generate_bubble("Hello World"),
            ["  ___________", "| Hello World |", "  ==========="],
        )

    def test_multiple_lines_strip_edges_and_drop_blank_lines(self):
        self.assertEqual(
            main.generate_bubble("  One  \n\n \t\n Two words \n"),
            [
                "  _________",
                " /         \\",
                "| One       |",
                "| Two words |",
                " \\         /",
                "  =========",
            ],
        )

    def test_english_hard_wrap_is_49_characters_even_inside_words(self):
        self.assertEqual(
            main.wrap_lines(["a" * 48 + "word"]),
            ["a" * 48 + "w", "ord"],
        )
        self.assertEqual(main.wrap_lines(["x" * 98]), ["x" * 49] * 2)

    def test_long_english_bubble_preserves_upstream_layout(self):
        self.assertEqual(
            main.generate_bubble("a" * 50),
            [
                "  " + "_" * 49,
                " /" + " " * 49 + "\\",
                "| " + "a" * 49 + " |",
                "| a" + " " * 49 + "|",
                " \\" + " " * 49 + "/",
                "  " + "=" * 49,
            ],
        )

    def test_chinese_uses_two_columns_per_character(self):
        self.assertEqual(
            main.generate_bubble("奶蛙来了"),
            ["  ________", "| 奶蛙来了 |", "  ========"],
        )

    def test_mixed_text_aligns_with_chinese_and_english_lines(self):
        self.assertEqual(
            main.generate_bubble("Hi 奶蛙!\nOK\n你好"),
            [
                "  ________",
                " /        \\",
                "| Hi 奶蛙! |",
                "| OK       |",
                "| 你好     |",
                " \\        /",
                "  ========",
            ],
        )

    def test_chinese_hard_wrap_never_splits_a_wide_character(self):
        self.assertEqual(main.wrap_lines(["蛙" * 25]), ["蛙" * 24, "蛙"])
        self.assertEqual(
            main.wrap_lines(["a" * 48 + "蛙b"]),
            ["a" * 48, "蛙b"],
        )
        self.assertEqual(
            main.wrap_lines(["a" * 47 + "蛙b"]),
            ["a" * 47 + "蛙", "b"],
        )

    def test_combining_mark_uses_no_extra_column(self):
        self.assertEqual(
            main.generate_bubble("cafe\u0301"),
            ["  ____", "| cafe\u0301 |", "  ===="],
        )

    def test_combining_mark_stays_with_letter_at_wrap_boundary(self):
        self.assertEqual(
            main.wrap_lines(["a" * 48 + "e\u0301b"]),
            ["a" * 48 + "e\u0301", "b"],
        )


class DrawingTests(unittest.TestCase):
    def test_custom_art_preserves_spaces_and_removes_only_empty_lines(self):
        art = "\n\\\n \\\n\n  /\"\"\\  \n   \n"
        self.assertEqual(
            main.generate_char(art, 2),
            ["  \\", "   \\", '    /""\\  ', "     "],
        )

    def test_art_indentation_uses_display_width(self):
        self.assertEqual(
            main.draw("奶蛙", "\\\n (o)", to_console=False),
            "  ____\n| 奶蛙 |\n  ====\n    \\\n     (o)",
        )

    def test_console_output_matches_returned_string_plus_final_newline(self):
        art = "\\\n \\\n  (o)"
        expected = main.draw("Hello", art, to_console=False)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            returned = main.draw("Hello", art)
        self.assertIsNone(returned)
        self.assertEqual(output.getvalue(), expected + "\n")
        self.assertFalse(expected.endswith("\n"))

    def test_string_output_does_not_print(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            returned = main.draw("Hello", "\\", to_console=False)
        self.assertIsInstance(returned, str)
        self.assertEqual(output.getvalue(), "")

    def test_named_character_uses_same_drawing_and_has_no_trailing_newline(self):
        art = "\\\n  (o)"
        with patch.dict(main.CHARS, {"test_naiwa": art}):
            result = main.get_output_string("test_naiwa", "Hi")
        self.assertEqual(result, main.draw("Hi", art, to_console=False))
        self.assertFalse(result.endswith("\n"))

    def test_unknown_character_raises_lookup_error(self):
        with self.assertRaisesRegex(main.CowsayError, "Available Characters"):
            main.get_output_string("not_a_character", "Hello")
        self.assertTrue(issubclass(main.CowsayError, LookupError))
        self.assertIs(main.NaiwasayError, main.CowsayError)

    def test_empty_or_whitespace_only_text_raises(self):
        for text in ["", " ", "\n\t\r", "\u3000\n\u00a0"]:
            with self.subTest(text=repr(text)):
                with self.assertRaisesRegex(main.CowsayError, "meaningful"):
                    main.draw(text, "\\", to_console=False)


if __name__ == "__main__":
    unittest.main()
