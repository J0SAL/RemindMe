import time
import schedule
from app import app
from services.scheduler_service import check_due_reminders
from dotenv import load_dotenv

load_dotenv()

def job():
    with app.app_context():
        check_due_reminders()

# Run every 60 seconds
schedule.every(60).seconds.do(job)

if __name__ == "__main__":
    print("Scheduler started... Running every 60s.")
    # Run once immediately on start
    job()
    
    while True:
        schedule.run_pending()
        time.sleep(1)
