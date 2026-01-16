import os
import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 1. Setup the Model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", # Use Flash for speed in bots
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

# 2. In-memory store for session history (Swap with Redis later!)
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 3. Enhanced Prompt with History Placeholder
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a scheduling assistant. Today is {current_time}."),
    MessagesPlaceholder(variable_name="chat_history"), # This is where memory lives
    ("human", """Parse the following user message into a JSON reminder format.
    
    Return ONLY JSON:
    - status: "COMPLETE" or "MISSING_TIME" or "MISSING_TASK"
    - task: The thing to do.
    - trigger_time: ISO timestamp (YYYY-MM-DD HH:MM:SS)
    - reply: A brief confirmation or a clarifying question.
    
    User message: {user_input}""")
])

# 4. The Chain
chain = prompt.pipe(llm).pipe(JsonOutputParser())

# 5. Wrap with Message History
# This version handles history automatically based on a session_id
with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="user_input",
    history_messages_key="chat_history",
    output_messages_key="reply"
)

def parse_intent_with_ai(user_id, user_message):
    current_time = datetime.datetime.now().strftime("%A, %Y-%m-%d %H:%M:%S")
    
    config = {"configurable": {"session_id": str(user_id)}}
    
    try:
        result = with_message_history.invoke(
            {"user_input": user_message, "current_time": current_time},
            config=config
        )
        return result
    except Exception as e:
        print(f"AI Error: {e}")
        return None

# Example usage:
# response = parse_intent_with_ai(12345, "Remind me to call John")
# print(response)