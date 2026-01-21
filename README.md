### Ngrok
```
ngrok http 5001
```

Note: copy the url to .env


### Backend
```
# activate env
source backend/venv/bin/activate

# run app (telegram endpoint)
python3 app.py
```



### Postres DB on RDS
```
1. Open CloudShell
2. Run command `psql -h remindme.cc5g4i0islpz.us-east-1.rds.amazonaws.com -U postgres -d remindme`
3. Enter the password
```

### Tools and Tech used

1. Artificial Intelligence & Orchestration

    - Google Gemini (Generative AI): Used as the "brain" for Natural Language Understanding (NLU) to extract intents and entities from user messages.

    - LangChain: Orchestration framework used to chain the LLM with logic and memory.

    - LangChain ConversationBufferMemory: Implemented to provide the bot with "short-term memory," allowing it to handle multi-turn conversations and maintain context.

    - Prompt Engineering: Designed system prompts to ensure the AI correctly identifies dates, times, and tasks from casual human speech.

2. Backend & Communication
    - Python (Flask/FastAPI): Built a persistent backend server to handle incoming requests and business logic.

    - Telegram Bot API: Integrated via Webhooks for real-time, bi-directional communication with users.

    - Ngrok: Utilized for secure tunneling to expose the local development server to Telegram’s webhooks during the building phase.

3. Database & Storage
    - Amazon RDS (PostgreSQL): Deployed a managed relational database in the cloud for high availability and persistence.

    - pg8000: Selected a pure-Python PostgreSQL driver to ensure compatibility and performance within a serverless environment.

    - SQLAlchemy / SQL: Designed a relational schema to manage users, reminders, and status tracking (pending vs. sent).

4. Cloud Infrastructure & DevOps
    - AWS Lambda (Serverless): Implemented a serverless "Worker" to execute the notification logic independently of the main server.

    - Amazon EventBridge (Cloud Cron): Configured a recurring 1-minute schedule to trigger the Lambda function, ensuring high-precision delivery of reminders.

    - AWS CloudShell: Used for cloud-native CLI management, building Lambda Layers, and direct database manipulation.

    - Cross-Timezone Logic: Solved complex UTC-to-IST synchronization issues to ensure reminders fire at the correct local time.
