
import asyncio
import time
from itertools import repeat
import aiohttp
import uvloop

class AsyncClient:

    def __init__(self, loop, endpoint, num_iter):
        self.sem = asyncio.Semaphore(1000, loop=loop)
        self.loop = loop
        self.endpoint = endpoint
        self.num_iter = num_iter

    async def fetch(self, session):
        async with self.sem:
            async with session.get(self.endpoint) as resp:
                return await resp.json()

    async def fetch_all(self):
        futures = []
        async with aiohttp.ClientSession() as session:
            for _ in repeat(None, self.num_iter):
                futures.append(self.fetch(session))
            await asyncio.gather(*futures, loop=self.loop)

    def run(self):
        start = time.perf_counter()
        self.loop.run_until_complete(
            self.fetch_all()
        )
        return time.perf_counter() - start

if __name__ == '__main__':
    loop = uvloop.new_event_loop()
    c = AsyncClient(
        loop=loop,
        endpoint='http://localhost:9000/json',
        num_iter=10000
    )
    print(c.run())

