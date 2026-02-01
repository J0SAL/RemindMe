# 🧠 RemindMe Bot
> **An Intelligent Telegram Reminder Assistant powered by Google Gemini and Containerized Architecture.**

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0-black?style=for-the-badge&logo=flask&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Queue-red?style=for-the-badge&logo=redis&logoColor=white)
![Postgres](https://img.shields.io/badge/PostgreSQL-RDS-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-AI-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge&logo=docker&logoColor=white)

---

## 🏗️ Architecture

RemindMe uses a modern **Event-Driven Architecture** to ensure responsiveness and reliability. It is fully containerized and uses a split-service design.

```mermaid
graph TD
    User((User)) -->|Message| Telegram[Telegram Bot API]
    Telegram -->|Webhook| Ngrok[Ngrok Tunnel]
    Ngrok -->|POST /webhook| WebApp[Flask Web App]
    
    WebApp -->|Enqueue Task| Redis[(Redis Queue)]
    WebApp -->|Save/Read| DB[(PostgreSQL)]
    
    Worker[RQ Worker] -->|Dequeue Task| Redis
    Worker -->|Process NLU| Gemini[Google Gemini AI]
    Worker -->|Save Reminder| DB
    Worker -->|Send Reply| Telegram
    
    Scheduler[Scheduler Service] -->|Check Every 60s| DB
    Scheduler -->|Send Due Reminders| Telegram
```

## ✨ Features

-   **Natural Language Understanding**: Just say "Remind me to call Mom in 10 mins" and it understands.
-   **Asynchronous Processing**: Webhooks return instantly; AI processing happens in the background.
-   **Reliable Scheduling**: Dedicated scheduler service ensures reminders are sent on time.
-   **Cloud Database**: Persisted in AWS RDS (PostgreSQL).
-   **Containerized**: Redis and Services are ready for Docker deployment.

---

## 🚀 Getting Started

### Prerequisites

-   Python 3.10+
-   Docker (for Redis)
-   Ngrok (for local development)

### 1. Environment Setup

Create a `.env` file in the `backend/` directory:
```bash
TELEGRAM_BOT_TOKEN=your_token
GEMINI_API_KEY=your_key
POSTGRES_DB_URL=postgresql://user:pass@host:5432/db?sslmode=require
REDIS_URL=redis://localhost:6379
DEV_URL=https://your-ngrok-url.ngrok-free.app
```

### 2. Infrastructure (Redis)

Start the Redis container:
```bash
docker compose up -d
```

### 3. Run the Services

You need to run 3 separate terminals to simulate the microservices architecture:

**Terminal 1: Web Server** (Receives Messages)
```bash
source backend/venv/bin/activate
python3 backend/app.py
```

**Terminal 2: Worker** (Processes AI)
```bash
source backend/venv/bin/activate
python3 backend/worker.py
```

**Terminal 3: Scheduler** (Checks Time)
```bash
source backend/venv/bin/activate
python3 backend/scheduler.py
```

---

## ☁️ Legacy Cloud Infrastructure

This project initially used a serverless architecture with **AWS Lambda** (for the worker) and **Amazon EventBridge** (for scheduling).

While we migrated to a containerized `worker` and `scheduler` for portability, the original cloud-native code is preserved in the `aws/` directory for reference. It demonstrates how to implement:
-   **AWS Lambda**: Serverless execution of Python logic.
-   **EventBridge**: Cron-style triggers in the cloud.

## 🛠️ Tech Stack Details

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Brain** | Google Gemini 2.5 Flash | Fast, cost-effective NLU |
| **Orchestration** | LangChain | AI Logic & Prompt Management |
| **Backend** | Flask | Lightweight Webhook handler |
| **Queue** | Redis + RQ | Async task management |
| **Database** | PostgreSQL (AWS RDS) | Persistent storage |
| **Scheduler** | Python Schedule | Periodic checks (Cron replacement) |
