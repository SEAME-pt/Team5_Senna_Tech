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
        self._frontend_websockets: set[WebSocket] = set()
        self._pending_commands: Deque[dict[str, Any]] = deque()
        self._latest_telemetry: Optional[dict[str, Any]] = None

    # ---------- robot side (unchanged behaviour) ----------

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
            # Normalize into the shape the Flutter app expects:
            # {"type": "telemetry", "telemetry": {"mission_state":..., "aruco":..., "current_grid":...}}
            # If the robot already nests its payload under "telemetry", keep it as-is;
            # otherwise treat every other top-level key as part of the telemetry body.
            telemetry_body = message.get("telemetry")
            if telemetry_body is None:
                telemetry_body = {k: v for k, v in message.items() if k != "type"}

            outgoing = {"type": "telemetry", "telemetry": telemetry_body}

            with self._lock:
                self._latest_telemetry = outgoing

            await self.broadcast_to_frontends(outgoing)
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

    # ---------- frontend side (new) ----------

    async def connect_frontend(self, websocket: WebSocket) -> None:
        await websocket.accept()
        with self._lock:
            self._frontend_websockets.add(websocket)
            latest = self._latest_telemetry

        # Push the last known telemetry immediately so the app doesn't
        # sit blank until the next robot update arrives.
        if latest is not None:
            try:
                await websocket.send_json(latest)
            except Exception:
                pass

    async def disconnect_frontend(self, websocket: WebSocket) -> None:
        with self._lock:
            self._frontend_websockets.discard(websocket)

    async def broadcast_to_frontends(self, payload: dict[str, Any]) -> None:
        with self._lock:
            targets = list(self._frontend_websockets)

        dead: list[WebSocket] = []
        for ws in targets:
            try:
                await ws.send_json(payload)
            except Exception:
                dead.append(ws)

        if dead:
            with self._lock:
                for ws in dead:
                    self._frontend_websockets.discard(ws)

    def status(self) -> dict[str, Any]:
        with self._lock:
            return {
                "connected": self._robot_websocket is not None,
                "frontend_clients": len(self._frontend_websockets),
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
    """Connection used by the physical robot / robot-side client only."""
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


@app.websocket("/ws/frontend")
async def frontend_websocket(websocket: WebSocket) -> None:
    """Connection used by the Flutter app. Read-only stream of telemetry;
    commands still go through POST /mission/command."""
    await session_manager.connect_frontend(websocket)

    try:
        while True:
            # The app doesn't need to send anything, but we keep receiving
            # so the disconnect is detected promptly. Anything it does send
            # is ignored (or you can add a ping/pong handler here later).
            await websocket.receive_text()
    except WebSocketDisconnect:
        await session_manager.disconnect_frontend(websocket)
    except Exception:
        await session_manager.disconnect_frontend(websocket)