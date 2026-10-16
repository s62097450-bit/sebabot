import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = "8401131654:AAGSRPyOfQRrvvdHhmxnE-BW__-Izrr23v0"

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
