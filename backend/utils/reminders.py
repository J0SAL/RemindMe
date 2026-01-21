from utils.models import Reminder, db
from datetime import datetime

def save_reminder(chat_id, user_id, ai_result):
    trigger_time_raw = ai_result.get("trigger_time")
    trigger_dt = datetime.strptime(trigger_time_raw, "%Y-%m-%d %H:%M:%S")


    reminder = Reminder(
        user_id=str(user_id),
        chat_id=str(chat_id),
        status=ai_result.get("status", "COMPLETE"),
        task=ai_result.get("task"),
        trigger_time=trigger_dt,
        reply=ai_result.get("reply")
    )

    try:
        db.session.add(reminder)
        db.session.commit()
        print(f"Reminder saved: {reminder}")
    except Exception as e:
        db.session.rollback()
        print(f"Error saving reminder: {e}")