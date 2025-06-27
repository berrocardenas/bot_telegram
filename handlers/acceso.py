from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
from services.hotmart_service import HotmartService
import os
from datetime import datetime
from utils.logger import logger

# Estados de la conversación
EMAIL_INPUT = 1

hotmart_service = HotmartService()

async def start_acceso(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inicia el proceso de validación pidiendo el email"""
    await update.message.reply_text(
        "📩 Por favor, ingresa el correo electrónico con el que compraste el curso:"
    )
    return EMAIL_INPUT

async def verify_access(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Verifica el acceso con Hotmart"""
    user_email = update.message.text.strip()
    logger.info(f"Validando acceso para: {user_email}")
    
    try:
        result = hotmart_service.get_user_status(user_email)
        
        if result["active"]:
            await update.message.reply_text(
                f"{result['message']}\n\n"
                f"✅ Únete al grupo privado: {os.getenv('GROUP_LINK')}"
            )
        else:
            await update.message.reply_text(
                f"{result['message']}\n\n"
                f"🔒 Para acceder, compra aquí: {os.getenv('CHECKOUT_URL')}"
            )
            
    except Exception as e:
        logger.error(f"Error en validación Hotmart: {e}")
        await update.message.reply_text(
            "⚠️ Ocurrió un error al validar tu acceso. Por favor intenta más tarde."
        )
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela el proceso"""
    await update.message.reply_text("❌ Operación cancelada")
    return ConversationHandler.END

# Handler de conversación
acceso_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("acceso", start_acceso)],
    states={
        EMAIL_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, verify_access)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

# Handler tradicional (opcional, si quieres mantener ambas formas)
async def acceso_directo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Versión simplificada sin conversación"""
    await update.message.reply_text(
        "⚠️ Por favor usa el comando /acceso y sigue el proceso interactivo.\n"
        "O envía tu correo directamente después del comando: /acceso tu@email.com"
    )

direct_handler = CommandHandler("acceso", acceso_directo)