from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Reminder(db.Model):
    __tablename__ = "reminders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), index=True, nullable=False)
    chat_id = db.Column(db.String(128), index=True, nullable=True)
    status = db.Column(db.String(32), nullable=False)
    task = db.Column(db.String(1024), nullable=True)
    trigger_time = db.Column(db.DateTime, nullable=True)
    reply = db.Column(db.String(1024), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    processed = db.Column(db.Boolean, default=False)