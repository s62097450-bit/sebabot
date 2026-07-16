import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Seba Downloader hazır! Linklerini bekliyorum.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if not text or "http" not in text:
        return 

    # Sadece link içeren mesajlarda işlem başlatır
    await update.message.reply_text("Video indiriliyor, lütfen bekle... ⏳")
    
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
            'max_filesize': 50 * 1024 * 1024,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([text])
            
        await update.message.reply_video(video=open('video.mp4', 'rb'))
        os.remove('video.mp4')
        
    except Exception as e:
        # Hata durumunda sadece log basar, kullanıcıya mesaj atmaz
        print(f"HATA: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token("8834173312:AAE253ZrgrQGvrKZ_qPwAmUWhd2t_GHGfW8").build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.run_polling()
