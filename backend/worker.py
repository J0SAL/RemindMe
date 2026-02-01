import os
from redis import Redis
from rq import Worker, Queue
from app import app
from dotenv import load_dotenv

load_dotenv()

listen = ['default']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

conn = Redis.from_url(redis_url)

if __name__ == '__main__':
    with app.app_context():
        # Instantiate worker with explicit connection
        queues = [Queue(name, connection=conn) for name in listen]
        worker = Worker(queues, connection=conn)
        print("Worker started...")
        worker.work()
