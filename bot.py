import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# عشان Fly ما يفتكر البوت نايم
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    server.serve_forever()

# شغل السيرفر في الخلفية
threading.Thread(target=run_health_server, daemon=True).start()

# المفاتيح
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not TELEGRAM_TOKEN or not GROQ_API_KEY:
    print("ERROR: Missing TELEGRAM_TOKEN or GROQ_API_KEY in Secrets!")
    
client = Groq(api_key=GROQ_API_KEY)

# رسالة البداية - هنا كان الغلط قبيل
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "يا زول هلا والله! \U0001f60e\U0001f525\n"
        "انا بوت اقتراحات الانمي حقك.\n"
        "قول لي بتحب شنو وانا برشح ليك \U0001f3ac"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "انت مساعد انمي سوداني، تتكلم لهجة سودانية خفيفة، ترشح انميات حسب ذوق المستخدم، ردودك قصيرة وممتعة."},
                {"role": "user", "content": user_text}
            ],
            max_tokens=500
        )
        reply = completion.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        print(f"Groq Error: {e}")
        await update.message.reply_text("والله حصل ايرور يا زول، جرب تاني شوية \U0001f62d")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
