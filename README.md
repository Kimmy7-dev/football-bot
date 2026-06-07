# ⚽ Football News Bot

A multilingual Telegram bot that provides real-time football data including standings, results, upcoming matches, and top scorers across major European leagues.

🤖 **Try it on Telegram:** [@Bundesliga_newsbot](https://t.me/Bundesliga_newsbot)

---

## 🌍 Supported Languages
- 🇮🇷 Persian (Farsi)
- 🇩🇪 German
- 🇬🇧 English

## 🏆 Supported Leagues
| League | Country |
|--------|---------|
| Premier League | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 England |
| La Liga | 🇪🇸 Spain |
| Bundesliga | 🇩🇪 Germany |
| Serie A | 🇮🇹 Italy |
| Ligue 1 | 🇫🇷 France |
| Champions League | 🏆 Europe |
| World Cup | 🌍 International |

## ✨ Features
- 🏆 **Live Standings** — Full league table with points
- 📋 **Recent Results** — Last 10 finished matches
- 📅 **Upcoming Matches** — Next scheduled games
- ⚽ **Top Scorers** — Top 10 goal scorers per league
- 🌐 **Multilingual** — Switch between 3 languages anytime

## 🛠️ Tech Stack
- **Python** — Core language
- **python-telegram-bot** — Telegram API wrapper
- **football-data.org API** — Live football data
- **PythonAnywhere** — Cloud hosting

## 🚀 How to Run Locally
```bash
git clone https://github.com/Kimmy7-dev/football-bot
cd football-bot
pip install -r requirements.txt
export BOT_TOKEN="your_telegram_bot_token"
export FOOTBALL_TOKEN="your_football_api_token"
python main.py
```
