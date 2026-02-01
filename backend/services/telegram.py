import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    """
    Send a message to a Telegram chat.
    Args:
        chat_id (int): The chat ID to send the message to.
        text (str): The message text to send.
    """
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending message: {e}")

def set_webhook(url):
    """
    Set the webhook URL for the Telegram bot.
    Args:
        url (str): The public URL to set as the webhook.
    Returns:
        dict: The response from the Telegram API.
    """
    webhook_url = f"{url}/webhook"
    try:
        res = requests.get(f"{TELEGRAM_API}/setWebhook?url={webhook_url}")
        return res.json()
    except Exception as e:
        print(f"Error setting webhook: {e}")
        return {"ok": False, "description": str(e)}
