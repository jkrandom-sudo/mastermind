"""Score a guess against a secret — red/black peg + white peg counts."""
from collections import Counter
from typing import List, Sequence, Tuple


def score(secret: Sequence[str], guess: Sequence[str]) -> Tuple[int, int]:
    """
    Return (black, white).
    black = correct colour at correct position (red/black peg).
    white = correct colour at wrong position (without double-counting blacks).
    """
    if len(secret) != len(guess):
        raise ValueError("length mismatch")
    black = sum(1 for a, b in zip(secret, guess) if a == b)
    sec_rest = Counter(a for a, b in zip(secret, guess) if a != b)
    gus_rest = Counter(b for a, b in zip(secret, guess) if a != b)
    white = sum((sec_rest & gus_rest).values())
    return black, white


def is_solved(secret: Sequence[str], guess: Sequence[str]) -> bool:
    return list(secret) == list(guess)
