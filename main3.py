#pylint
"""
Telegram bot for Fidelio - Image encryption & decryption
"""

import telebot
import main
import main2


API_TOKEN = "7959422543:AAE7Ciy_AnFUm3b3Cr11HwSOiDtS43DTykI"
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
        """👋 Welcome to **Fidelio** 🔐

This bot lets you **encrypt** and **decrypt images** using a custom-built, secure algorithm developed just for this project.

🛡️ Whether you're looking to protect your personal memories or secure sensitive visual data, **Fidelio** has you covered.

✨ Commands to get started:
- /encrypt – Encrypt an image
- /decrypt – Decrypt an encrypted image
- /help – View usage instructions

Ready to protect your pixels? Let's begin.
        """)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message,
                 """✨ Commands to get started:
- /encrypt – Encrypt an image
- /decrypt – Decrypt an encrypted image
- /help – View usage instructions
                  """)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)
    
    
    
bot.infinity_polling()
