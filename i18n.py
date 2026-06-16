"""Bilingual strings."""
STRINGS = {
    "zh": {
        "title": "珠玑妙算 / Mastermind",
        "menu_play": "P) 开始猜码",
        "menu_codemaker": "C) 我来出码 (你猜)",
        "menu_settings": "S) 设置",
        "menu_scores": "L) 排行榜",
        "menu_help": "H) 帮助",
        "menu_quit": "Q) 退出",
        "prompt_choice": "选择> ",
        "settings_title": "── 设置 ──",
        "settings_lang": "1) 语言: {value}",
        "settings_sound": "2) 音效: {value}",
        "settings_volume": "3) 音量: {value}",
        "settings_difficulty": "4) 难度: {value}",
        "settings_back": "B) 返回",
        "scores_title": "── 排行榜 (Top 10) ──",
        "scores_empty": "暂无记录。",
        "scores_row": "{rank:>2}. {name:<10} {score:>5}  turns={turns}  win={win}  lvl={lvl}",
        "help_title": "── 帮助 ──",
        "help_body": (
            "电脑随机生成一串密码,你需在限定回合内猜中。\n"
            "颜色:R(红) G(绿) B(蓝) Y(黄) O(橙) P(紫)。\n"
            "每次输入与码长相等的字母串,例如 RGBY。\n"
            "反馈:●(黑钉)= 颜色与位置都对;○(白钉)= 颜色对但位置不对。\n"
            "全为黑钉即猜中。得分 = (剩余回合 * 100) - 用时回合数 + 难度奖励。"
        ),
        "press_enter": "回车继续...",
        "round_start": "── 新一局,密码长度 {length},回合上限 {turns} ──",
        "your_guess": "回合 {n}/{total}, 输入猜测 (或 Q 放弃): ",
        "guess_invalid": "输入无效,请重试。颜色字母:{palette}",
        "result_line": "{guess} → ●{black}  ○{white}",
        "win_line": "猜中!用了 {n} 回合, 得分 {score}。",
        "lose_line": "回合用尽。密码是 {secret}。得分 {score}。",
        "save_name": "输入名字保存(回车跳过): ",
        "level_easy": "简单 (4色4位 12回合)",
        "level_normal": "普通 (6色4位 10回合)",
        "level_hard": "困难 (6色5位 10回合)",
        "on": "开",
        "off": "关",
        "lang_zh": "中文",
        "lang_en": "English",
        "bye": "再见!",
        "unknown": "未知选择。",
        "ai_codemaker_intro": "请输入你的密码 (其他人勿看!),长度 {length},颜色 {palette}: ",
        "ai_thinks": "AI 正在思考...",
        "ai_guess": "AI 猜 {guess}",
        "ai_input_feedback": "请输入反馈,格式 'B W' (黑钉 白钉,例如 '2 1') 或 Q 放弃: ",
        "ai_invalid_feedback": "反馈无效,请输入两个 0..{n} 间的数字。",
        "ai_won_line": "AI 在 {n} 回合内破解了你的密码!",
        "ai_lost_line": "AI 在 {total} 回合内未能破解密码,你赢了!",
        "ai_inconsistent": "你给出的反馈互相矛盾,AI 无法继续。",
    },
    "en": {
        "title": "Mastermind",
        "menu_play": "P) Play (you guess)",
        "menu_codemaker": "C) I make the code (AI guesses)",
        "menu_settings": "S) Settings",
        "menu_scores": "L) Leaderboard",
        "menu_help": "H) Help",
        "menu_quit": "Q) Quit",
        "prompt_choice": "Choice> ",
        "settings_title": "-- Settings --",
        "settings_lang": "1) Language: {value}",
        "settings_sound": "2) Sound: {value}",
        "settings_volume": "3) Volume: {value}",
        "settings_difficulty": "4) Difficulty: {value}",
        "settings_back": "B) Back",
        "scores_title": "-- Leaderboard (Top 10) --",
        "scores_empty": "No scores yet.",
        "scores_row": "{rank:>2}. {name:<10} {score:>5}  turns={turns}  win={win}  lvl={lvl}",
        "help_title": "-- Help --",
        "help_body": (
            "The computer picks a hidden code; guess it within the turn limit.\n"
            "Colors: R(ed) G(reen) B(lue) Y(ellow) O(range) P(urple).\n"
            "Type a string of letters equal to the code length, e.g. RGBY.\n"
            "Feedback: B(black) = right colour & position; W(white) = right colour, wrong position.\n"
            "All-black means solved. Score = (remaining turns * 100) - turns used + difficulty bonus."
        ),
        "press_enter": "Press Enter to continue...",
        "round_start": "-- New round, code length {length}, turn limit {turns} --",
        "your_guess": "Turn {n}/{total}, your guess (or Q to give up): ",
        "guess_invalid": "Invalid input. Palette: {palette}",
        "result_line": "{guess} -> B{black}  W{white}",
        "win_line": "Solved in {n} turns! Score {score}.",
        "lose_line": "Out of turns. Code was {secret}. Score {score}.",
        "save_name": "Enter name to save (blank to skip): ",
        "level_easy": "Easy (4 colors, 4 pegs, 12 turns)",
        "level_normal": "Normal (6 colors, 4 pegs, 10 turns)",
        "level_hard": "Hard (6 colors, 5 pegs, 10 turns)",
        "on": "On",
        "off": "Off",
        "lang_zh": "Chinese",
        "lang_en": "English",
        "bye": "Bye!",
        "unknown": "Unknown choice.",
        "ai_codemaker_intro": "Type your secret (others look away!) length {length}, palette {palette}: ",
        "ai_thinks": "AI is thinking...",
        "ai_guess": "AI guesses {guess}",
        "ai_input_feedback": "Enter feedback as 'B W' (black white, e.g. '2 1') or Q to abort: ",
        "ai_invalid_feedback": "Invalid feedback. Enter two ints in 0..{n}.",
        "ai_won_line": "AI cracked your code in {n} turns!",
        "ai_lost_line": "AI failed to crack the code in {total} turns. You win!",
        "ai_inconsistent": "Your feedback is inconsistent. AI gives up.",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    table = STRINGS.get(lang, STRINGS["en"])
    val = table.get(key, key)
    if isinstance(val, str) and kwargs:
        try:
            return val.format(**kwargs)
        except (KeyError, IndexError):
            return val
    return val
