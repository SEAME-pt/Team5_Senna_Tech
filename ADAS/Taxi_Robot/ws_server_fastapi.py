import json
import time
from typing import Any, Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI(title="Robotaxi WebSocket Gateway")

LATEST_STATE: Dict[str, Any] = {}
PENDING_COMMANDS: list[Dict[str, Any]] = []


class StartMissionCommand(BaseModel):
    pickup: int
    dropoff: int


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "has_state": bool(LATEST_STATE),
        "timestamp": time.time(),
    }


@app.get("/vehicle/latest")
def latest_vehicle_state():
    if not LATEST_STATE:
        return JSONResponse(status_code=404, content={"error": "no telemetry received"})
    return LATEST_STATE


@app.post("/command/start-mission")
def command_start_mission(cmd: StartMissionCommand):
    command = {
        "type": "command",
        "command": "start_mission",
        "pickup": cmd.pickup,
        "dropoff": cmd.dropoff,
        "queued_at": time.time(),
    }
    PENDING_COMMANDS.append(command)
    return {"status": "queued", "command": command}


@app.post("/command/stop-mission")
def command_stop_mission():
    command = {
        "type": "command",
        "command": "stop_mission",
        "queued_at": time.time(),
    }
    PENDING_COMMANDS.append(command)
    return {"status": "queued", "command": command}


@app.websocket("/ws/robotaxi")
async def robotaxi_ws(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            raw_msg = await websocket.receive_text()
            payload = json.loads(raw_msg)

            payload["received_at"] = time.time()
            LATEST_STATE.clear()
            LATEST_STATE.update(payload)

            await websocket.send_json(
                {
                    "type": "ack",
                    "received_at": payload["received_at"],
                }
            )

            if PENDING_COMMANDS:
                await websocket.send_json(PENDING_COMMANDS.pop(0))

    except WebSocketDisconnect:
        return
