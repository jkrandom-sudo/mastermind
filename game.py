"""Mastermind — main menu + guess / codemaker modes."""
import random
import sys
from pathlib import Path
from typing import Callable, List, Optional

from ai_solver import AISolver
from judge import score, is_solved
from secret import make_secret, parse_guess, COLORS
from i18n import t, STRINGS
import score as score_mod
import settings as settings_mod
from sound import Sound


class QuitGame(Exception):
    pass


class QuitRound(Exception):
    pass


def input_or_quit(prompt: str, input_func: Callable[[str], str]) -> str:
    try:
        s = input_func(prompt)
    except (EOFError, KeyboardInterrupt):
        raise QuitGame()
    if s.strip().lower() == "q":
        raise QuitRound()
    return s


def write(output, *parts) -> None:
    for p in parts:
        output.write(str(p))
    output.write("\n")
    output.flush()


def show_guess_result(output, guess, black, white, sound: Sound, lang: str):
    line = t(lang, "result_line", guess="".join(guess), black=black, white=white)
    write(output, line)
    sound.guess()
    if black > 0:
        sound.black_peg()
        sound.black_peg()


def play_guess(
    settings: dict,
    sound: Sound,
    input_func: Callable[[str], str],
    output,
    rng: Optional[random.Random] = None,
) -> Optional[dict]:
    rng = rng or random.Random()
    lang = settings["lang"]
    diff = settings_mod.DIFFICULTY[settings["difficulty"]]
    length = diff["length"]
    palette = COLORS[:diff["palette"]]
    turns_max = diff["turns"]
    bonus = diff["bonus"]

    secret_code = make_secret(length=length, colors=palette, allow_duplicates=True, rng=rng)
    secret_str = "".join(secret_code)
    write(output, t(lang, "round_start", length=length, turns=turns_max))

    for n in range(1, turns_max + 1):
        try:
            raw = input_or_quit(t(lang, "your_guess", n=n, total=turns_max), input_func).strip()
        except QuitRound:
            return None
        guess = parse_guess(raw, length, palette)
        if guess is None:
            write(output, t(lang, "guess_invalid", palette="".join(palette)))
            continue
        black, white = score(secret_code, guess)
        show_guess_result(output, guess, black, white, sound, lang)
        if black == length:
            sc = score_mod.compute_score(turns_max, n, won=True, bonus=bonus)
            sound.win()
            write(output, t(lang, "win_line", n=n, score=sc))
            return {"won": True, "score": sc, "turns": n, "difficulty": settings["difficulty"]}
        # show secret digits for feedback reference
        # compact hint: remaining colors info would spoil too much — skip

    # Out of turns
    sc = score_mod.compute_score(turns_max, turns_max, won=False, bonus=bonus)
    sound.lose()
    write(output, t(lang, "lose_line", secret=secret_str, score=sc))
    return {"won": False, "score": sc, "turns": turns_max, "difficulty": settings["difficulty"]}


def play_codemaker(
    settings: dict,
    sound: Sound,
    input_func: Callable[[str], str],
    output,
    rng: Optional[random.Random] = None,
) -> None:
    """Player picks a code, AI tries to crack it. No score — for fun."""
    rng = rng or random.Random()
    lang = settings["lang"]
    diff = settings_mod.DIFFICULTY[settings["difficulty"]]
    length = diff["length"]
    palette = COLORS[:diff["palette"]]
    turns_max = diff["turns"]

    palette_str = "".join(palette)
    write(output, t(lang, "ai_codemaker_intro", length=length, palette=palette_str))
    try:
        raw = input_func(t(lang, "prompt_choice")).strip()
    except (EOFError, KeyboardInterrupt):
        raise QuitGame()
    secret_code = parse_guess(raw, length, palette)
    if secret_code is None:
        write(output, t(lang, "guess_invalid", palette=palette_str))
        return

    solver = AISolver(length=length, colors=palette, rng=rng)
    write(output, t(lang, "ai_thinks"))

    for n in range(1, turns_max + 1):
        guess = solver.make_guess()
        if not guess:
            sound.lose()
            write(output, t(lang, "ai_inconsistent"))
            return
        write(output, t(lang, "ai_guess", guess="".join(guess)))
        black, white = score(secret_code, guess)
        if black == length:
            sound.win()
            write(output, t(lang, "result_line", guess="".join(guess), black=black, white=white))
            write(output, t(lang, "ai_won_line", n=n, total=turns_max))
            return
        try:
            fb_raw = input_func(t(lang, "ai_input_feedback")).strip()
        except (EOFError, KeyboardInterrupt):
            raise QuitGame()
        if fb_raw.lower() == "q":
            raise QuitRound()
        parts = fb_raw.replace(",", " ").split()
        if len(parts) != 2 or not all(p.isdigit() for p in parts):
            write(output, t(lang, "ai_invalid_feedback", n=length))
            continue
        b, w = int(parts[0]), int(parts[1])
        if b + w > length or b < 0 or w < 0:
            write(output, t(lang, "ai_invalid_feedback", n=length))
            continue
        solver.feedback(guess, b, w)

    sound.win()
    write(output, t(lang, "ai_lost_line", total=turns_max))


