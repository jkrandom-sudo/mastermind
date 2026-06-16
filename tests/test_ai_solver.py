import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ai_solver import AISolver  # noqa: E402
from judge import score  # noqa: E402


class TestAISolver(unittest.TestCase):
    def test_first_guess_consistent(self):
        s = AISolver(length=4, colors=["R", "G", "B", "Y"], rng=random.Random(0))
        g = s.make_guess()
        self.assertEqual(len(g), 4)

    def test_remaining_decreases(self):
        s = AISolver(length=4, colors=["R", "G", "B", "Y"], rng=random.Random(0))
        before = s.remaining
        g = s.make_guess()
        s.feedback(g, 0, 0)  # zero info → still cuts a lot
        self.assertLess(s.remaining, before)

    def test_solver_solves_within_limit(self):
        """Brute test — solver must crack any 4x6 code in <= 10 turns."""
        secret = list("RGBO")
        s = AISolver(length=4, colors=["R", "G", "B", "Y", "O", "P"], rng=random.Random(7))
        for n in range(1, 12):
            g = s.make_guess()
            self.assertNotEqual(g, [], f"empty guess at turn {n}")
            b, w = score(secret, g)
            if b == 4:
                self.assertLessEqual(n, 10)
                return
            s.feedback(g, b, w)
        self.fail("solver did not converge")

    def test_solver_handles_all_correct(self):
        s = AISolver(length=3, colors=["R", "G", "B"], rng=random.Random(0))
        # Force the solver's first guess
        g = s.make_guess()
        s.feedback(g, 3, 0)
        self.assertTrue(s.solved)

    def test_inconsistent_feedback_empties_candidates(self):
        s = AISolver(length=3, colors=["R", "G"], rng=random.Random(0))
        g = s.make_guess()
        s.feedback(g, 99, 99)  # impossible
        self.assertEqual(s.remaining, 0)
        self.assertEqual(s.make_guess(), [])


if __name__ == "__main__":
    unittest.main()
