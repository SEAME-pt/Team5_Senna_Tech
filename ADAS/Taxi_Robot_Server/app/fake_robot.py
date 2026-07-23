import asyncio, json
import websockets

async def main():
    async with websockets.connect("ws://localhost:8000/ws/robotaxi") as ws:
        await ws.send(json.dumps({"type": "hello"}))
        print("robot:", await ws.recv())  # must be {"type":"ack","status":"ready"}

        for i in range(5):
            telemetry = {
                "type": "telemetry",
                "mission_state": "en_route",
                "aruco": {"id": 3, "distance_cm": 42.5},
                "current_grid": {"row": 8, "col": 7 + i},
            }
            await ws.send(json.dumps(telemetry))
            print("sent telemetry", i)
            await asyncio.sleep(2)

asyncio.run(main())