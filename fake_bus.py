import json
import logging
from pathlib import Path
import random
from itertools import cycle, islice
import configargparse
import dotenv
import trio
from trio_websocket import open_websocket_url, HandshakeError, ConnectionClosed

# pylint: disable=C0103

logger = logging.getLogger(__file__)
READ_CHANNEL_DELAY = 1
SEND_BUS_COORD_DELAY = 1
CHANNEL_BUFFER_SIZE = 10000


def load_routes(directory_path='routes'):
    for filepath in Path(directory_path).glob("**/*.json"):
        with open(filepath, 'r', encoding='utf-8') as file:
            yield json.load(file)


async def run_bus(route, bus_id, send_channel):
    route_points = route['coordinates']
    cycle_route = cycle(route_points)
    lenght_route = len(route_points)
    random_start_point = random.randint(1, lenght_route)
    for point in islice(cycle_route, random_start_point, None):
        bus_geopoint = {
                "busId": f"{route['name']}-{bus_id}",
                "lat": point[0],
                "lng": point[1],
                "route": route['name']
        }
        await send_channel.send(bus_geopoint)
        await trio.sleep(SEND_BUS_COORD_DELAY)


async def send_updates(server_address, receive_channel):
    while True:
        try:
            async with open_websocket_url(server_address) as ws:
                while True:
                    try:
                        with trio.move_on_after(1):
                            buses_counter = 0
                            buses_geopoints = []
                            while True:
                                bus_geopoint = receive_channel.receive_nowait()
                                buses_geopoints.append(bus_geopoint)
                                buses_counter += 1
                                await trio.sleep(0)
                        message = {
                            'msgType': 'Buses',
                            'buses': buses_geopoints,
                        }
                        await ws.send_message(
                            json.dumps(message, ensure_ascii=True)
                        )
                        logger.debug('%s buses send', buses_counter)
                        reply_message = await ws.get_message()
                        logger.debug(reply_message)
                    except trio.WouldBlock:
                        logger.debug('Dry channel at %s', buses_counter)
                        message = {
                            'msgType': 'Buses',
                            'buses': buses_geopoints,
                        }
                        await ws.send_message(
                            json.dumps(message, ensure_ascii=True)
                        )
                        logger.debug('%s buses send', buses_counter)
                        reply_message = await ws.get_message()
                        logger.debug(reply_message)
                        await trio.sleep(READ_CHANNEL_DELAY)
        except HandshakeError:
            logger.warning('Handshake error!')
            await trio.sleep(5)
            logger.debug('Trying reconnect')
        except ConnectionClosed:
            logger.warning('Lost connection!')
            await trio.sleep(5)
            logger.debug('Trying reconnect')


async def main():
    dotenv.load_dotenv()
    parser = configargparse.ArgParser()
    parser.add(
        '-host',
        required=False,
        help='host to connection',
        env_var='HOST',
        default='127.0.0.1',
    )
    parser.add(
        '-port',
        required=False,
        help='buses server port',
        env_var='BUSES_SERVER_PORT',
        default='8080',
    )
    parser.add(
        '-r',
        required=False,
        type=int,
        help='routes number',
        env_var='ROUTES_NUMBER',
        dest='routes_number',
    )
    parser.add(
        '-b',
        required=False,
        type=int,
        help='buses_per_route',
        env_var='BUSES_PER_ROUTE',
        dest='buses_per_route',
        default=1,
    )
    parser.add(
        '-id',
        required=False,
        type=str,
        help='emulator id',
        env_var='EMULATOR_ID',
        dest='emulator_id',
        default='1',
    )
    parser.add(
        '-w',
        required=False,
        type=int,
        help='websockets number',
        env_var='WEBSOCKETS_NUMBER',
        dest='websockets_number',
        default=5,
    )
    parser.add(
        '-v',
        required=False,
        action='count',
        dest='verbose',
        default=0,
    )
    options = parser.parse_args()

    if options.verbose == 0:
        logging_level = logging.ERROR
    elif options.verbose == 1:
        logging_level = logging.WARNING
    elif options.verbose == 2:
        logging_level = logging.INFO
    else:
        logging_level = logging.DEBUG

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging_level,
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logger.setLevel(logging_level)

    logger.debug(options)
    logger.info(
        'Host: %s, port: %s, websockets_number: %s',
        options.host,
        options.port,
        options.websockets_number,
    )
    try:
        async with trio.open_nursery() as nursery:
            send_channels = []
            receive_channels = []
            for _ in range(options.websockets_number):
                send_channel, receive_channel = trio.open_memory_channel(
                    CHANNEL_BUFFER_SIZE,
                )
                send_channels.append(send_channel)
                receive_channels.append(receive_channel)
                nursery.start_soon(
                    send_updates,
                    f'ws://{options.host}:{options.port}',
                    receive_channel
                )
            for counter, route in enumerate(load_routes(), start=1):
                if options.routes_number and counter > options.routes_number:
                    break
                for bus_id in range(1, options.buses_per_route + 1):
                    nursery.start_soon(
                        run_bus,
                        route,
                        f'{options.emulator_id}-{bus_id}',
                        random.choice(send_channels),
                    )
    except HandshakeError:
        print('Main')

try:
    trio.run(main)
except KeyboardInterrupt:
    logger.debug('Exit by Ctrl-C!')
