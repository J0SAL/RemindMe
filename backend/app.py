"""
This module provides the backend application for a Telegram bot.
"""
import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Handle incoming webhook requests from Telegram.

    Returns:
        A JSON response indicating success.
    """
    data = request.get_json()
    
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        send_message(chat_id, f"You Said: {text}")

    return jsonify({"status": "success"}), 200

def send_message(chat_id, text):
    """
    Send a message to a Telegram chat.
    Args:
        chat_id (int): The chat ID to send the message to.
        text (str): The message text to send.
    """
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def set_webhook(url):
    """
    Set the webhook URL for the Telegram bot.
    Args:
        url (str): The public URL to set as the webhook.
    Returns:
        dict: The response from the Telegram API.
    """
    webhook_url = f"{url}/webhook"
    res = requests.get(f"{TELEGRAM_API}/setWebhook?url={webhook_url}")
    return res.json()

if __name__ == "__main__":
    """
    Set the webhook and run the Flask app.
    """
    public_url = os.getenv("DEV_URL")
    if public_url:
        print(f"Setting webhook to: {public_url}")
        set_webhook(public_url)
    
    app.run(port=5001, debug=True)