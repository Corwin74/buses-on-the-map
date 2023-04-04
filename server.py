import json
from functools import partial
import trio
from trio_websocket import serve_websocket, ConnectionClosed


HOST = '127.0.0.1'
LISTEN_BUSES_COORD_PORT = 8080

buses = {}


async def buses_server(request):

    web_socket = await request.accept()
    while True:
        try:
            message = json.loads(await web_socket.get_message())
            print(message)
            #buses = {
            #            "msgType": "Buses",
            #            "buses": [
            #                {"busId": message['busId'], "lat": message['lat'], "lng": message['lng'], "route": "120"},
            #                {"busId": "a134aa", "lat": 55.7494, "lng": 37.621, "route": "670к"},
            #            ]
            #}
            await web_socket.send_message('OK')
            #message = await web_socket.get_message()
            #print(message)
        except ConnectionClosed:
            break

listen_buses_coord_ws = partial(
    serve_websocket,
    buses_server,
    HOST,
    LISTEN_BUSES_COORD_PORT,
    ssl_context=None
)


async def main():
    async with trio.open_nursery() as nursery:
        nursery.start_soon(listen_buses_coord_ws)


trio.run(main)
