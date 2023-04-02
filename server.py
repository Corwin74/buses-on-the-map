import json
import trio
from trio_websocket import serve_websocket, ConnectionClosed


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


async def main():
    await serve_websocket(buses_server, '127.0.0.1', 8080, ssl_context=None)

trio.run(main)
