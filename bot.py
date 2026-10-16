import os
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

logging.basicConfig(level=logging.INFO)

TOKEN = "8742438265:AAHNoTC1FzNBf3Nd151L7ChYRJxC5D--JLI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot çalışıyor")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    url = message.text.strip()
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
            # Önce video bilgilerini (metadata) çekiyoruz
            info = ydl.extract_info(url, download=True)
            
            # Bilgileri değişkenlere atıyoruz
            uploader = info.get('uploader') or info.get('uploader_id') or 'Bilinmiyor'
            caption_text = info.get('description') or ''
            
            # Tarih formatlama
            upload_date_str = info.get('upload_date')
            if upload_date_str:
                try:
                    formatted_date = datetime.strptime(upload_date_str, '%Y%m%d').strftime('%d %B %Y')
                except Exception:
                    formatted_date = upload_date_str
            else:
                formatted_date = "Bilinmiyor"

            like_count = info.get('like_count') or 0
            comment_count = info.get('comment_count') or 0

            # İstediğin şablon formatı
            custom_caption = (
                f"📷{uploader} 🗓{formatted_date}\n"
                f"{caption_text}\n"
                f"❤️{like_count} 💬{comment_count}\n"
                f"⚡️reLynth | Downloader & Checker"
            )

            # Telegram yazı sınırı (1024 karakter) kontrolü
            if len(custom_caption) > 1000:
                custom_caption = custom_caption[:995] + "..."

        await status_msg.edit_text("📤 Video Telegram'a yükleniyor...")

        with open(file_path, 'rb') as video:
            await message.reply_video(
                video=video,
                caption=custom_caption
            )

        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text("❌ Video indirilemedi. (Boyut 50MB'tan büyük olabilir veya site engeli)")
        print(f"Hata detayı: {e}")

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
