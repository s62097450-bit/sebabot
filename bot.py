async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Sadece içinde "http" geçen mesajları işle, gerisini görmezden gel
    if not text or "http" not in text:
        return 

    # Link varsa aşağısı çalışmaya devam edecek
    status_msg = await update.message.reply_text("Video indiriliyor... ⏳")
    
    file_path = 'video.mp4'
    try:
        ydl_opts = {
            'format': 'best[filesize<50M]',
            'outtmpl': file_path,
            'no_cache': True,
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([text])
            
        if os.path.exists(file_path):
            await update.message.reply_video(video=open(file_path, 'rb'))
            
    except Exception as e:
        print(f"HATA: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        try:
            await status_msg.delete()
        except:
            pass
