import logging
import os
import threading
import yt_dlp
from flask import Flask
from telegram import Update, ReactionTypeEmoji
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot Online", 200

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

logging.basicConfig(level=logging.INFO)

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE, query, mode):
    # 1. Tepkiyi manuel gönder (hata alırsak try-except ile sessizce geç)
    try:
        await update.message.set_reaction(reaction=[ReactionTypeEmoji(emoji="👁️")])
    except Exception:
        pass 

    file_path = "/tmp/media.mp4" if mode == "video" else "/tmp/media.mp3"
    
    try:
        # YouTube arama engellerini aşmak için ek parametreler
        ydl_opts = {
            'outtmpl': file_path,
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'cookiefile': 'cookies.txt',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'extractor_args': {'youtube': {'player_client': ['android']}}, # ÖNEMLİ: Mobil client taklidi
        }
        
        if mode == "audio":
            ydl_opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}], 'default_search': 'ytsearch1:'})
        else:
            ydl_opts.update({'format': 'best[ext=mp4]/best', 'default_search': 'ytsearch1:'})
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            # Eğer arama sonucu döndüyse ilkini al
            if 'entries' in info:
                video = info['entries'][0]
            else:
                video = info
            
            final_path = ydl.prepare_filename(video)
            # Eğer dosya ismi uzantı değişmişse (mp3 ise) onu yakala
            if mode == "audio":
                final_path = final_path.rsplit('.', 1)[0] + '.mp3'
            
        if os.path.exists(final_path):
            if mode == "audio":
                await update.message.reply_audio(audio=open(final_path, 'rb'))
            else:
                await update.message.reply_video(video=open(final_path, 'rb'))
            os.remove(final_path)
        else:
            await update.message.reply_text("Üzgünüm, YouTube bu aramayı engelledi.")
            
    except Exception as e:
        await update.message.reply_text(f"Hata oluştu: {str(e)}")

async def start(update, context):
    await update.message.reply_text("Seba Downloader aktif!")

async def arama_video(update, context):
    query = " ".join(context.args)
    if not query: return
    await download_media(update, context, query, "video")

async def indir_sarki(update, context):
    query = " ".join(context.args)
    if not query: return
    await download_media(update, context, query, "audio")

if __name__ == '__main__':
    threading.Thread(target=run_web, daemon=True).start()
    app = ApplicationBuilder().token("8834173312:AAE253ZrgrQGvrKZ_qPwAmUWhd2t_GHGfW8").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", arama_video))
    app.add_handler(CommandHandler("indir", indir_sarki))
    app.run_polling()
