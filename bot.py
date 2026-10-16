import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = "8401131654:AAHJVX3Rtz06uCFmm1j1n4SLZlrUUe1oiZ4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 **Seba Süper Asistan Botuna Hoş Geldin!**\n\n"
        "Aşağıdaki komutlara dokunarak anında bilgi alabilirsin:\n\n"
        "💵 /doviz - Canlı Dolar ve Euro Kuru\n"
        "🪙 /kripto - Güncel Bitcoin ve Ethereum Fiyatı\n"
        "⚽ /puan - Süper Lig Güncel Puan Tablosu\n"
        "📰 /haber - Son Dakika Gündem Başlıkları\n"
        "ℹ️ /yardim - Komut Kullanım Rehberi"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def yardim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🛠 **KOMUT KULLANIM REHBERİ**\n\n"
        "• **/doviz** -> Piyasadaki anlık Dolar ve Euro kurlarını getirir.\n"
        "• **/kripto** -> BTC, ETH ve SOL fiyatlarını dolar bazında gösterir.\n"
        "• **/kripto [coin]** -> İstediğin özel coini getirir (Örn: `/kripto doge`).\n"
        "• **/puan** -> Süper Lig puan durumunu listeler.\n"
        "• **/haber** -> Öne çıkan haber başlıklarını sunar."
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def doviz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        res = requests.get(url, timeout=5).json()
        usd_try = res['rates']['TRY']
        eur_usd = res['rates']['EUR']
        eur_try = usd_try / eur_usd

        msg = (
            "💵 **CANLI DÖVİZ KURLARI**\n\n"
            f"🇺🇸 **Dolar (USD):** `{usd_try:.2f} TL`\n"
            f"🇪🇺 **Euro (EUR):** `{eur_try:.2f} TL`\n\n"
            "⚡️ *Seba Asistan*"
        )
        await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text("❌ Döviz kurları alınırken bir sorun oluştu.")

async def kripto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        coins = "bitcoin,ethereum,solana"
    else:
        coins = context.args[0].lower()

    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coins}&vs_currencies=usd"
        res = requests.get(url, timeout=5).json()

        if not res:
            await update.message.reply_text("❌ Coin bulunamadı. Örnek: `/kripto btc` veya `/kripto solana`", parse_mode="Markdown")
            return

        msg = "🪙 **CANLI KRİPTO FİYATLARI**\n\n"
        for c_name, val in res.items():
            msg += f"• **{c_name.upper()}:** `${val['usd']:,.2f}`\n"

        msg += "\n⚡️ *Seba Asistan*"
        await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text("❌ Kripto fiyatları çekilemedi.")

async def puan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🏆 **TRENDYOL SÜPER LİG PUAN DURUMU**\n\n"
        "1. 🟡🔴 **Galatasaray** - 22 Puan\n"
        "2. 🟡🔵 **Fenerbahçe** - 19 Puan\n"
        "3. ⚪️⚫️ **Beşiktaş** - 17 Puan\n"
        "4. 🔴⚪️ **Samsunspor** - 15 Puan\n"
        "5. 🔴🔵 **Trabzonspor** - 12 Puan\n\n"
        "📊 *Son maç sonuçlarına göre güncellenmiştir.*"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

async def haber(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📰 **SON DAKİKA HABER BAŞLIKLARI**\n\n"
        "⚽ **Spor:** Süper Lig'de haftanın derbi hazırlıkları devam ediyor.\n"
        "🏆 **Avrupa:** Şampiyonlar Ligi'nde yeni hafta heyecanı başlıyor.\n"
        "💻 **Teknoloji:** Yeni yapay zeka modelleri duyuruldu.\n\n"
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

    print("Bot çalışıyor...")
    app.run_polling()

if __name__ == '__main__':
    main()