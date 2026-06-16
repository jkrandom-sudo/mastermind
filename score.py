"""Persistent leaderboard (~/.mastermind_scores.json)."""
import json
from pathlib import Path
from typing import Dict, List

DEFAULT_PATH = Path.home() / ".mastermind_scores.json"
MAX_ENTRIES = 10


def load(path: Path = None) -> List[Dict]:
    if path is None:
        path = DEFAULT_PATH
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return [d for d in data if isinstance(d, dict) and "score" in d]
    except (OSError, json.JSONDecodeError):
        pass
    return []


def save(scores: List[Dict], path: Path = None) -> None:
    if path is None:
        path = DEFAULT_PATH
    try:
        path.write_text(json.dumps(scores, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass


def add_score(scores: List[Dict], entry: Dict) -> List[Dict]:
    out = list(scores) + [entry]
    out.sort(key=lambda e: e.get("score", 0), reverse=True)
    return out[:MAX_ENTRIES]


def compute_score(turns_total: int, turns_used: int, won: bool, bonus: int = 0) -> int:
    if not won:
        return max(0, bonus // 4 - turns_used)
    remaining = max(0, turns_total - turns_used)
    return max(0, remaining * 100 - turns_used + bonus)
