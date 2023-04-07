import json
import logging
import os
import random
from itertools import cycle, islice
import trio
from trio_websocket import open_websocket_url


logger = logging.getLogger(__file__)
CHANNEL_COUNT = 5
RECEIVE_DELAY = 1


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
    for point in islice(cycle_route, random_start_point, None):
        message = {
                "busId": f"{route['name']}-{bus_id}",
                "lat": point[0],
                "lng": point[1],
                "route": route['name']
        }
        send_channel.send_nowait(message)
        await trio.sleep(2)


async def send_updates(server_address, receive_channel):
    message = []
    async with open_websocket_url(server_address) as ws:
        while True:
            try:
                with trio.move_on_after(1):
                    count = 0
                    while True:
                        value = receive_channel.receive_nowait()
                        message.append(value)
                        count += 1
                        await trio.sleep(0)
                await ws.send_message(
                    json.dumps(message, ensure_ascii=True)
                )
                logger.debug('%s items send', count)
                message = []
            except trio.WouldBlock:
                logger.debug('Dry channel at %s', count)
                await ws.send_message(
                    json.dumps(message, ensure_ascii=True)
                )
                await trio.sleep(RECEIVE_DELAY)
                message = []


async def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    async with trio.open_nursery() as nursery:
        send_channels = []
        receive_channels = []
        for _ in range(CHANNEL_COUNT):
            send_channel, receive_channel = trio.open_memory_channel(400000)
            send_channels.append(send_channel)
            receive_channels.append(receive_channel)
            nursery.start_soon(send_updates, 'ws://127.0.0.1:8080', receive_channel)
        for route in load_routes():
            for bus_id in range(35):
                nursery.start_soon(
                    run_bus,
                    route,
                    bus_id,
                    random.choice(send_channels),
                )


trio.run(main)
