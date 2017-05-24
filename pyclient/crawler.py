from celery_client import CeleryClient

import argparse

parser = argparse.ArgumentParser(description='Run aiohttp/uvloop benchmark')
parser.add_argument('cmd', type=str, default='async', help='run test')
parser.add_argument('--endpoint',
                    type=str,
                    default='http://localhost:9000/json',
                    help='endpoint url to hit')
parser.add_argument('--num_iter',
                    type=int,
                    default=100,
                    help='test iterations')

if __name__ == '__main__':
    args = parser.parse_args()
    if args.cmd == 'async':
        from async_client import AsyncClient as Client
    else:
        from celery_client import CeleryClient as Client
    c = Client(
        endpoint = args.endpoint,
        num_iter = args.num_iter
    )
    print(c.run())
