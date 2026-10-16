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
            info = ydl.extract_info(url, download=True)
            
            raw_uploader = info.get('uploader') or info.get('uploader_id') or info.get('channel') or 'Instagram'
            raw_caption = info.get('description') or info.get('title') or ''
            
            uploader = html.escape(str(raw_uploader))
            caption_text = html.escape(str(raw_caption))
            
            upload_date_str = info.get('upload_date')
            if upload_date_str:
                try:
                    formatted_date = datetime.strptime(str(upload_date_str), '%Y%m%d').strftime('%d %B %Y')
                except Exception:
                    formatted_date = str(upload_date_str)
            else:
                formatted_date = datetime.now().strftime('%d %B %Y')

            like_count = info.get('like_count') if info.get('like_count') is not None else 0
            comment_count = info.get('comment_count') if info.get('comment_count') is not None else 0

            # Şablon Formatı
            custom_caption = (
                f"📷 <b>{uploader}</b>  🗓 <b>{formatted_date}</b>\n\n"
                f"{caption_text}\n\n"
                f"❤️ {like_count}  💬 {comment_count}\n\n"
                f"⚡️ <a href=\"https://t.me/sebadownloaderbot\">Seba Downloader</a>"
            )

