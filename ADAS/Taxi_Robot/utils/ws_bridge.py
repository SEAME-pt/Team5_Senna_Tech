import asyncio
import json
import logging
import threading
import time
from typing import Any, Dict, Optional

try:
    import websockets
except ImportError:  # pragma: no cover - dependency optional during local development
    websockets = None


class RobotaxiWebSocketBridge:
    """Background publisher for Robotaxi telemetry over WebSocket."""

    def __init__(self, server_url: Optional[str], publish_hz: float):
        self.server_url = server_url
        self.publish_hz = publish_hz

        self._logger = logging.getLogger(self.__class__.__name__)
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._latest_payload: Optional[Dict[str, Any]] = None
        self._pending_commands: list[Dict[str, Any]] = []
        self._is_connected = False

    @property
    def is_enabled(self) -> bool:
        return bool(self.server_url)

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    def start(self) -> None:
        if not self.is_enabled:
            return

        if websockets is None:
            self._logger.warning(
                "WebSocket bridge disabled: missing dependency 'websockets'. "
                "Install it with: pip install websockets"
            )
            return

        if self._thread and self._thread.is_alive():
            return

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_thread, name="robotaxi-ws", daemon=True)
        self._thread.start()
        self._logger.info("WebSocket bridge started -> %s", self.server_url)

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)

    def update(self, telemetry: Dict[str, Any]) -> None:
        if not self.is_enabled:
            return

        payload = {
            "type": "telemetry",
            "sent_at": time.time(),
            "telemetry": telemetry,
        }

        with self._lock:
            self._latest_payload = payload

    def _run_thread(self) -> None:
        asyncio.run(self._run_loop())

    def get_next_command(self) -> Optional[Dict[str, Any]]:
        with self._lock:
            if not self._pending_commands:
                return None
            return self._pending_commands.pop(0)

    async def _run_loop(self) -> None:
        reconnect_delay_s = 2.0
        send_interval_s = 1.0 / self.publish_hz

        while not self._stop_event.is_set():
            try:
                async with websockets.connect(self.server_url, ping_interval=20, ping_timeout=20) as ws:
                    self._is_connected = True
                    self._logger.info("WebSocket connected")

                    hello = {
                        "type": "hello",
                        "sent_at": time.time(),
                    }
                    await ws.send(json.dumps(hello))

                    while not self._stop_event.is_set():
                        payload = self._consume_latest_payload()
                        if payload is not None:
                            await ws.send(json.dumps(payload))

                        command = await self._try_receive_command(ws)
                        if command is not None:
                            with self._lock:
                                self._pending_commands.append(command)

                        await asyncio.sleep(send_interval_s)

            except Exception as exc:
                self._is_connected = False
                if not self._stop_event.is_set():
                    self._logger.warning("WebSocket disconnected (%s). Retrying in %.1fs...", exc, reconnect_delay_s)
                    await asyncio.sleep(reconnect_delay_s)

        self._is_connected = False

    def _consume_latest_payload(self) -> Optional[Dict[str, Any]]:
        with self._lock:
            payload = self._latest_payload
            self._latest_payload = None
        return payload

    async def _try_receive_command(self, ws) -> Optional[Dict[str, Any]]:
        try:
            raw = await asyncio.wait_for(ws.recv(), timeout=0.01)
        except asyncio.TimeoutError:
            return None
        except Exception:
            return None

        try:
            message = json.loads(raw)
        except Exception:
            return None

        if message.get("type") != "command":
            return None

        return message
