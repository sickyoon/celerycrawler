
import argparse
import asyncio
import time
from itertools import repeat
import aiohttp
import uvloop

parser = argparse.ArgumentParser(description='Run aiohttp/uvloop benchmark')
parser.add_argument('--endpoint', type=str, default='http://localhost:9000/json', help='endpoint url to hit')
parser.add_argument('--num_iter', type=int, default=10000, help='test iterations')

async def fetch(url, session, sem):
    async with sem:
        async with session.get(url) as resp:
            return await resp.json()

async def main(loop, args):
    futures = []
    sem = asyncio.Semaphore(1000, loop=self.loop)
    async with aiohttp.ClientSession() as session:
        for _ in repeat(None, args.num_iter):
            futures.append(fetch(args.endpoint, session, sem))
        await asyncio.gather(*futures, loop=loop)

if __name__ == '__main__':
    args = parser.parse_args()
    loop = uvloop.new_event_loop()
    start = time.perf_counter()
    loop.run_until_complete(
        main(loop, args)
    )
    print(time.perf_counter()-start)

