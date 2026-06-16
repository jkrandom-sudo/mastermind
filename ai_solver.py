"""AI codebreaker — simple deductive solver using candidate elimination."""
from itertools import product
from typing import List, Optional, Sequence, Tuple

from judge import score


class AISolver:
    """Eliminate candidates that would not produce the same score as observed."""

    def __init__(self, length: int, colors: Sequence[str], rng=None):
        import random
        self.length = length
        self.colors = list(colors)
        self.rng = rng or random.Random()
        self._candidates = [list(p) for p in product(self.colors, repeat=length)]
        self._history: List[Tuple[List[str], int, int]] = []

    def make_guess(self) -> List[str]:
        if not self._candidates:
            return []
        if not self._history:
            # first guess: fixed pattern for consistency (half R half G)
            half = self.length // 2
            return [self.colors[0]] * half + [self.colors[1] if self.colors[1:] else self.colors[0]] * (self.length - half)
        return list(self._candidates[0])

    def feedback(self, guess: List[str], black: int, white: int) -> None:
        self._history.append((guess, black, white))
        self._candidates = [
            c for c in self._candidates
            if score(c, guess) == (black, white)
        ]
        # Shuffle to avoid bias — but keep deterministic with rng
        if self.rng and len(self._candidates) > 1:
            self.rng.shuffle(self._candidates)

    @property
    def remaining(self) -> int:
        return len(self._candidates)

    @property
    def solved(self) -> bool:
        return len(self._history) > 0 and self._history[-1][1] == self.length