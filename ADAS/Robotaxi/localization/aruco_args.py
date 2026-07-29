from dataclasses import dataclass

from map.track_map import (
	ARUCO_POS_BY_ID,
	GridPos,
	PARKING_POS,
	get_grid_pos_from_aruco_id,
)


@dataclass(frozen=True)
class MissionArucoArgs:
	pickup_aruco_id: int
	dropoff_aruco_id: int
	pickup: GridPos
	dropoff: GridPos


def resolve_mission_aruco_args(
	pickup_aruco_id: int,
	dropoff_aruco_id: int,
) -> MissionArucoArgs:
	if pickup_aruco_id < 0:
		raise ValueError("pickup ArUco ID must be >= 0")

	if dropoff_aruco_id < 0:
		raise ValueError("dropoff ArUco ID must be >= 0")

	if pickup_aruco_id == dropoff_aruco_id:
		raise ValueError("pickup and dropoff ArUco IDs must be different")

	pickup = get_grid_pos_from_aruco_id(pickup_aruco_id)
	dropoff = get_grid_pos_from_aruco_id(dropoff_aruco_id)

	valid_aruco_ids = sorted(ARUCO_POS_BY_ID.keys())

	if pickup is None:
		raise ValueError(
			f"pickup ArUco ID {pickup_aruco_id} is not mapped in track_map. "
			f"Valid IDs: {valid_aruco_ids}"
		)

	if dropoff is None:
		raise ValueError(
			f"dropoff ArUco ID {dropoff_aruco_id} is not mapped in track_map. "
			f"Valid IDs: {valid_aruco_ids}"
		)

	if pickup == PARKING_POS:
		raise ValueError("pickup cannot be the parking position")

	if dropoff == PARKING_POS:
		raise ValueError("dropoff cannot be the parking position")

	return MissionArucoArgs(
		pickup_aruco_id=pickup_aruco_id,
		dropoff_aruco_id=dropoff_aruco_id,
		pickup=pickup,
		dropoff=dropoff,
	)
