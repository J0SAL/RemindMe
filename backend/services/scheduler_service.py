from datetime import datetime, timezone, timedelta
from services.database import db
from services.telegram import send_message
from sqlalchemy import text

def check_due_reminders():
    """
    Check for due reminders in the database and send them using Telegram.
    Updates the reminder status to processed.
    """
    print("Checking for due reminders...")
    
    # Current time in UTC (Assuming DB stores times, ideally use UTC)
    # The original lambda used 'Asia/Kolkata', we should stick to what the user expects
    # For now, let's use the DB's NOW() logic to be consistent with the original query
    
    query = text("""
        SELECT id, user_id, task, trigger_time
        FROM reminders
        WHERE trigger_time <= (NOW() AT TIME ZONE 'Asia/Kolkata')
        AND processed = false;
    """)

    try:
        # Execute query
        result = db.session.execute(query)
        rows = result.fetchall()
        
        if not rows:
            print("No due reminders.")
            return

        for row in rows:
            rem_id, user_id, task, trigger_time = row
            text_msg = f"⏰ REMINDER: {task}"
            
            print(f"Sending reminder {rem_id} to {user_id}")
            
            try:
                # Send Message
                send_message(user_id, text_msg)
                
                # Update processed status
                update_query = text("UPDATE reminders SET processed = true WHERE id = :id")
                db.session.execute(update_query, {"id": rem_id})
                db.session.commit()
                print(f"Reminder {rem_id} processed.")

            except Exception as e:
                db.session.rollback()
                print(f"Error checking/sending reminder {rem_id}: {e}")
                
    except Exception as e:
        print(f"Scheduler Error: {e}")
