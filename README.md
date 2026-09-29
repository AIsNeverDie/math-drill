# 🧮 Math Drill

> An exciting math trainer for kids — combos, trophies, streaks & time capsules. Beat the clock in Extra mode.

**🇺🇸 English · 🇯🇵 [日本語](README.ja.md) · 🇨🇳 [简体中文](README.zh-CN.md) · 🇹🇼 [繁體中文](README.zh-TW.md)**

---

## What is this?

A browser-based math practice game for Grade 1–6 elementary school students. It looks like a game, plays like a game, and somehow also teaches arithmetic.

Kids work through a **skill tree** of 58 math skills — from single-digit addition all the way to fractions, ratios, and long division. The system tracks what they know, what they're rusty on, and what they're ready to learn next.

---

## Features

| Feature | Description |
|:--------|:------------|
| 🌳 **Skill Tree** | 58 skills across 6 grades, with prerequisite chains |
| 📅 **Daily Quests** | 3 goals per day, matched to the child's current level |
| 🔥 **Combo System** | Answer fast and correctly to build a multiplier up to ×2 |
| ⏱️ **Extra Mode (加时赛)** | 90-second bonus round unlocked by ≥80% first-try accuracy |
| 🏆 **300+ Trophies** | Achievements for speed, accuracy, streaks, and milestones |
| 🎒 **Collectibles** | Unlock avatar costumes by earning trophies |
| 📦 **Time Capsule** | Revisit a problem from your very first day, after 30 days |
| 📈 **Growth Tracking** | Stars, speed records, and retention metrics per skill |
| 🔐 **Offline-first** | No account needed — all data lives in `localStorage` |

---

## Gameplay Loop

```
Home → Start a session → Answer 10 problems (Basic)
     → Result screen → Extra mode unlocked? → 90-sec sprint
     → Final score → Trophies & skill news → Home
```

Each problem is chosen by an **adaptive engine**: it weighs spaced repetition, recent errors, skill prerequisites, and combo state to pick the right challenge at the right moment.

---

## Tech Stack

- **Pure vanilla JS** — zero frameworks, zero build step
- **ES modules** — native browser imports, no bundler
- **CSS custom properties** — theme and font vars per language
- **`localStorage`** — all progress stored client-side
- **Node.js test runner** — 66 unit tests, no test framework needed

```
app/
├── index.html          # Language router
├── en/                 # English version (self-contained)
├── ja/                 # Japanese version
├── zh-CN/              # Simplified Chinese version
├── zh-TW/              # Traditional Chinese version
│   ├── index.html
│   ├── style.css
│   ├── fonts/          # Language-specific WOFF2 subsets
│   └── js/
│       ├── main.js     # UI & game loop
│       ├── problems.js # Problem generators (all skill types)
│       ├── skills.js   # Skill tree & mastery logic
│       ├── scoring.js  # Dopa & combo math
│       ├── trophies.js # Achievement catalogue
│       ├── quests.js   # Daily quest engine
│       └── store.js    # localStorage persistence
tests/                  # 66 unit tests (Node built-in runner)
tools/                  # Font subsetting scripts
```

---

## Languages & Fonts

Each language ships its own font subset — no cross-language font mixing:

| Language | Chunky font | Body font |
|:---------|:------------|:----------|
| English  | Dela Gothic One | Zen Maru Gothic |
| Japanese | Dela Gothic One | Zen Maru Gothic |
| 简体中文  | ZCOOL KuaiLe | PingFang SC / Microsoft YaHei |
| 繁體中文  | ZCOOL KuaiLe | PingFang TC / Microsoft JhengHei |

Font subsets are built per-language from actual game text — only the glyphs that appear in the game are shipped.

---

## Run Locally

No install, no build:

```bash
python3 -m http.server 8000 -d app
# → open http://localhost:8000
```

---

## Run Tests

```bash
node --test tests/*.test.mjs
# 66 tests, ~400ms
```

---

## Credits

This is an unofficial Simplified/Traditional Chinese localization.

| | |
|:--|:--|
| 🎮 **Original game** | [ドパドリル (Dopa Drill)](https://github.com/grmchn/dopa-drill) by **gear_machine** |
| 🌏 **English localization** | [math-drill](https://github.com/elatd/math-drill) by **elatd** |
| 🇨🇳 🇹🇼 **Chinese localization** | This repository |

---

## License

**Source code:** MIT License

**Fonts:** [SIL Open Font License 1.1](https://openfontlicense.org) — see `app/*/fonts/OFL-*.txt`

**Character & branding — Dopakichi (ドパキチ) and the Dopa Drill name/logo:**  
These are **not** covered by the MIT License and belong to the original author (gear_machine).  
- ✅ Non-commercial fan works, forks, and modifications are freely allowed without prior permission  
- ✅ Gameplay videos and streams are allowed (ad revenue / donations OK)  
- ❌ Commercial use, merchandise, paid products, or official branding requires permission from the original author  
- ❌ Content that harms the character's or project's reputation is prohibited  

Please make clear that any derivative work is **unofficial**.  
See the [original LICENSE](https://github.com/grmchn/dopa-drill/blob/main/LICENSE) for the authoritative terms (English text takes precedence).
