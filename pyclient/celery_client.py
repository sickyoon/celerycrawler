import time
from itertools import repeat
from celery import group
from celery_worker import fetch


class CeleryClient:

    def __init__(self, endpoint, num_iter):
        self.endpoint = endpoint
        self.num_iter = num_iter

    def run(self):
        start = time.perf_counter()
        jobs = group(
            fetch.s(url=self.endpoint) for _ in repeat(None, self.num_iter)
        )
        jobs().get()
        return time.perf_counter() - start

if __name__ == '__main__':
    c = CeleryClient(
        endpoint = "http://localhost:9000/json",
        num_iter = 1000
    )
    print(c.run())
