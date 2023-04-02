import json
import trio
from sys import stderr
from trio_websocket import open_websocket_url


def load_coord(file):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    return json.loads(content)


async def main():
    bus_track = load_coord('156.json')
    try:
        async with open_websocket_url('ws://127.0.0.1:8080') as ws:
            for point in bus_track['coordinates']:
                message = {
                        "busId": "c790сс",
                        "lat": point[0],
                        "lng": point[1],
                        "route": "156"
                }
                await ws.send_message(json.dumps(message))
                message = await ws.get_message()
                print('Received message: %s' % message)
                await trio.sleep(1)
    except OSError as ose:
        print('Connection attempt failed: %s' % ose, file=stderr)

trio.run(main)
