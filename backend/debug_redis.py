from redis import Redis
from rq import Queue
import os
from dotenv import load_dotenv

load_dotenv()

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
conn = Redis.from_url(redis_url)
q = Queue(connection=conn)

print(f"Queue Size: {len(q)}")
print(f"Jobs in Registry: {q.job_ids}")
