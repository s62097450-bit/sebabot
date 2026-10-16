import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

logging.basicConfig(level=logging.INFO)

TOKEN = "8742438265:AAHNoTC1FzNBf3Nd151L7ChYRJxC5D--JLI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Bana indirmek istediğin video linkini gönder (Instagram, YouTube, TikTok vb.).")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"):
        return

    status_msg = await update.message.reply_text("⏳ Video indiriliyor, lütfen bekleyin...")
    file_path = "downloaded_video.mp4"

    ydl_opts = {
        'format': 'best',
        'outtmpl': file_path,
        'max_filesize': 50 * 1024 * 1024,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await status_msg.edit_text("📤 Video Telegram'a yükleniyor...")
        with open(file_path, 'rb') as video:
            await update.message.reply_video(video=video)

        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"❌ Bir hata oluştu veya video boyutu 50MB'tan büyük: {e}")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("Bot çalışıyor...")
    app.run_polling()

if __name__ == '__main__':
    main()
