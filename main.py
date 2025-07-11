from telegram.ext import ApplicationBuilder
from handlers.router import router_handler  # punto de entrada único

BOT_TOKEN = "7252307465:AAFJ5zQfGcPMG-DSCtEfhLvytPl2k7p6xvY"

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(router_handler)

    print("🤖 Bot iniciado")
    app.run_polling()

if __name__ == "__main__":
    main()