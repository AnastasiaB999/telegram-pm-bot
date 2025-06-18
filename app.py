import os
from flask import Flask, request, jsonify
from openai_helper import OpenAIHelper
import telebot

app = Flask(__name__)
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
openai_key = os.environ.get("OPENAI_API_KEY")
bot = telebot.TeleBot(bot_token)
ai_helper = OpenAIHelper()

SYSTEM_PROMPT = """Ты — Telegram-бот, персональный помощник продуктового менеджера, работающего на платформе 999.md — крупнейшем классифайде в Молдове. Твоя задача — помогать выстраивать корректный, реалистичный и эффективный дизайн экспериментов под задачи продукта..."""

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    result = ai_helper.generate_response(user_input, SYSTEM_PROMPT)
    if result["success"]:
        bot.send_message(message.chat.id, result["response"])
    else:
        bot.send_message(message.chat.id, "Ошибка: " + result["error"])

@app.route("/webhook", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return jsonify({"ok": True})

@app.route("/")
def home():
    return "Bot is running"
