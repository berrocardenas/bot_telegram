from telegram.ext import Application
from dotenv import load_dotenv
import os
import asyncio
import sys
from handlers import start, acceso  # Importar handlers

load_dotenv()

async def main():
    app = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    
    # Registra tus handlers aquí
    from handlers import start, acceso
    app.add_handler(start.handler)
    app.add_handler(acceso.handler)
    
    print("🤖 Bot iniciado. Presiona Ctrl+C para detener...")
    
    # Solución mejorada para polling
    await app.initialize()
    await app.start()
    try:
        await app.updater.start_polling()
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, asyncio.CancelledError):
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

if __name__ == "__main__":
    # Configuración especial para Windows
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot detenido correctamente")