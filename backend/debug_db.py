from app import app
from services.database import db
from sqlalchemy import text

with app.app_context():
    result = db.session.execute(text("SELECT id, task, trigger_time, status, processed FROM reminders ORDER BY id DESC"))
    rows = result.fetchall()
    print(f"Found {len(rows)} reminders:")
    for row in rows:
        print(f"ID: {row.id} | Task: {row.task} | Time: {row.trigger_time} | Status: {row.status} | Processed: {row.processed}")
