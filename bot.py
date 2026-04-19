import telebot
import os
from flask import Flask
from threading import Thread

# 1. Bot va Server sozlamalari
TOKEN = '8701941489:AAG5fLoANqgV9CP6L-8qBuA2_gONWabYZF4' 
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot yoniq!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# 2. Referal tizimi
users = {} 

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if user_id not in users:
        users[user_id] = {'referrals': 0, 'balance': 0}
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("👤 Kabinet", "🔗 Referal Link")
    bot.send_message(user_id, "Xush kelibsiz! Pul ishlash botiga start berdingiz.", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "👤 Kabinet")
def cabinet(message):
    u = users.get(message.chat.id, {'referrals': 0, 'balance': 0})
    bot.send_message(message.chat.id, f"Sizning balansingiz: {u['balance']} so'm\nTaklif qilgan do'stlaringiz: {u['referrals']} ta")

@bot.message_handler(func=lambda m: m.text == "🔗 Referal Link")
def link(message):
    bot_username = bot.get_me().username
    referral_link = f"https://t.me/{bot_username}?start={message.chat.id}"
    bot.send_message(message.chat.id, f"Sizning referal havolangiz:\n\n{referral_link}\n\nDo'stlaringizni taklif qiling va pul ishlang!")

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)

