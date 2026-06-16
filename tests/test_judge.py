import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from judge import score, is_solved  # noqa: E402


class TestScore(unittest.TestCase):
    def test_perfect_match(self):
        self.assertEqual(score("RGBY", "RGBY"), (4, 0))

    def test_no_match(self):
        self.assertEqual(score("RRRR", "GGGG"), (0, 0))

    def test_all_white(self):
        self.assertEqual(score("RGBY", "YBGR"), (0, 4))

    def test_some_black_some_white(self):
        # secret RGBY vs guess RBGY
        # positions 0,3 are black (R,Y match exactly)
        # positions 1,2 of guess (B,G) match positions 2,1 of secret => 2 white
        self.assertEqual(score("RGBY", "RBGY"), (2, 2))

    def test_duplicate_in_guess_no_double_white(self):
        # secret has one R, guess has two Rs in wrong spots — only 1 white
        self.assertEqual(score("RGGY", "BRRR"), (0, 1))

    def test_duplicate_in_secret(self):
        self.assertEqual(score("RRGG", "RGRG"), (2, 2))

    def test_length_mismatch_raises(self):
        with self.assertRaises(ValueError):
            score("RGB", "RGBY")

    def test_works_with_lists(self):
        self.assertEqual(score(["R", "G"], ["R", "G"]), (2, 0))


class TestIsSolved(unittest.TestCase):
    def test_solved(self):
        self.assertTrue(is_solved("RGBY", "RGBY"))

    def test_not_solved(self):
        self.assertFalse(is_solved("RGBY", "RGYB"))


if __name__ == "__main__":
    unittest.main()
