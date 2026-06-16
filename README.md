# Mastermind / 珠玑妙算

A console **Mastermind** in pure Python (stdlib only): the computer hides a colour code, you crack it within the turn limit using black/white peg feedback. Reverse mode included — *you* hide a code and an AI deduces it.

一个用 Python 标准库实现的控制台版珠玑妙算:电脑随机生成颜色密码,你在限定回合内根据黑钉/白钉反馈破译。也可反向玩——你出题,AI 用候选剔除推理破解。

---

## Features / 功能

- **Two modes** — *you guess* (classic) and *codemaker* (you set the secret, AI cracks it).
- **Three difficulties** — easy (4 colours, 4 pegs, 12 turns), normal (6/4/10), hard (6/5/10).
- **Bilingual UI** (中文 / English) — switch in Settings.
- **Sound** via terminal bell (guess / hit / win / lose), on/off + 0–3 volume.
- **Persistent leaderboard** (`~/.mastermind_scores.json`), top 10.
- **Persistent settings** (`~/.mastermind_settings.json`).
- **57 tests** covering pure-logic secret/judge/AI solver, persistence, i18n, sound, menu flow.

## Requirements / 环境

- Python 3.9 or newer
- Any terminal — no `curses` needed
- No third-party packages

## Quick Start / 快速开始

```bash
git clone https://github.com/<your-user>/mastermind.git
cd mastermind
python3 game.py
```

In the menu:

| Key | Action |
|-----|-----|
| `P` | Play / 开始猜码 |
| `C` | I make the code, AI guesses / 我来出码 |
| `S` | Settings / 设置 |
| `L` | Leaderboard / 排行榜 |
| `H` | Help / 帮助 |
| `Q` | Quit / 退出 |

In a round:

| Input | Action |
|-----|-----|
| e.g. `RGBY` | Your guess of length = code length |
| `Q` | Quit current round / 退出本局 |

## Game Logic

- The palette is `R G B Y O P` (red, green, blue, yellow, orange, purple).
- After each guess you receive `●N ○M`:
  - `●` (black peg) — correct colour and correct position.
  - `○` (white peg) — correct colour but wrong position. Whites do not double-count blacks.
- All-black equals the code length means solved.
- **Scoring** (you-guess mode): `(turns_remaining * 100) − turns_used + difficulty_bonus`. Hard mode adds a 250 bonus.

The pure-logic core lives in `secret.py`, `judge.py`, `ai_solver.py` — no I/O, no globals, fully unit-testable. `game.py` glues them together with `input_func` / `output` injection so tests drive the menu by stacked strings.

### Codemaker mode

You type a secret (others look away!), then the AI uses simple **candidate elimination** — every guess prunes the candidate set down to those compatible with the feedback you've given. With a length-4 / 6-colour palette it converges within ~6 guesses on average.

## Project Layout

```
mastermind/
├── game.py              # menu + you-guess + codemaker loops
├── secret.py            # secret generation + guess parsing
├── judge.py             # black/white peg scoring
├── ai_solver.py         # candidate-elimination solver
├── i18n.py              # zh / en strings
├── sound.py             # terminal-bell sound
├── settings.py          # persistent settings + difficulty profiles
├── score.py             # persistent leaderboard
├── tests/
│   ├── test_secret.py
│   ├── test_judge.py
│   ├── test_ai_solver.py
│   ├── test_modules.py
│   ├── test_game.py
│   └── run_tests.py
├── README.md
└── .gitignore
```

## Running Tests

```bash
python3 -m unittest discover tests/
# or
python3 tests/run_tests.py
```

Expected: `Ran 57 tests`, all passing.

## Settings & Scores Files

- Settings:    `~/.mastermind_settings.json`
- Leaderboard: `~/.mastermind_scores.json`

Delete to reset.

## License

MIT — use freely.
