from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
load_dotenv()


# Load bot token and handle from environment variables
API_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
BOT_HANDLE = os.environ.get('TELEGRAM_BOT_HANDLE')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message when the /start command is issued."""
    await update.message.reply_text('Hello! I am your new Telegram bot.')

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echoes back any text message received."""
    await update.message.reply_text(f"You said: {update.message.text}")

def main():
    """Starts the bot."""
    if not API_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set.")
    application = Application.builder().token(API_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))

    # Start polling for updates
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()