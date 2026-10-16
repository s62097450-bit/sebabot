import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

logging.basicConfig(level=logging.INFO)

TOKEN = "8742438265:AAHNoTC1FzNBf3Nd151L7ChYRJxC5D--JLI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Bana indirmek istediğin video linkini gönder (Özelde veya gruplarda kullanabilirsin).")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    url = message.text
    if not url.startswith("http"):
        return

    status_msg = await message.reply_text("⏳ Video işleniyor, lütfen bekleyin...")
    file_path = "downloaded_video.mp4"

    ydl_opts = {
        'format': 'best',
        'outtmpl': file_path,
        'max_filesize': 50 * 1024 * 1024,
        'quiet': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await status_msg.edit_text("📤 Video Telegram'a yükleniyor...")
        with open(file_path, 'rb') as video:
            await message.reply_video(
                video=video,
                caption="@sebadownloaderbot"
            )

        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"❌ Video indirilemedi. (Boyut 50MB'tan büyük olabilir veya site engeli)")
        print(f"Hata detayı: {e}")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # Hem özel sohbetleri hem de grup mesajlarını yakalaması için filtre güncellendi
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("Bot çalışıyor...")
    app.run_polling()

if __name__ == '__main__':
    main()
