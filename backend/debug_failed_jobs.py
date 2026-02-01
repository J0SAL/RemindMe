from redis import Redis
from rq import Queue
from rq.registry import FailedJobRegistry
import os
from dotenv import load_dotenv

load_dotenv()

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
conn = Redis.from_url(redis_url)
q = Queue(connection=conn)
registry = FailedJobRegistry(queue=q)

print(f"Failed Jobs: {len(registry)}")
for job_id in registry.get_job_ids():
    job = q.fetch_job(job_id)
    print(f"Job {job_id} Error: {job.exc_info}")
