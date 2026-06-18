import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import score as score_mod  # noqa: E402
import settings as settings_mod  # noqa: E402
from i18n import t, STRINGS  # noqa: E402
from sound import Sound  # noqa: E402


class TestSettings(unittest.TestCase):
    def test_load_defaults_when_missing(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.json"
            s = settings_mod.load(p)
            self.assertEqual(s["lang"], "zh")
            self.assertEqual(s["difficulty"], "normal")

    def test_save_and_load_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.json"
            settings_mod.save({"lang": "en", "sound": False, "volume": 3, "difficulty": "hard"}, p)
            s = settings_mod.load(p)
            self.assertEqual(s["lang"], "en")
            self.assertFalse(s["sound"])

    def test_load_resets_invalid_persisted_values(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.json"
            p.write_text(
                '{"lang":"xx","sound":"yes","volume":99,"difficulty":"extreme"}',
                encoding="utf-8",
            )
            self.assertEqual(settings_mod.load(p), settings_mod.DEFAULTS)

    def test_load_rejects_bool_volume(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.json"
            p.write_text('{"volume":true}', encoding="utf-8")
            volume = settings_mod.load(p)["volume"]
            self.assertIs(type(volume), int)
            self.assertEqual(volume, settings_mod.DEFAULTS["volume"])

    def test_difficulty_table_complete(self):
        for k in ("easy", "normal", "hard"):
            self.assertIn(k, settings_mod.DIFFICULTY)

    def test_cycle_difficulty(self):
        self.assertEqual(settings_mod.cycle_difficulty("easy"), "normal")
        self.assertEqual(settings_mod.cycle_difficulty("normal"), "hard")
        self.assertEqual(settings_mod.cycle_difficulty("hard"), "easy")

    def test_cycle_lang_volume(self):
        self.assertEqual(settings_mod.cycle_lang("zh"), "en")
        self.assertEqual(settings_mod.cycle_volume(3), 0)


class TestScore(unittest.TestCase):
    def test_compute_score_win_better_with_fewer_turns(self):
        a = score_mod.compute_score(10, 2, won=True, bonus=0)
        b = score_mod.compute_score(10, 8, won=True, bonus=0)
        self.assertGreater(a, b)

    def test_compute_score_loss_smaller_than_any_win(self):
        win = score_mod.compute_score(10, 10, won=True, bonus=0)
        lose = score_mod.compute_score(10, 10, won=False, bonus=0)
        self.assertGreaterEqual(win, lose)

    def test_compute_score_never_negative(self):
        self.assertGreaterEqual(score_mod.compute_score(0, 100, won=False, bonus=0), 0)

    def test_add_score_truncates(self):
        scores = []
        for i in range(15):
            scores = score_mod.add_score(scores, {"name": f"p{i}", "score": i})
        self.assertEqual(len(scores), score_mod.MAX_ENTRIES)

    def test_save_and_load_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "scores.json"
            data = [{"name": "A", "score": 100, "won": True}]
            score_mod.save(data, p)
            self.assertEqual(score_mod.load(p), data)

    def test_load_corrupt_returns_empty(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bad.json"
            p.write_text("{not json")
            self.assertEqual(score_mod.load(p), [])


class TestI18n(unittest.TestCase):
    def test_basic_lookup(self):
        self.assertIn("退出", t("zh", "menu_quit"))
        self.assertIn("Quit", t("en", "menu_quit"))

    def test_unknown_lang_falls_back(self):
        self.assertEqual(t("xx", "menu_quit"), "Q) Quit")

    def test_unknown_key_returns_key(self):
        self.assertEqual(t("zh", "no_such"), "no_such")

    def test_format_kwargs(self):
        out = t("en", "win_line", n=3, score=99)
        self.assertIn("99", out)

    def test_keys_match(self):
        self.assertEqual(set(STRINGS["zh"].keys()), set(STRINGS["en"].keys()))


class TestSound(unittest.TestCase):
    def test_disabled_silent(self):
        buf = io.StringIO()
        s = Sound(enabled=False, volume=3, output=buf)
        s.win()
        self.assertEqual(buf.getvalue(), "")

    def test_volume_scales(self):
        buf = io.StringIO()
        s = Sound(enabled=True, volume=2, output=buf)
        s.win()  # 4 bells * vol 2 = 8
        self.assertEqual(buf.getvalue().count("\a"), 8)


if __name__ == "__main__":
    unittest.main()
