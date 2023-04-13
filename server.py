import json
import logging
from functools import partial
import configargparse
import dotenv
import trio
from trio_websocket import serve_websocket, ConnectionClosed
from jsonschema import validate, exceptions
from schema import bound_message_schema

# pylint: disable=C0103

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

    def update(self, bound):
        self.east_lng = bound['east_lng']
        self.north_lat = bound['north_lat']
        self.south_lat = bound['south_lat']
        self.west_lng = bound['west_lng']


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


async def listen_browser(ws, shared_init_bound):
    while True:
        error_message = json.loads(await ws.get_message())
        logger.debug('Recive message: %s', error_message)
        try:
            validate(error_message, bound_message_schema)
            logger.debug('New bound message is valid. Processing...')
            shared_init_bound.update(error_message['data'])
        except exceptions.ValidationError as exc:
            logger.error(exc.message)
            error_message = {
                    'msgType': 'Errors',
                    'errors': [exc.message],
            }
            await ws.send_message(json.dumps(error_message))


async def talk_to_browser(ws, shared_init_bound):
    while True:
        await send_buses(ws, shared_init_bound)
        await trio.sleep(1)


async def browser_server(request):
    ws = await request.accept()
    logger.debug('Open connection on browsers port')
    try:
        async with trio.open_nursery() as nursery:
            shared_init_bound = WindowBound({
                'east_lng': 0,
                'north_lat': 0,
                'south_lat': 0,
                'west_lng': 0,
            })
            nursery.start_soon(listen_browser, ws, shared_init_bound)
            nursery.start_soon(talk_to_browser, ws, shared_init_bound)
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
    browser_server,
    HOST,
    LISTEN_BROWSERS_PORT,
    ssl_context=None,
    max_message_size=10485760,
)


async def main():
    dotenv.load_dotenv()
    parser = configargparse.ArgParser()
    parser.add(
        '-host',
        required=False,
        help='host to connection',
        env_var='HOST',
        default='127.0.0.1'
    )
    parser.add(
        '-browser_port',
        required=False,
        help='host to connection',
        env_var='BROWSER_PORT',
        default='8000'
    )
    parser.add(
        '-bus_port',
        required=False,
        help='buses server port',
        env_var='BUSES_SERVER_PORT',
        default='8080',
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
    async with trio.open_nursery() as nursery:
        nursery.start_soon(listen_buses_coord_ws)
        nursery.start_soon(listen_browsers_ws)


try:
    trio.run(main)
except KeyboardInterrupt:
    logger.debug('Exit by Ctrl-C!')
