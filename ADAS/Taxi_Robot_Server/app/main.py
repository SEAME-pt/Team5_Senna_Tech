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

class RideStatusUpdate(BaseModel):
    status: str

lock = Lock()
ride_counter = itertools.count(1)
available_aruco_ids = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}
allowed_ride_statuses = {"waiting", "pick up", "drop off"}
queue = deque()          # rides waiting
active_mission = None    # current ride running
MAX_QUEUE = 5

@app.post("/ride")
def create_ride(req: RideRequest):
    with lock:
        if len(queue) >= MAX_QUEUE:
            raise HTTPException(429, "Queue full")
        if req.pickup_aruco_id not in available_aruco_ids:
            raise HTTPException(status_code=400, detail="invalid pickup_aruco_id")
        if req.dropoff_aruco_id not in available_aruco_ids:
            raise HTTPException(status_code=400, detail="invalid dropoff_aruco_id")

        mission = {
            "mission_id": next(ride_counter),
            "pickup_aruco_id": req.pickup_aruco_id,
            "dropoff_aruco_id": req.dropoff_aruco_id,
            "status": "waiting",
        }
        queue.append(mission)
        return {**mission, "position_in_queue": len(queue)}

@app.put("/ride/{mission_id}/status")
def update_ride_status(mission_id: int, req: RideStatusUpdate):
    with lock:
        if req.status not in allowed_ride_statuses:
            raise HTTPException(status_code=400, detail=f"invalid status. Valid values: {sorted(allowed_ride_statuses)}")

        target = None
        if active_mission and active_mission["mission_id"] == mission_id:
            target = active_mission
        else:
            for mission in queue:
                if mission["mission_id"] == mission_id:
                    target = mission
                    break

        if target is None:
            raise HTTPException(status_code=404, detail="mission_id not found")

        target["status"] = req.status
        return target

@app.get("/mission/next")
def get_mission():
    global active_mission
    with lock:
        if active_mission is not None:
            return active_mission          # still executing current mission
        if not queue:
            raise HTTPException(404, "No mission")
        active_mission = queue.popleft()   # promote next mission from queue
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
