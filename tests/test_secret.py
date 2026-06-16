import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from secret import make_secret, parse_guess, COLORS  # noqa: E402


class TestMakeSecret(unittest.TestCase):
    def test_default_length(self):
        s = make_secret(rng=random.Random(0))
        self.assertEqual(len(s), 4)

    def test_custom_length(self):
        s = make_secret(length=6, rng=random.Random(0))
        self.assertEqual(len(s), 6)

    def test_uses_palette(self):
        s = make_secret(length=10, colors=["A", "B"], rng=random.Random(0))
        self.assertTrue(set(s) <= {"A", "B"})

    def test_no_duplicates_unique(self):
        s = make_secret(length=4, colors=["A", "B", "C", "D"], allow_duplicates=False, rng=random.Random(0))
        self.assertEqual(len(set(s)), 4)

    def test_no_duplicates_overflow_raises(self):
        with self.assertRaises(ValueError):
            make_secret(length=5, colors=["A", "B"], allow_duplicates=False)

    def test_zero_length_rejected(self):
        with self.assertRaises(ValueError):
            make_secret(length=0)


class TestParseGuess(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(parse_guess("RGBY", 4), ["R", "G", "B", "Y"])

    def test_lowercase(self):
        self.assertEqual(parse_guess("rgby", 4), ["R", "G", "B", "Y"])

    def test_with_spaces(self):
        self.assertEqual(parse_guess("R G B Y", 4), ["R", "G", "B", "Y"])

    def test_repeats_allowed(self):
        self.assertEqual(parse_guess("RRRR", 4), ["R", "R", "R", "R"])

    def test_wrong_length_returns_none(self):
        self.assertIsNone(parse_guess("RGB", 4))
        self.assertIsNone(parse_guess("RGBYO", 4))

    def test_unknown_letter_rejected(self):
        self.assertIsNone(parse_guess("RGBZ", 4))

    def test_palette_subset(self):
        # color "P" not in restricted palette
        self.assertIsNone(parse_guess("RGBP", 4, colors=["R", "G", "B", "Y"]))

    def test_empty_returns_none(self):
        self.assertIsNone(parse_guess("", 4))


if __name__ == "__main__":
    unittest.main()
