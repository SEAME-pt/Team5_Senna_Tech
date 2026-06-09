from collections import deque
from map.track_map import GridPos, is_drivable


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

        # Only include the neighbor if it is a valid road/station cell.
        if is_drivable(next_pos):
            neighbors.append(next_pos)

    return neighbors


# Find a shortest path from start to goal using breadth-first search.
def find_path(start: GridPos, goal: GridPos) -> list[GridPos]:
    queue = deque([start])
    came_from = {start: None}

    # BFS queue exploration.
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

    # Reconstruct the path from goal back to start.
    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()
    return path
