from collections import deque
from map.track_map import GridPos, is_drivable, TRACK_MAP


# Four cardinal moves on the map: up, down, left, and right.
DIRECTIONS = [
    GridPos(-1, 0),
    GridPos(1, 0),
    GridPos(0, -1),
    GridPos(0, 1),
]


# Return the adjacent drivable positions from the current grid cell.
def get_neighbors(pos: GridPos) -> list[GridPos]:
    neighbors = []

    for direction in DIRECTIONS:
        next_pos = GridPos(
            pos.row + direction.row,
            pos.col + direction.col,
        )

        if is_drivable(next_pos):
            neighbors.append(next_pos)

    return neighbors


# Find a shortest path from start to goal using breadth-first search.
def find_path(start: GridPos, goal: GridPos) -> list[GridPos]:
    queue = deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        for neighbor in get_neighbors(current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

    if goal not in came_from:
        return []

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()
    return path


def print_path_map(
    path: list[GridPos],
    current_pos: GridPos,
    goal_pos: GridPos | None,
    pickup: GridPos | None = None,
    dropoff: GridPos | None = None,
) -> None:
    path_cells = set()

    for pos in path:
        path_cells.add((pos.row, pos.col))

    print("\n========== ROBOTAXI PATH MAP ==========")
    print("Legend:")
    print("  # = blocked")
    print("  . = road")
    print("  * = path")
    print("  C = car")
    print("  G = current goal")
    print("  P = pickup")
    print("  D = dropoff")
    print()

    for row_index, row in enumerate(TRACK_MAP):
        line = ""

        for col_index, cell in enumerate(row):
            is_current = (
                current_pos.row == row_index
                and current_pos.col == col_index
            )

            is_goal = (
                goal_pos is not None
                and goal_pos.row == row_index
                and goal_pos.col == col_index
            )

            is_pickup = (
                pickup is not None
                and pickup.row == row_index
                and pickup.col == col_index
            )

            is_dropoff = (
                dropoff is not None
                and dropoff.row == row_index
                and dropoff.col == col_index
            )

            is_path = (row_index, col_index) in path_cells

            if is_current:
                line += "C "
            elif is_goal:
                line += "G "
            elif is_pickup:
                line += "P "
            elif is_dropoff:
                line += "D "
            elif is_path:
                line += "* "
            elif cell == 0:
                line += ". "
            else:
                line += "# "

        print(line)

    print("=======================================\n")