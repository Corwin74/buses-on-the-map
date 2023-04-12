from dataclasses import dataclass, asdict
import json
import logging
from functools import partial
import configargparse
import dotenv
import trio
from trio_websocket import serve_websocket, ConnectionClosed


logger = logging.getLogger(__file__)
HOST = '127.0.0.1'
LISTEN_BUSES_COORD_PORT = 8080
LISTEN_BROWSERS_PORT = 8000

buses = {}


class Bus:
    def __init__(self, bus):
        self.bus_id = bus['busId']
        self.lat = bus['lat']
        self.lng = bus['lng']
        self.route = bus['route']

    def to_dict(self):
        return {
            'busId': self.bus_id,
            'lat': self.lat,
            'lng': self.lng,
            'route': self.route
        }


class WindowBound:
    def __init__(self, bound):
        self.east_lng = bound['east_lng']
        self.north_lat = bound['north_lat']
        self.south_lat = bound['south_lat']
        self.west_lng = bound['west_lng']

    def is_inside(self, bus):
        if not self.south_lat < bus.lat < self.north_lat:
            return False
        if not self.west_lng < bus.lng < self.east_lng:
            return False
        return True


async def send_buses(ws, current_bound):
    visible_buses = []
    for _, bus in buses.items():
        if current_bound.is_inside(bus):
            visible_buses.append(bus.to_dict())
    reply_message = {
        'msgType': 'Buses',
        'buses': visible_buses,
    }
    await ws.send_message(
        json.dumps(reply_message, ensure_ascii=True)
    )


async def listen_browsers(ws):
    while True:
        message = json.loads(await ws.get_message())
        logger.debug('Recive message: %s', message)
        await send_buses(ws, WindowBound(message['data']))


async def talk_to_browser(request):
    web_socket = await request.accept()
    logger.debug('Open connection on browsers port')
    try:
        async with trio.open_nursery() as nursery:
            nursery.start_soon(listen_browsers, web_socket)
            while False:
                buses_coord_snapshot = []
                for bus, bus_details in buses.items():
                    buses_coord_snapshot.append({
                        'busId': bus,
                        'lat': bus_details['lat'],
                        'lng': bus_details['lng'],
                        'route': bus_details['route'],
                    })
                reply_message = {
                    'msgType': 'Buses',
                    'buses': buses_coord_snapshot,
                }
                await web_socket.send_message(
                    json.dumps(reply_message, ensure_ascii=True)
                )
                await trio.sleep(1)
    except ConnectionClosed:
        logger.debug('Close connection on browsers port')


async def buses_server(request):
    web_socket = await request.accept()
    while True:
        try:
            message = json.loads(await web_socket.get_message())
            for bus in message['buses']:
                bus_id = bus['busId']
                buses[bus_id] = Bus(bus)
            await web_socket.send_message('OK')
        except ConnectionClosed:
            break


listen_buses_coord_ws = partial(
    serve_websocket,
    buses_server,
    HOST,
    LISTEN_BUSES_COORD_PORT,
    ssl_context=None,
    max_message_size=10485760,
)

listen_browsers_ws = partial(
    serve_websocket,
    talk_to_browser,
    HOST,
    LISTEN_BROWSERS_PORT,
    ssl_context=None,
    max_message_size=10485760,
)


async def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logger.setLevel(logging.DEBUG)
    async with trio.open_nursery() as nursery:
        nursery.start_soon(listen_buses_coord_ws)
        nursery.start_soon(listen_browsers_ws)


trio.run(main)
