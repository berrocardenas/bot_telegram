from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Usa /acceso para verificar tu compra.")

# Esta es la variable que main.py espera encontrar:
handler = CommandHandler('start', start_command)