def show_scores(input_func, output, lang: str) -> None:
    scores = score_mod.load()
    write(output, t(lang, "scores_title"))
    if not scores:
        write(output, t(lang, "scores_empty"))
    else:
        for i, e in enumerate(scores, 1):
            write(output, t(
                lang, "scores_row",
                rank=i,
                name=e.get("name", "?"),
                score=e.get("score", 0),
                turns=e.get("turns", 0),
                win="Y" if e.get("won") else "N",
                lvl=e.get("difficulty", ""),
            ))
    try:
        input_func(t(lang, "press_enter"))
    except (EOFError, KeyboardInterrupt):
        pass


def show_help(input_func, output, lang: str) -> None:
    write(output, t(lang, "help_title"))
    write(output, t(lang, "help_body"))
    try:
        input_func(t(lang, "press_enter"))
    except (EOFError, KeyboardInterrupt):
        pass


def settings_menu(settings: dict, sound: Sound, input_func, output) -> None:
    while True:
        lang = settings["lang"]
        sound_label = t(lang, "on" if settings["sound"] else "off")
        diff_key = settings["difficulty"]
        write(output, t(lang, "settings_title"))
        write(output, t(lang, "settings_lang", value=t(lang, "lang_zh") if lang == "zh" else t(lang, "lang_en")))
        write(output, t(lang, "settings_sound", value=sound_label))
        write(output, t(lang, "settings_volume", value=settings["volume"]))
        write(output, t(lang, "settings_difficulty", value=t(lang, f"level_{diff_key}")))
        write(output, t(lang, "settings_back"))
        try:
            choice = input_func(t(lang, "prompt_choice")).strip().lower()
        except (EOFError, KeyboardInterrupt):
            return
        if choice == "1":
            settings["lang"] = settings_mod.cycle_lang(settings["lang"])
        elif choice == "2":
            settings["sound"] = not settings["sound"]
            sound.enabled = settings["sound"]
        elif choice == "3":
            settings["volume"] = settings_mod.cycle_volume(settings["volume"])
            sound.volume = settings["volume"]
        elif choice == "4":
            settings["difficulty"] = settings_mod.cycle_difficulty(settings["difficulty"])
        elif choice == "b":
            settings_mod.save(settings)
            return
        else:
            write(output, t(lang, "unknown"))


def main_menu(
    input_func: Callable[[str], str] = input,
    output=sys.stdout,
    rng: Optional[random.Random] = None,
) -> None:
    settings = settings_mod.load()
    sound = Sound(enabled=settings["sound"], volume=settings["volume"], output=output)
    rng = rng or random.Random()

    while True:
        lang = settings["lang"]
        write(output, "")
        write(output, t(lang, "title"))
        write(output, t(lang, "menu_play"))
        write(output, t(lang, "menu_codemaker"))
        write(output, t(lang, "menu_settings"))
        write(output, t(lang, "menu_scores"))
        write(output, t(lang, "menu_help"))
        write(output, t(lang, "menu_quit"))
        try:
            choice = input_func(t(lang, "prompt_choice")).strip().lower()
        except (EOFError, KeyboardInterrupt):
            write(output, t(lang, "bye"))
            return
        try:
            if choice == "p":
                result = play_guess(settings, sound, input_func, output, rng=rng)
                if result is not None:
                    try:
                        name = input_func(t(lang, "save_name")).strip()
                    except (EOFError, KeyboardInterrupt):
                        name = ""
                    if name:
                        scores = score_mod.load()
                        entry = {"name": name[:10], **result}
                        scores = score_mod.add_score(scores, entry)
                        score_mod.save(scores)
            elif choice == "c":
                play_codemaker(settings, sound, input_func, output, rng=rng)
            elif choice == "s":
                settings_menu(settings, sound, input_func, output)
            elif choice == "l":
                show_scores(input_func, output, lang)
            elif choice == "h":
                show_help(input_func, output, lang)
            elif choice == "q":
                write(output, t(lang, "bye"))
                return
            else:
                write(output, t(lang, "unknown"))
        except QuitGame:
            write(output, t(lang, "bye"))
            return
        except QuitRound:
            continue


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print()