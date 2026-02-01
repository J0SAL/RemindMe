from services.ai import parse_intent_with_ai
from services.reminders import save_reminder
from services.telegram import send_message

def process_message(chat_id, user_id, text):
    """
    Process the user message in the background.
    """
    # Local import to avoid circular dependency
    from app import app
    
    print(f"Processing message {text}")

    with app.app_context():
        try:
            ai_result = parse_intent_with_ai(user_id, text)
            print(f"AI Result: {ai_result}")
            
            if ai_result:
                response = ai_result.get("reply", "Got it!")
                send_message(chat_id, response)

                if ai_result.get("status") == "COMPLETE":
                    save_reminder(chat_id, user_id, ai_result)
                    print(f"Saved reminder for {user_id}")
                
        except Exception as e:
            print(f"Error processing message: {e}")
            send_message(chat_id, "Sorry, I encountered an error processing your request.")
