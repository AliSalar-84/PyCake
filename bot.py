# pylint
"""
Telegram bot for Fidelio - Image encryption & decryption
"""
import os
import string
from io import BytesIO

import telebot
from PIL import Image

from main import encode_message_in_image
from main2 import decode_message_from_image

API_TOKEN = os.environ.get("BOT_TOKEN") or "YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(m):
    bot.reply_to(m,
        """👋 Welcome to **Fidelio** 🔐

Encrypt & decrypt images easily.

✨ Commands:
- Reply to an image with /Aegis or /Hide for encryption.
- Reply to an encrypted image/document_file with /Oblivion or /Reveal for decryption.
- /help – View instructions.
        """)

@bot.message_handler(commands=['help'])
def send_help(m):
    bot.reply_to(m,
        """✨ Usage:
- Reply to an image with /Aegis or /Hide → enter psypher.
- Reply to an encrypted image with /Oblivion or /Reveal → get hidden message.
        """)

@bot.message_handler(func=lambda m: m.text
                                     and not m.text.startswith('/') and m.from_user.id not in pending_encrypt)
def echo_message(m):
    bot.reply_to(m, m.text)

pending_encrypt = {}

@bot.message_handler(commands=['Aegis' , 'Hide'])
def ask_psypher(m):
    if not (m.reply_to_message and m.reply_to_message.photo):
        return bot.reply_to(m, "⚠️ Reply to an image with /Aegis or /Hide.")
    pending_encrypt[m.from_user.id] = m.reply_to_message.photo[-1].file_id
    bot.reply_to(m, "🔑 PLEASE ENTER THE PSYPHER:")

@bot.message_handler(func=lambda m: m.from_user.id in pending_encrypt)
def do_encrypt(m):
    fid = pending_encrypt.pop(m.from_user.id)
    file_info = bot.get_file(fid)
    img = Image.open(BytesIO(bot.download_file(file_info.file_path)))
    out = BytesIO(); out.name = "encrypted.png"
    encode_message_in_image(img, m.text).save(out, "PNG")
    out.seek(0)
    bot.send_document(m.chat.id, out, caption="🔐 Encrypted!")

def is_text(data) -> bool:
    if isinstance(data, str):
        text = data
    else:
        try:
            text = data.decode('utf-8')
        except UnicodeDecodeError:
            return False
    return all(c in string.printable or c in "\n\r\t" for c in text)

def escape_markdown_v2(text: str) -> str:
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    return ''.join(f"\\{c}" if c in escape_chars else c for c in text)

MAX_MESSAGE_LENGTH = 10000

@bot.message_handler(commands=['Oblivion', 'Reveal'])
def decrypt_handler(m):
    if not (m.reply_to_message and (m.reply_to_message.photo or m.reply_to_message.document)):
        return bot.reply_to(m, "⚠️ Reply to an encrypted image or file with /Oblivion or /Reveal.")

    fid = m.reply_to_message.photo[-1].file_id if m.reply_to_message.photo else m.reply_to_message.document.file_id
    file_info = bot.get_file(fid)
    file_bytes = bot.download_file(file_info.file_path)
    img = Image.open(BytesIO(file_bytes))

    hidden_text = decode_message_from_image(img)
    escaped = escape_markdown_v2(hidden_text)

    if len(escaped) <= MAX_MESSAGE_LENGTH:
        bot.reply_to(m, f"HIDDEN PSYPHER:\n||{escaped}||", parse_mode="MarkdownV2")
    else:
        out = BytesIO(hidden_text.encode("utf-8"))
        out.name = "hidden_psypher.txt"
        out.seek(0)
        bot.send_document(m.chat.id, out, caption="🔓 Hidden psypher (too long)")

bot.infinity_polling()
