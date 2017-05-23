
import json
import urllib.request
from celery import Celery

app = Celery('crawler',
    broker='redis://localhost:6379',
    backend='redis://localhost:6379',
    task_serializer='json',
    result_serializer='json',
    accept_content=['application/json']
)

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ENABLE_UTC=True,
)

@app.task
def fetch(url):
    """Fetch a single url
    """
    with urllib.request.urlopen(url) as f:
        resp = json.loads(f.read())
        return resp
