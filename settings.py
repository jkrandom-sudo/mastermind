"""Persistent settings (~/.mastermind_settings.json)."""
import json
from pathlib import Path
from typing import Any, Dict

DEFAULT_PATH = Path.home() / ".mastermind_settings.json"

DEFAULTS: Dict[str, Any] = {
    "lang": "zh",
    "sound": True,
    "volume": 1,
    "difficulty": "normal",   # easy / normal / hard
}

# Difficulty profile: (length, palette_size, turns, score_bonus)
DIFFICULTY = {
    "easy":   {"length": 4, "palette": 4, "turns": 12, "bonus": 0},
    "normal": {"length": 4, "palette": 6, "turns": 10, "bonus": 100},
    "hard":   {"length": 5, "palette": 6, "turns": 10, "bonus": 250},
}


def load(path: Path = None) -> Dict[str, Any]:
    if path is None:
        path = DEFAULT_PATH
    s = dict(DEFAULTS)
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                for k in DEFAULTS:
                    if k in data:
                        s[k] = data[k]
        except (OSError, json.JSONDecodeError):
            pass
    return s


def save(settings: Dict[str, Any], path: Path = None) -> None:
    if path is None:
        path = DEFAULT_PATH
    try:
        path.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass


def cycle_lang(lang: str) -> str:
    return "en" if lang == "zh" else "zh"


def cycle_volume(v: int) -> int:
    return (v + 1) % 4


def cycle_difficulty(d: str) -> str:
    order = ["easy", "normal", "hard"]
    try:
        i = order.index(d)
    except ValueError:
        i = 0
    return order[(i + 1) % len(order)]
