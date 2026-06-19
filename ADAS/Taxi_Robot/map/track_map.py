from dataclasses import dataclass
from enum import IntEnum


class Cell(IntEnum):
    ROAD = 0
    BLOCKED = 1
    STATION = 2
    ARUCO = 5


@dataclass(frozen=True)
class GridPos:
    row: int
    col: int


TRACK_MAP = [
#    0  1  2  3  4  5  6  7  8  9  10 11 12 13 14
    [1, 1, 1, 5, 0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 1],  # 0
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # 1
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5],  # 2
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 3
    [5, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 4
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 5
    [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 6
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5],  # 7
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 8
    [1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 9
    [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0],  # 10
    [1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0],  # 11
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 5],  # 12
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],  # 13
    [1, 1, 1, 5, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],  # 14
    [1, 1, 1, 0, 0, 1, 1, 0, 5, 0, 1, 1, 1, 1, 0],  # 15
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0],  # 16
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 5],  # 17
    [1, 1, 1, 1, 1, 1, 5, 0, 0, 5, 0, 0, 5, 0, 1],  # 18
]


ARUCO_ID_BY_POS = {
    GridPos(17, 14): 0,
    GridPos(12, 14): 1,
    GridPos(7, 14): 2,
    GridPos(2, 14): 3,
    GridPos(0, 12): 4,
    GridPos(0, 7): 5,
    GridPos(0, 3): 6,
    GridPos(4, 0): 7,
    GridPos(9, 5): 8,
    GridPos(14, 3): 9,
    GridPos(18, 6): 11,
    GridPos(18, 9): 12,
    GridPos(15, 8): 13,
    GridPos(18, 12): 14,
}


ARUCO_POS_BY_ID = {
    aruco_id: pos
    for pos, aruco_id in ARUCO_ID_BY_POS.items()
}


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
        Cell.STATION,
        Cell.ARUCO,
    )


def is_aruco_cell(pos: GridPos) -> bool:
    if not is_inside(pos):
        return False

    return TRACK_MAP[pos.row][pos.col] == Cell.ARUCO


def parse_coord(value: str) -> GridPos:
    try:
        row_str, col_str = value.split(",")
        return GridPos(int(row_str), int(col_str))
    except ValueError as exc:
        raise ValueError(
            f"Invalid coordinate '{value}'. Expected format: row,col"
        ) from exc


def validate_coord(name: str, pos: GridPos) -> None:
    if not is_inside(pos):
        raise ValueError(f"{name} {pos} is outside the map")

    if not is_drivable(pos):
        raise ValueError(f"{name} {pos} is not on a drivable cell")