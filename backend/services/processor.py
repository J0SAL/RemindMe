from services.ai import parse_intent_with_ai
from services.reminders import save_reminder
from services.telegram import send_message

def process_message(chat_id, user_id, text):
    """
    Process the user message in the background.
    """
    print(f"Processing message from {user_id}: {text}")
    
    try:
        ai_result = parse_intent_with_ai(user_id, text)
        print(f"AI Result: {ai_result}")
        
        if ai_result:
            response = ai_result.get("reply", "Got it!")
            send_message(chat_id, response)

            if ai_result.get("status") == "COMPLETE":
                # Note: This might need an app context if using Flask-SQLAlchemy directly,
                # but let's see if it works since save_reminder uses db.session
                save_reminder(chat_id, user_id, ai_result)
            
            print(f"To Schedule: {ai_result.get('task')} at {ai_result.get('trigger_time')}")
        else:
            send_message(chat_id, "Sorry, I couldn't understand that.")
            
    except Exception as e:
        print(f"Error processing message: {e}")
        send_message(chat_id, "Sorry, I encountered an error processing your request.")
