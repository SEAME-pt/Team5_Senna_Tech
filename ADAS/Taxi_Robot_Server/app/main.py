# server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from threading import Lock
from collections import deque
import itertools

app = FastAPI()

class RideRequest(BaseModel):
    pickup_aruco_id: int
    dropoff_aruco_id: int

lock = Lock()
ride_counter = itertools.count(1)
queue = deque()          # corridas aguardando
active_mission = None    # corrida em execução no veículo
MAX_QUEUE = 5

@app.post("/ride")
def create_ride(req: RideRequest):
    with lock:
        if len(queue) >= MAX_QUEUE:
            raise HTTPException(429, "Queue full")
        mission = {
            "mission_id": next(ride_counter),
            "pickup_aruco_id": req.pickup_aruco_id,
            "dropoff_aruco_id": req.dropoff_aruco_id,
        }
        queue.append(mission)
        return {**mission, "position_in_queue": len(queue)}

@app.get("/mission/next")
def get_mission():
    global active_mission
    with lock:
        if active_mission is not None:
            return active_mission          # ainda executando a atual
        if not queue:
            raise HTTPException(404, "No mission")
        active_mission = queue.popleft()   # promove a próxima da fila
        return active_mission

@app.post("/mission/complete")
def complete_mission(mission_id: int):
    global active_mission
    with lock:
        if active_mission and active_mission["mission_id"] == mission_id:
            active_mission = None
    return {"ok": True}

@app.get("/status")
def status():
    with lock:
        return {
            "active": active_mission,
            "queue": list(queue),
        }
