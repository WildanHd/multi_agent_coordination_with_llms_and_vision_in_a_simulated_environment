import json
from collections import deque
from pathlib import Path

GRID_SIZE = 5

# Text directions for each step
DIRECTION_MAP = {
    (0, -1): "move one grid up",
    (0, 1): "move one grid down",
    (-1, 0): "move one grid left",
    (1, 0): "move one grid right"
}

def bfs_shortest_path(start, goal, obstacles):
    queue = deque([(start, [])])
    visited = set([start])

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) == goal:
            return path

        for dx, dy in DIRECTION_MAP:
            nx, ny = x + dx, y + dy
            next_pos = (nx, ny)

            if (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and
                next_pos not in obstacles and next_pos not in visited):
                visited.add(next_pos)
                queue.append((next_pos, path + [(dx, dy)]))

    return []  # No path found

def convert_path_to_text(path):
    return [DIRECTION_MAP[step] for step in path]

def plan_route_rule_based(vision_output_path, save_path):
    with open(vision_output_path, 'r') as f:
        data = json.load(f)

    start = None
    finish = None
    obstacles = set()

    for obj in data["objects"]:
        pos = tuple(obj["position"])
        if obj["type"] == "start_position":
            start = pos
        elif obj["type"] == "finish_position":
            finish = pos
        else:
            obstacles.add(pos)

    if not start or not finish:
        print("Start or finish not found in the vision output.")
        return

    path = bfs_shortest_path(start, finish, obstacles)
    route = convert_path_to_text(path) if path else ["No path found"]

    # Save route to file
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    with open(save_path, 'w') as f:
        json.dump({"route": route}, f, indent=2)

    print(f"Route saved to: {save_path}")
    return route
