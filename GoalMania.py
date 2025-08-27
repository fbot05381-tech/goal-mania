import telebot
import random
from datetime import datetime, timedelta
y
# Replace with your BotFather token
TOKEN = "7076818138:AAFaXvRv4qjc_c04Nv2HmVnIHAHTpl23rzo"
bot = telebot.TeleBot(TOKEN)

# Store player stats
players = {}
leaderboard_reset_time = datetime.now() + timedelta(days=1)

def reset_leaderboard():
    global players, leaderboard_reset_time
    players = {}
    leaderboard_reset_time = datetime.now() + timedelta(days=1)

def get_player(user_id):
    if user_id not in players:
        players[user_id] = {"goals": 0, "shots": 0, "streak": 0}
    return players[user_id]

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
        "⚽ Welcome to Football Bot!\n"
        "Use /shoot to try scoring a goal.\n"
        "Check your /profile and the /leaderboard.\n"
        "Leaderboard resets daily 🔄"
    )

@bot.message_handler(commands=['shoot'])
def shoot(message):
    global leaderboard_reset_time
    if datetime.now() >= leaderboard_reset_time:
        reset_leaderboard()

    user = get_player(message.from_user.id)
    user["shots"] += 1

    outcome = random.choice(["goal", "miss", "save", "crossbar"])

    if outcome == "goal":
        user["goals"] += 1
        user["streak"] += 1
        msg = f"🎯 GOAL!!! You scored!\n🔥 Streak: {user['streak']}"
        if user["streak"] >= 3:
            user["goals"] += 2  # bonus points
            msg += "\n🔥🔥 STREAK BONUS +2!"
    else:
        user["streak"] = 0
        if outcome == "miss":
            msg = "❌ You missed the goal..."
        elif outcome == "save":
            msg = "🧤 The keeper saved it!"
        else:
            msg = "🔔 CROSSBAR!! So close!"

    bot.reply_to(message, msg)

@bot.message_handler(commands=['profile'])
def profile(message):
    user = get_player(message.from_user.id)
    accuracy = (user["goals"] / user["shots"] * 100) if user["shots"] > 0 else 0
    bot.reply_to(message,
        f"📊 Profile of {message.from_user.first_name}\n"
        f"Goals: {user['goals']}\n"
        f"Shots: {user['shots']}\n"
        f"Accuracy: {accuracy:.1f}%\n"
        f"Current Streak: {user['streak']}"
    )

@bot.message_handler(commands=['leaderboard'])
def leaderboard(message):
    if datetime.now() >= leaderboard_reset_time:
        reset_leaderboard()

    if not players:
        bot.reply_to(message, "📉 No players yet. Start shooting with /shoot!")
        return

    sorted_players = sorted(players.items(), key=lambda x: x[1]["goals"], reverse=True)
    top_players = sorted_players[:10]

    text = "🏆 Daily Leaderboard 🏆\n\n"
    for i, (uid, data) in enumerate(top_players, 1):
        text += f"{i}. Goals: {data['goals']} | Shots: {data['shots']}\n"

    bot.reply_to(message, text)

print("⚽ Football Bot is running...")
bot.infinity_polling()
