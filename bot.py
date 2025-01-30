import os
import telebot
from services.drm_service import generate_drm_keys

# Load the token from environment variables
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', 'default_token_if_not_set')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'default_telegram_bot_token')

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me a video URL to get DRM keys.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    video_url = message.text
    result = generate_drm_keys(video_url, ACCESS_TOKEN)
    if "error" in result:
        bot.reply_to(message, f"Error: {result['error']}")
    else:
        bot.reply_to(message, f"MPD URL: {result['mpd_url']}\nKeys: {', '.join(result['keys'])}")

if __name__ == '__main__':
    bot.polling()
