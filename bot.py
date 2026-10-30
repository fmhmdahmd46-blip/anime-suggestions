import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# سيرفر وهمي عشان Render ما يفشل
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(('0.0.0.0', port), Handler).serve_forever()

threading.Thread(target=run_server, daemon=True).start()
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

SYSTEM_PROMPT = """
انت مساعد انمي سوداني رهيب، بتتكلم باللهجة السودانية العامية (زي "يا زول", "ظابط", "رهيب").
مهمتك ترشح انميات حسب مزاج المستخدم.
لو المستخدم قال داير اكشن زي قاتل الشياطين وجوجيتسو كايسن رشح ليه Chainsaw Man, Jujutsu Kaisen, Demon Slayer, Bleach.
لو قال رومانسي رشح Your Name, Clannad.
لو قال حزين رشح Anohana.
دائما رد بالسوداني وبطريقة حماسية ومختصرة ومع ايموجي.
"""

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا يا زول! 😍 انا بوت الانمي السوداني. قول لي داير تحضر شنو؟\nمثلا: داير انمي اكشن زي قاتل الشياطين")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            temperature=0.8,
        )
        reply = completion.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"حصل ايرور يا زول: {e}")

def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    main()
