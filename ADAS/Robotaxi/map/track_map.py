from dataclasses import dataclass
from enum import IntEnum


class Cell(IntEnum):
    ROAD = 0
    BLOCKED = 1
    CROSSING = 2
    ARUCO = 5


@dataclass(frozen=True)
class GridPos:
    row: int
    col: int


TRACK_MAP = [
#    0  1  2  3  4  5  6  7  8  9  10 11 12 13 14
    [1, 1, 1, 5, 0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 1],  # 0
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # 1
    [5, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5],  # 2
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 3
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 4
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 5
    [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 6
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5],  # 7
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 8
    [1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 9
    [1, 1, 1, 1, 1, 0, 1, 1, 5, 0, 1, 1, 1, 1, 0],  # 10
    [1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0],  # 11
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 5],  # 12
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],  # 13
    [1, 1, 1, 5, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],  # 14
    [1, 1, 1, 0, 0, 1, 1, 0, 2, 0, 1, 1, 1, 1, 0],  # 15
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0],  # 16
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 5],  # 17
    [1, 1, 1, 1, 1, 1, 2, 0, 0, 2, 0, 2, 0, 0, 1],  # 18
]


ARUCO_ID_BY_POS = {
    GridPos(17, 14): 0,
    GridPos(12, 14): 1,
    GridPos(7, 14): 2,
    GridPos(2, 14): 3,
    GridPos(0, 12): 4,
    GridPos(0, 7): 5,
    GridPos(0, 3): 6,
    GridPos(2, 0): 7,
    GridPos(9, 5): 8,
    GridPos(14, 3): 9,
    GridPos(18, 6): 11,     # CROSS_RIGHT & PARKING_IN_LEFT
    GridPos(18, 9): 12,     # PARKING_IN_RIGHT
    GridPos(18, 11): 13,    # CROSS_LEFT
    GridPos(15, 8): 14,     # PARKING_OUT_LEFT & PARKING_OUT_LEFT
    GridPos(10, 8): 15,     # PARKING_STATION
}

ARUCO_POS_BY_ID = {
    aruco_id: pos
    for pos, aruco_id in ARUCO_ID_BY_POS.items()
}

PARKING_POS = GridPos(10, 8)
PARKING_ARUCO_ID = ARUCO_ID_BY_POS[PARKING_POS]


def get_grid_pos_from_aruco_id(aruco_id: int) -> GridPos | None:
    return ARUCO_POS_BY_ID.get(aruco_id)


def get_aruco_id(pos: GridPos) -> int | None:
    return ARUCO_ID_BY_POS.get(pos)


def is_inside(pos: GridPos) -> bool:
    return (
        0 <= pos.row < len(TRACK_MAP)
        and 0 <= pos.col < len(TRACK_MAP[0])
    )


def is_drivable(pos: GridPos) -> bool:
    if not is_inside(pos):
        return False

    return TRACK_MAP[pos.row][pos.col] in (
        Cell.ROAD,
        Cell.CROSSING,
        Cell.ARUCO,
    )
