from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests

# BOT_TOKEN = "8729069794:AAHW3mr3ZkD6uQP28YVSLVe7nX4KCxkclM8"
# FOOTBALL_TOKEN = "270ab7f04c124a33828d3ecf79d65d8c"

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
FOOTBALL_TOKEN = os.environ.get("FOOTBALL_TOKEN")

HEADERS = {"X-Auth-Token": FOOTBALL_TOKEN}

LEAGUES = {
    "bl1": {"url": "https://api.football-data.org/v4/competitions/BL1", "name": {"fa": "🇩🇪 بوندسلیگا", "de": "🇩🇪 Bundesliga", "en": "🇩🇪 Bundesliga"}},
    "pl":  {"url": "https://api.football-data.org/v4/competitions/PL",  "name": {"fa": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 پرمیر لیگ", "de": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League", "en": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League"}},
    "pd":  {"url": "https://api.football-data.org/v4/competitions/PD",  "name": {"fa": "🇪🇸 لالیگا", "de": "🇪🇸 La Liga", "en": "🇪🇸 La Liga"}},
    "sa":  {"url": "https://api.football-data.org/v4/competitions/SA",  "name": {"fa": "🇮🇹 سری آ", "de": "🇮🇹 Serie A", "en": "🇮🇹 Serie A"}},
    "fl1": {"url": "https://api.football-data.org/v4/competitions/FL1", "name": {"fa": "🇫🇷 لیگ ۱", "de": "🇫🇷 Ligue 1", "en": "🇫🇷 Ligue 1"}},
    "cl":  {"url": "https://api.football-data.org/v4/competitions/CL",  "name": {"fa": "🏆 لیگ قهرمانان", "de": "🏆 Champions League", "en": "🏆 Champions League"}},
    "wc":  {"url": "https://api.football-data.org/v4/competitions/WC",  "name": {"fa": "🌍 جام جهانی", "de": "🌍 WM 2026", "en": "🌍 World Cup"}},
}

TEXTS = {
    "fa": {
        "welcome": "سلام! 👋 به ربات فوتبال خوش اومدی! ⚽",
        "choose_league": "لیگ مورد نظرت رو انتخاب کن:",
        "choose_action": "چی میخوای ببینی؟",
        "standings": "🏆 جدول",
        "results": "📋 نتایج",
        "next": "📅 بازی‌های آینده",
        "scorers": "⚽ گلزنان",
        "back": "🔙 بازگشت",
        "no_next": "فعلاً بازی برنامه‌ریزی شده‌ای نیست!",
        "pts": "امتیاز",
        "goals": "گل",
    },
    "de": {
        "welcome": "Hallo! 👋 Willkommen beim Fußball-Bot! ⚽",
        "choose_league": "Wähle eine Liga:",
        "choose_action": "Was möchtest du sehen?",
        "standings": "🏆 Tabelle",
        "results": "📋 Ergebnisse",
        "next": "📅 Kommende Spiele",
        "scorers": "⚽ Torjäger",
        "back": "🔙 Zurück",
        "no_next": "Keine kommenden Spiele!",
        "pts": "Pts",
        "goals": "Tore",
    },
    "en": {
        "welcome": "Hello! 👋 Welcome to the Football Bot! ⚽",
        "choose_league": "Choose a league:",
        "choose_action": "What do you want to see?",
        "standings": "🏆 Standings",
        "results": "📋 Results",
        "next": "📅 Upcoming Matches",
        "scorers": "⚽ Top Scorers",
        "back": "🔙 Back",
        "no_next": "No upcoming matches!",
        "pts": "pts",
        "goals": "goals",
    }
}

user_data = {}

def get_lang(user_id):
    return user_data.get(user_id, {}).get("lang", "en")

def get_league(user_id):
    return user_data.get(user_id, {}).get("league", "bl1")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
        InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
    ]]
    await update.message.reply_text(
        "🌍 زبان / Sprache / Language:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_leagues(query, lang):
    t = TEXTS[lang]
    keyboard = [
        [InlineKeyboardButton(LEAGUES["bl1"]["name"][lang], callback_data="league_bl1"),
         InlineKeyboardButton(LEAGUES["pl"]["name"][lang], callback_data="league_pl")],
        [InlineKeyboardButton(LEAGUES["pd"]["name"][lang], callback_data="league_pd"),
         InlineKeyboardButton(LEAGUES["sa"]["name"][lang], callback_data="league_sa")],
        [InlineKeyboardButton(LEAGUES["fl1"]["name"][lang], callback_data="league_fl1"),
         InlineKeyboardButton(LEAGUES["cl"]["name"][lang], callback_data="league_cl")],
        [InlineKeyboardButton(LEAGUES["wc"]["name"][lang], callback_data="league_wc")],
    ]
    await query.edit_message_text(
        f"{t['welcome']}\n\n{t['choose_league']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_menu(query, lang, league):
    t = TEXTS[lang]
    league_name = LEAGUES[league]["name"][lang]
    keyboard = [
        [InlineKeyboardButton(t["standings"], callback_data="action_standings"),
         InlineKeyboardButton(t["results"], callback_data="action_results")],
        [InlineKeyboardButton(t["next"], callback_data="action_next"),
         InlineKeyboardButton(t["scorers"], callback_data="action_scorers")],
        [InlineKeyboardButton(t["back"], callback_data="back_leagues")],
    ]
    await query.edit_message_text(
        f"{league_name}\n\n{t['choose_action']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data.startswith("lang_"):
        lang = data.split("_")[1]
        user_data[user_id] = {"lang": lang, "league": "bl1"}
        await show_leagues(query, lang)

    elif data.startswith("league_"):
        league = data.split("_")[1]
        lang = get_lang(user_id)
        user_data[user_id]["league"] = league
        await show_menu(query, lang, league)

    elif data == "back_leagues":
        lang = get_lang(user_id)
        await show_leagues(query, lang)

    elif data.startswith("action_"):
        action = data.split("_")[1]
        lang = get_lang(user_id)
        league = get_league(user_id)
        t = TEXTS[lang]
        url = LEAGUES[league]["url"]
        league_name = LEAGUES[league]["name"][lang]

        try:
            if action == "standings":
                res = requests.get(f"{url}/standings", headers=HEADERS).json()
                table = res["standings"][0]["table"]
                text = f"{t['standings']} — {league_name}:\n\n"
                for row in table:
                    text += f"{row['position']}. {row['team']['name']} — {row['points']} {t['pts']}\n"

            elif action == "results":
                res = requests.get(f"{url}/matches?status=FINISHED", headers=HEADERS).json()
                matches = res["matches"][-10:]
                text = f"{t['results']} — {league_name}:\n\n"
                for m in matches:
                    hg = m["score"]["fullTime"]["home"]
                    ag = m["score"]["fullTime"]["away"]
                    text += f"{m['homeTeam']['name']} {hg} - {ag} {m['awayTeam']['name']}\n"

            elif action == "next":
                res = requests.get(f"{url}/matches?status=SCHEDULED,TIMED", headers=HEADERS).json()
                matches = res["matches"][:10]
                if not matches:
                    text = f"⚽ {t['no_next']}"
                else:
                    text = f"{t['next']} — {league_name}:\n\n"
                    for m in matches:
                        date = m["utcDate"][:10]
                        text += f"{date}: {m['homeTeam']['name']} vs {m['awayTeam']['name']}\n"

            elif action == "scorers":
                res = requests.get(f"{url}/scorers", headers=HEADERS).json()
                scorers = res["scorers"][:10]
                text = f"{t['scorers']} — {league_name}:\n\n"
                for i, s in enumerate(scorers, 1):
                    text += f"{i}. {s['player']['name']} ({s['team']['name']}) — {s['goals']} {t['goals']}\n"

        except Exception as e:
            text = "❌ خطا در دریافت اطلاعات — دوباره امتحان کن!"

        keyboard = [[InlineKeyboardButton(t["back"], callback_data="back_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "back_menu":
        lang = get_lang(user_id)
        league = get_league(user_id)
        await show_menu(query, lang, league)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(callback_handler))

print("ربات شروع به کار کرد... ⚽")
app.run_polling()