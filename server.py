import json
import logging
from functools import partial
import trio
from trio_websocket import serve_websocket, ConnectionClosed


logger = logging.getLogger(__file__)
HOST = '127.0.0.1'
LISTEN_BUSES_COORD_PORT = 8080
LISTEN_BROWSERS_PORT = 8000

buses = {}


async def talk_to_browser(request):
    web_socket = await request.accept()
    logger.debug('Open connection on browsers port')
    try:
        message = json.loads(await web_socket.get_message())
        logger.debug('Recive message: %s', message)
        while True:
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
            bus_id = message['busId']
            buses[bus_id] = {
                'lat': message['lat'],
                'lng': message['lng'],
                'route': message['route'],
            }
            await web_socket.send_message('OK')
        except ConnectionClosed:
            break

listen_buses_coord_ws = partial(
    serve_websocket,
    buses_server,
    HOST,
    LISTEN_BUSES_COORD_PORT,
    ssl_context=None
)

listen_browsers_ws = partial(
    serve_websocket,
    talk_to_browser,
    HOST,
    LISTEN_BROWSERS_PORT,
    ssl_context=None
)


async def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    async with trio.open_nursery() as nursery:
        nursery.start_soon(listen_buses_coord_ws)
        nursery.start_soon(listen_browsers_ws)


trio.run(main)
