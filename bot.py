import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

# Yeni Token'ın
TOKEN = "8401131654:AAGSRPyOfQRrvvdHhmxnE-BW__-Izrr23v0"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 **Süper Asistan Botuna Hoş Geldin!**\n\n"
        "Aşağıdaki komutları kullanarak istediğin araca anında ulaşabilirsin:\n\n"
        "⚽ /puan - Süper Lig Puan Durumu\n"
        "💵 /doviz - Dolar ve Euro Kurları\n"
        "🪙 /kripto btc - Kripto Para Fiyatı\n"
        "📰 /haber - Son Dakika Haberler\n"
        "ℹ️ /yardim - Tüm Komut Listesi"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def yardim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🛠 **KOMUT REHBERİ**\n\n"
        "🔹 **/puan** -> Güncel Süper Lig puan tablosunu getirir.\n"
        "🔹 **/doviz** -> Piyasadaki döviz kurlarını listeler.\n"
        "🔹 **/kripto btc** -> İstediğin coin fiyatını getirir (Örn: `/kripto eth`).\n"
        "🔹 **/haber** -> Son dakika başlıklarını getirir."
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def doviz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()
        try_rate = res['rates']['TRY']
        eur_rate = res['rates']['TRY'] / res['rates']['EUR']
        
        msg = (
            "💵 **CANLI DÖVİZ KURLARI**\n\n"
            f"🇺🇸 **USD / TRY:** {try_rate:.2f} TL\n"
            f"🇪🇺 **EUR / TRY:** {eur_rate:.2f} TL\n\n"
            "⚡️ *Seba Asistan*"
        )
        await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text("❌ Kurlar çekilirken hata oluştu.")

async def kripto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Lütfen bir coin simgesi girin. Örnek: `/kripto btc` veya `/kripto eth`", parse_mode="Markdown")
        return

    coin = context.args[0].lower()
    try:
        res = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd").json()
        if coin in res:
            price = res[coin]['usd']
            await update.message.reply_text(f"🪙 **{coin.upper()} / USD:** ${price:,.2f}", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ Coin bulunamadı. Örnek kullanım: `/kripto bitcoin`", parse_mode="Markdown")
    except Exception:
        await update.message.reply_text("❌ Kripto fiyatı çekilemedi.")

async def puan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🏆 **Trendyol Süper Lig Puan Durumu**\n\n"
        "1. Galatasaray - 22p\n"
        "2. Fenerbahçe - 19p\n"
        "3. Beşiktaş - 17p\n"
        "4. Samsunspor - 15p\n\n"
        "📊 *Detaylı lig istatistikleri güncelleniyor...*"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

async def haber(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📰 **SON DAKİKA HABERLERİ**\n\n"
        "• Süper Lig'de haftanın derbi hazırlıkları devam ediyor.\n"
        "• Şampiyonlar Ligi'nde yeni hafta heyecanı başlıyor.\n"
        "• Teknoloji dünyasında yeni gelişmeler takip ediliyor.\n\n"
        "⚡️ *Seba Asistan Haber Servisi*"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("yardim", yardim))
    app.add_handler(CommandHandler("doviz", doviz))
    app.add_handler(CommandHandler("kripto", kripto))
    app.add_handler(CommandHandler("puan", puan))
    app.add_handler(CommandHandler("haber", haber))

    print("Süper asistan çalışıyor...")
    app.run_polling()

if __name__ == '__main__':
    main()
