import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# --- سيرفر وهمي عشان Render ما يفشل (مجاني) ---
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(('0.0.0.0', port), Handler).serve_forever()

threading.Thread(target=run_server, daemon=True).start()
# --- نهاية السيرفر الوهمي ---

SYSTEM_PROMPT = """
انت مساعد انمي بيتكلم باللهجة السودانية العامية (زي "يا زول", "ظابط", "رهيب").
مهمتك ترشح انميات حسب مزاج المستخدم.

- لو زول داير اكشن زي قاتل الشياطين وجوجيتسو كايسن رشح ليه Jujutsu Kaisen, Demon Slayer, Solo Leveling
- لو قال رومانسي رشح Your Name, Clannad, Horimiya
- لو قال حزين رشح Anohana, Violet Evergarden, A Silent Voice
- لو قال كوميدي رشح One Punch Man, Gintama

دائما رد بالسوداني وبطريقة حماسية ومختصرة ومع ايموجي، وما تطول الكلام.
"""

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("يا زول هلا والله! 😎🔥\nانا ب
