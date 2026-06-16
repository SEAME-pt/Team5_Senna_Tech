from dataclasses import dataclass
from enum import IntEnum

class Cell(IntEnum):
    ROAD = 0
    BLOCKED = 1
    STATION = 2


@dataclass(frozen=True)
class GridPos:
    row: int
    col: int

TRACK_MAP = [
#             q           q              q
#    0  1  2  3  4  5  6  7  8  9  10 11 12 13 14
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 0
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # 1  
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 2 q
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 3
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 4
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 5
    [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 6
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 7 q
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 8
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 9
    [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0],  # 10
    [1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0],  # 11
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],  # 12 q
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],  # 13
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],  # 14
    [1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0],  # 15
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0],  # 16
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0],  # 17 q
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 18
#                      q        q        q
]

def is_inside(pos: GridPos) -> bool:
    return (
        0 <= pos.row < len(TRACK_MAP)
        and 0 <= pos.col < len(TRACK_MAP[0])
    )

def is_drivable(pos: GridPos) -> bool:
    if not is_inside(pos):
        return False
    return TRACK_MAP[pos.row][pos.col] in (Cell.ROAD, Cell.STATION)

# Convert a string into a grid position object.
def parse_coord(value: str) -> GridPos:
    try:
        row_str, col_str = value.split(",")
        return GridPos(int(row_str), int(col_str))
    except ValueError as exc:
        raise ValueError(
            f"Invalid coordinate '{value}'. Expected format: row,col"
        ) from exc

# Is inside the map and on a drivable cell.
def validate_coord(name: str, pos: GridPos) -> None:
    if not is_inside(pos):
        raise ValueError(f"{name} {pos} is outside the map")

    if not is_drivable(pos):
        raise ValueError(f"{name} {pos} is not on a drivable cell")
