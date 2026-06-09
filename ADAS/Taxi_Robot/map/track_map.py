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
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
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
