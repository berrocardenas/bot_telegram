from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from services.hotmart_service import verify_hotmart_user
import os

async def acceso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_email = "correo@usuario.com"  # Obtener esto de un mensaje previo
    is_buyer = await verify_hotmart_user(user_email)
    
    if is_buyer:
        await update.message.reply_text(f"✅ Únete al grupo: {os.getenv('GROUP_LINK')}")
    else:
        await update.message.reply_text(f"🔒 Compra aquí: {os.getenv('CHECKOUT_URL')}")

handler = CommandHandler("acceso", acceso)

