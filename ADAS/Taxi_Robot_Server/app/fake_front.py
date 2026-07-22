import asyncio, json
import websockets

async def main():
    async with websockets.connect("ws://localhost:8000/ws/frontend") as ws:
        while True:
            msg = await ws.recv()
            print("frontend recebeu:", json.loads(msg))

asyncio.run(main())