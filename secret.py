"""Secret code generation."""
import random
from typing import List, Optional, Sequence

# 6 standard pegs
COLORS: List[str] = ["R", "G", "B", "Y", "O", "P"]   # Red Green Blue Yellow Orange Purple


def make_secret(
    length: int = 4,
    colors: Sequence[str] = COLORS,
    allow_duplicates: bool = True,
    rng: Optional[random.Random] = None,
) -> List[str]:
    rng = rng or random.Random()
    if length <= 0:
        raise ValueError("length must be positive")
    if not allow_duplicates:
        if length > len(colors):
            raise ValueError("length exceeds palette without duplicates")
        return rng.sample(list(colors), length)
    return [rng.choice(list(colors)) for _ in range(length)]


def parse_guess(text: str, length: int, colors: Sequence[str] = COLORS) -> Optional[List[str]]:
    """Accept inputs like 'RGBY', 'r g b y', 'rrgg'. Return list or None on failure."""
    if not text:
        return None
    s = "".join(text.upper().split())
    if len(s) != length:
        return None
    palette = set(c.upper() for c in colors)
    if any(ch not in palette for ch in s):
        return None
    return list(s)
