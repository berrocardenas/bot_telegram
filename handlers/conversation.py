from handlers.acceso import AccesoHandler
from telegram.ext import ConversationHandler

# Estados
EMAIL_INPUT = 1

conversation_handler = ConversationHandler(
    entry_points=[...],  # Tus comandos de inicio (ej: /start)
    states={
        EMAIL_INPUT: [
            MessageHandler(Filters.text & ~Filters.command, AccesoHandler.handle_email_input)
        ],
    },
    fallbacks=[...],  # Comandos de cancelación
)