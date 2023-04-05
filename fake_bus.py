import json
from sys import stderr
import os
import trio
from trio_websocket import open_websocket_url


def load_routes(directory_path='routes'):
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r', encoding='utf8') as file:
                yield json.load(file)


async def send_bus_route(route):
    try:
        async with open_websocket_url('ws://127.0.0.1:8080') as ws:
            for point in route['coordinates']:
                message = {
                        "busId": route['name'],
                        "lat": point[0],
                        "lng": point[1],
                        "route": route['name']
                }
                await ws.send_message(json.dumps(message, ensure_ascii=True))
                message = await ws.get_message()
                await trio.sleep(1)
    except OSError as ose:
        print('Connection attempt failed: %s' % ose, file=stderr)


async def main():
    async with trio.open_nursery() as nursery:
        for route in load_routes():
            nursery.start_soon(send_bus_route, route)


trio.run(main)
