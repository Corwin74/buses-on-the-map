import json
from sys import stderr
import os
import random
from itertools import cycle, islice
import trio
from trio_websocket import open_websocket_url


CHANNEL_COUNT = 5


def load_routes(directory_path='routes'):
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r', encoding='utf8') as file:
                yield json.load(file)


async def run_bus(route, bus_id, send_channel):
    route_points = route['coordinates']
    cycle_route = cycle(route_points)
    lenght_route = len(route_points)
    random_start_point = random.randint(1, lenght_route)
    i = 0
    for point in islice(cycle_route, random_start_point, None):
        message = {
                "busId": f"{route['name']}-{bus_id}",
                "lat": point[0],
                "lng": point[1],
                "route": route['name']
        }
        send_channel.send_nowait(message)
        await trio.sleep(0.1)
    print('Oops')


async def send_updates(server_address, receive_channel):
    message = []
    while True:
        try:
            for i in range(20000):
                message.append(receive_channel.receive_nowait())
            print("got value")
            # await trio.sleep(0.1)
        except trio.WouldBlock:
            print(f'Flush {i}')
            await trio.sleep(5)


async def main():
    async with trio.open_nursery() as nursery:
        send_channels = []
        receive_channels = []
        for i in range(CHANNEL_COUNT):
            send_channel, receive_channel = trio.open_memory_channel(20000)
            send_channels.append(send_channel)
            receive_channels.append(receive_channel)
            nursery.start_soon(send_updates, 'server_address', receive_channel)
        for route in load_routes():
            for bus_id in range(5):
                nursery.start_soon(
                    run_bus,
                    route,
                    bus_id,
                    random.choice(send_channels),
                )


trio.run(main)
'''
    try:
                await trio.sleep(1)
        async with open_websocket_url('ws://127.0.0.1:8080') as ws:
                except OSError as ose:
        print(f'Connection attempt failed: {ose}', file=stderr)
'''