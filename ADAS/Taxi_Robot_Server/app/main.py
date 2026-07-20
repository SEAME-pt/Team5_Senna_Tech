import json
import threading
from collections import deque
from typing import Any, Deque, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

app = FastAPI(title="Robotaxi mission server")


class MissionCommandRequest(BaseModel):
    command: str
    pickup: int | None = None
    dropoff: int | None = None


class RobotaxiSessionManager:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._robot_websocket: Optional[WebSocket] = None
        self._pending_commands: Deque[dict[str, Any]] = deque()
        self._latest_telemetry: Optional[dict[str, Any]] = None

    async def connect_robot(self, websocket: WebSocket) -> None:
        await websocket.accept()
        with self._lock:
            if self._robot_websocket is not None:
                try:
                    await self._robot_websocket.close(code=1000, reason="replaced by new robot connection")
                except Exception:
                    pass
            self._robot_websocket = websocket

    async def disconnect_robot(self, websocket: WebSocket) -> None:
        with self._lock:
            if self._robot_websocket is websocket:
                self._robot_websocket = None

    async def handle_robot_message(self, websocket: WebSocket, message: dict[str, Any]) -> None:
        message_type = message.get("type")
        if message_type == "hello":
            await websocket.send_json({"type": "ack", "status": "ready"})
            return

        if message_type == "telemetry":
            with self._lock:
                self._latest_telemetry = message
            return

    async def dispatch_command(self, command: dict[str, Any]) -> bool:
        with self._lock:
            websocket = self._robot_websocket
            if websocket is None:
                self._pending_commands.append(command)
                return False

        try:
            await websocket.send_json(command)
            return True
        except Exception:
            with self._lock:
                self._pending_commands.append(command)
            return False

    async def flush_pending_commands(self) -> None:
        with self._lock:
            pending = list(self._pending_commands)
            self._pending_commands.clear()
            websocket = self._robot_websocket

        if websocket is None or not pending:
            return

        for command in pending:
            try:
                await websocket.send_json(command)
            except Exception:
                with self._lock:
                    self._pending_commands.append(command)

    def status(self) -> dict[str, Any]:
        with self._lock:
            return {
                "connected": self._robot_websocket is not None,
                "pending_commands": list(self._pending_commands),
                "latest_telemetry": self._latest_telemetry,
            }


session_manager = RobotaxiSessionManager()


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok"}


@app.post("/mission/command", status_code=202)
async def send_mission_command(req: MissionCommandRequest) -> dict[str, Any]:
    if req.command not in {"start_mission", "stop_mission"}:
        raise HTTPException(status_code=400, detail="unsupported command")

    if req.command == "start_mission" and (req.pickup is None or req.dropoff is None):
        raise HTTPException(status_code=400, detail="start_mission requires pickup and dropoff")

    payload: dict[str, Any] = {"type": "command", "command": req.command}
    if req.pickup is not None:
        payload["pickup"] = req.pickup
    if req.dropoff is not None:
        payload["dropoff"] = req.dropoff

    delivered = await session_manager.dispatch_command(payload)
    return {"accepted": True, "delivered": delivered, "command": payload}


@app.get("/status")
def status() -> dict[str, Any]:
    return session_manager.status()


@app.websocket("/ws/robotaxi")
async def robot_websocket(websocket: WebSocket) -> None:
    await session_manager.connect_robot(websocket)
    await session_manager.flush_pending_commands()

    try:
        while True:
            raw_message = await websocket.receive_text()
            try:
                payload = json.loads(raw_message)
            except json.JSONDecodeError:
                continue

            await session_manager.handle_robot_message(websocket, payload)
    except WebSocketDisconnect:
        await session_manager.disconnect_robot(websocket)
    except Exception:
        await session_manager.disconnect_robot(websocket)
