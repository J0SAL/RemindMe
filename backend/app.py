import os
from dotenv import load_dotenv

# Load env before importing services that might use it
load_dotenv()

from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue
from services.database import db
from services.telegram import send_message, set_webhook
from services.processor import process_message

app = Flask(__name__)
DATABASE_URL = os.getenv("POSTGRES_DB_URL")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Setup Redis Queue
conn = Redis.from_url(REDIS_URL)
q = Queue(connection=conn)

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

        print(f"Enqueuing message from {user_id}")
        q.enqueue(process_message, chat_id, user_id, text)

    return jsonify({"status": "queued"}), 200

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