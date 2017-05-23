
import argparse
import asyncio
import time
from itertools import repeat
import aiohttp
import uvloop

parser = argparse.ArgumentParser(description='Run aiohttp/uvloop benchmark')
parser.add_argument('--endpoint', type=str, default='http://localhost:9000/json', help='endpoint url to hit')
parser.add_argument('--num_iter', type=int, default=10, help='test iterations')

async def run(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

async def main(loop, args):
    await asyncio.gather(*[run(args.endpoint) for _ in repeat(None, args.num_iter)], loop=loop)

if __name__ == '__main__':
    args = parser.parse_args()
    loop = uvloop.new_event_loop()
    start = time.perf_counter()
    loop.run_until_complete(
        main(loop, args)
    )
    end = time.perf_counter()
    print(end-start)

