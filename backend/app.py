"""
This module provides the backend application for a Telegram bot.
"""
import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from utils.ai_model import parse_intent_with_ai

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
        user_id = data["message"]["from"]["id"]
        text = data["message"].get("text", "")

        ai_result = parse_intent_with_ai(user_id, text)
        if ai_result:
            response = ai_result.get("reply", "Got it!")
            send_message(chat_id, response)
            # TODO: DB + reminder scheduling logic goes here
            print(f"To Schedule: {ai_result.get('task')} at {ai_result.get('trigger_time')}")
        else:
            send_message(chat_id, "Sorry, I couldn't understand that.")

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