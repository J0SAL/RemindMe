import os
import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# 1. Setup the Model
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview", 
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

def parse_intent_with_ai(user_message):
    """Parse user message into a structured reminder using AI.
    Args:
        user_message (str): The user's input message.
    Returns:
        dict: Parsed reminder with status, task, trigger_time, and reply.
    """
    current_time = datetime.datetime.now().strftime("%A, %Y-%m-%d %H:%M:%S")
    
    # 2. Define a clean Prompt Template
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are a scheduling assistant. Today is {current_time}."),
        ("human", """Parse the following user message into a JSON reminder format.
        
        Return ONLY JSON with these fields:
        - status: "COMPLETE" if you have task and time, "MISSING_TIME" if time is vague.
        - task: The thing to do.
        - trigger_time: ISO timestamp (YYYY-MM-DD HH:MM:SS) calculated from the user's relative time.
        - reply: A brief confirmation message.

        User message: {user_input}""")
    ])

    # 3. Build the "Chain" using .pipe()
    chain = prompt.pipe(llm).pipe(JsonOutputParser())

    try:
        # 4. Invoke the chain
        result = chain.invoke({"user_input": user_message})
        return result
    except Exception as e:
        print(f"AI Error: {e}")
        return None

# Example usage 
# parse_intent_with_ai("Remind me to buy milk tomorrow")