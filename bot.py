import os
import logging
import html
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
            # Video bilgilerini çek
            info = ydl.extract_info(url, download=True)
            
            # Kullanıcı adı ve Açıklamayı güvenli şekilde al
            raw_uploader = info.get('uploader') or info.get('uploader_id') or 'Instagram'
            raw_caption = info.get('description') or info.get('title') or ''
            
            uploader = html.escape(str(raw_uploader))
            caption_text = html.escape(str(raw_caption))
            
            # Tarih
            formatted_date = datetime.now().strftime('%d %B %Y')

            # Şablon Metni (Çökmeye neden olan riskli sayaçlar temizlendi)
            custom_caption = (
                f"📷 <b>{uploader}</b>  🗓 <b>{formatted_date}</b>\n\n"
                f"{caption_text}\n\n"
                f"⚡️ <a href=\"https://t.me/sebadownloaderbot\">Seba Downloader</a>"
            )

            if len(custom_caption) > 1000:
                custom_caption = custom_caption[:990] + "..."

        await status_msg.edit_text("📤 Video Telegram'a yükleniyor...")

        # Videoyu açıklama ile birlikte atıyoruz
        with open(file_path, 'rb') as video:
            await message.reply_video(
                video=video,
                caption=custom_caption,
                parse_mode="HTML"
            )

        await status_msg.delete()

    except Exception as e:
        # Eğer videonun altına metin eklerken yine Telegram sınırı aşılırsa sadece videoyu ve ayrı mesajı at
        print(f"Hata detayı: {e}")
        try:
            with open(file_path, 'rb') as video:
                await message.reply_video(video=video)
            await message.reply_text(
                text=f"📷 <b>{uploader}</b>\n\n{caption_text}\n\n⚡️ <a href=\"https://t.me/sebadownloaderbot\">Seba Downloader</a>",
                parse_mode="HTML",
                disable_web_page_preview=True
            )
            await status_msg.delete()
        except Exception as inner_error:
            await status_msg.edit_text("❌ Video indirilemedi. (Boyut 50MB'tan büyük olabilir veya site engeli)")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_
