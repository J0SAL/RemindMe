"""
This module provides the backend application for a Telegram bot.
"""
import os
from dotenv import load_dotenv

# Load env before importing services that might use it
load_dotenv()

from flask import Flask, request, jsonify
from services.ai import parse_intent_with_ai
from services.reminders import save_reminder
from services.database import db
from services.telegram import send_message, set_webhook

app = Flask(__name__)
DATABASE_URL = os.getenv("POSTGRES_DB_URL")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()

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
        print(f"AI Result: {ai_result}")
        if ai_result:
            response = ai_result.get("reply", "Got it!")
            send_message(chat_id, response)

            if ai_result.get("status") == "COMPLETE":
                save_reminder(chat_id, user_id, ai_result)
            
            print(f"To Schedule: {ai_result.get('task')} at {ai_result.get('trigger_time')}")
        else:
            send_message(chat_id, "Sorry, I couldn't understand that.")

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    """
    Set the webhook and run the Flask app.
    """
    print("Setting up webhook...")
    public_url = os.getenv("DEV_URL")
    if public_url:
        print(f"Setting webhook to: {public_url}")
        set_webhook(public_url)
    
    app.run(port=5001, debug=True)