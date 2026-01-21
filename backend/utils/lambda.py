import os
import json
import pg8000.native
import urllib.request

def get_db_connection():
    return pg8000.native.Connection(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        port=5432
    )

def send_telegram(chat_id, message):
    token = os.environ['TELEGRAM_BOT_TOKEN']
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = json.dumps({"chat_id": chat_id, "text": message}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as response:
        return response.read()

def lambda_handler(event, context):
    db = get_db_connection()
    
    # Get reminders where trigger_time is now or in the past, and processed is false
    query = """
        SELECT id, user_id, task
        FROM reminders
        WHERE trigger_time <= (NOW() AT TIME ZONE 'Asia/Kolkata')
        AND processed = false;
    """
    
    for row in db.run(query):
        rem_id, user_id, task = row
        text = f"⏰ REMINDER: {task}"
        
        try:
            send_telegram(user_id, text)
            db.run("UPDATE reminders SET processed = true WHERE id = :id", id=rem_id)

        except Exception as e:
            print(f"Error sending reminder {rem_id}: {e}")
    
    db.close()
    
    return {"statusCode": 200}