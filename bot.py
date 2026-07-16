import logging
import os
import threading
import yt_dlp
from flask import Flask
from telegram import Update, ReactionTypeEmoji
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot Online", 200

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

logging.basicConfig(level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    # Desteklenen platformlar
    platforms = ["youtube.com", "youtu.be", "tiktok.com", "twitter.com", "x.com", "instagram.com"]
    
    if any(platform in text for platform in platforms):
        try:
            await update.message.set_reaction(reaction=[ReactionTypeEmoji(emoji="👁️")])
        except:
            pass
        
        status_msg = await update.message.reply_text("🔎 İndiriliyor...")
        file_path = "/tmp/media.mp4"
        
        try:
            # yt-dlp tüm bu platformları otomatik tanır
            ydl_opts = {
                'outtmpl': file_path,
                'quiet': True,
                'no_warnings': True,
                'cookiefile': 'cookies.txt', # Her platform için aynı cookie dosyasını kullanır
                'format': 'best',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([text])
            
            if os.path.exists(file_path):
                await status_msg.edit_text("✅ Gönderiliyor...")
                await update.message.reply_video(video=open(file_path, 'rb'))
                await status_msg.delete()
            else:
                await status_msg.edit_text("❌ İndirilemedi veya kısıtlı içerik.")
                
        except Exception as e:
            await status_msg.edit_text(f"⚠️ Hata: {str(e)}")
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

if __name__ == '__main__':
    threading.Thread(target=run_web, daemon=True).start()
    app = ApplicationBuilder().token("8834173312:AAE253ZrgrQGvrKZ_qPwAmUWhd2t_GHGfW8").build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
