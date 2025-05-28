import json
import inflect

def manhattan_route(start, finish):
    p = inflect.engine()
    moves = []
    dx = finish[0] - start[0]
    dy = finish[1] - start[1]

    if dy < 0:
        moves.append(f"move {p.number_to_words(abs(dy))} grid up")
    elif dy > 0:
        moves.append(f"move {p.number_to_words(abs(dy))} grid down")

    if dx < 0:
        moves.append(f"move {p.number_to_words(abs(dx))} grid left")
    elif dx > 0:
        moves.append(f"move {p.number_to_words(abs(dx))} grid right")

    return moves

def process_vision_output(vision_output_path, save_path=None):
    with open(vision_output_path, 'r') as f:
        data = json.load(f)

    start = None
    finish = None

    for obj in data.get("objects", []):
        if obj["type"] == "start_position":
            start = obj["position"]
        elif obj["type"] == "finish_position":
            finish = obj["position"]

    if start is None or finish is None:
        actions = ["Start or finish not found"]
    else:
        actions = manhattan_route(start, finish)

    # Optional: Save output
    if save_path:
        with open(save_path, 'w') as f:
            json.dump({"route": actions}, f, indent=4)

    return actions
