import logging
import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp

# Flask sunucusu (Render'ın botu ayakta tutması için)
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot aktif!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

# Logging ayarı
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Seba Downloader aktif! Link gönder.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Sadece linkleri işle, diğer mesajları görmezden gel
    if not text or "http" not in text:
        return 

    status_msg = await update.message.reply_text("İndiriliyor... ⏳")
    
    # /tmp klasörü Render'da yazma izni olan tek yerdir
    file_path = "/tmp/video.mp4"
    
    try:
        ydl_opts = {
            'format': 'best[filesize<45M]', 
            'outtmpl': file_path,
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([text])
            
        if os.path.exists(file_path):
            await update.message.reply_video(video=open(file_path, 'rb'))
        else:
            await update.message.reply_text("Video indirilemedi veya boyut sınırı aşıldı.")
            
    except Exception as e:
        await update.message.reply_text(f"Hata: {str(e)}")
    finally:
        # İşlem bitince dosyayı temizle
        if os.path.exists(file_path):
            os.remove(file_path)
        try:
            await status_msg.delete()
        except:
            pass

if __name__ == '__main__':
    # Web sunucusunu başlat
    threading.Thread(target=run_web, daemon=True).start()
    
    # Botu başlat
    app = ApplicationBuilder().token("8834173312:AAE253ZrgrQGvrKZ_qPwAmUWhd2t_GHGfW8").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
