import json
import time
from typing import Any, Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

app = FastAPI(title="Robotaxi WebSocket Gateway")

LATEST_STATE: Dict[str, Any] = {}


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

    except WebSocketDisconnect:
        return
