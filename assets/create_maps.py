import cv2
import numpy as np
import os
import random
import json

# Preparing objects and directory path

ASSET_PATH = "objects" 
MAP_SAVE_PATH = "generated_maps/generated_map.png"
METADATA_SAVE_PATH = "generated_maps/generated_map.json"

# Preparing basic grid

GRID_SIZE = (5, 5) # Number of grid in x and y axis
CELL_SIZE = (64, 64) # Image width and height in pixels

def load_object_images(asset_path):
    object_files = [f for f in os.listdir(asset_path) if f.endswith(".png")]
    object_types = list(set(f.split(".")[0] for f in object_files))
    selected_types = random.sample(object_types, k=3)
    
    objects = {}
    for t in selected_types:
        img_path = os.path.join(asset_path, t + ".png")
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        if img is not None:
            img = cv2.resize(img, CELL_SIZE)
            objects[t] = img
    return objects

def paste_object(canvas, obj_img, x, y):
    if obj_img.shape[2] == 4:
        alpha = obj_img[:, :, 3] / 255.0
        for c in range(3):
            canvas[y:y+CELL_SIZE[1], x:x+CELL_SIZE[0], c] = (
                alpha * obj_img[:, :, c] +
                (1 - alpha) * canvas[y:y+CELL_SIZE[1], x:x+CELL_SIZE[0], c]
            )
    else:
        canvas[y:y+CELL_SIZE[1], x:x+CELL_SIZE[0]] = obj_img

def draw_grid(canvas):
    rows, cols = GRID_SIZE
    for r in range(1, rows):
        y = r * CELL_SIZE[1]
        cv2.line(canvas, (0, y), (canvas.shape[1], y), (200, 200, 200), 1)
    for c in range(1, cols):
        x = c * CELL_SIZE[0]
        cv2.line(canvas, (x, 0), (x, canvas.shape[0]), (200, 200, 200), 1)

def create_map():
    rows, cols = GRID_SIZE

    # Prepare the empty room for drawing

    canvas = np.ones((rows * CELL_SIZE[1], cols * CELL_SIZE[0], 3), dtype=np.uint8) * 255
    draw_grid(canvas)

    metadata = {"start": None, "finish": None, "objects": []} # Prepare metadata for start and finish positions

    available_cells = [(r, c) for r in range(rows) for c in range(cols)]

    # Randomly assign start and finish
    start = random.choice(available_cells)
    available_cells.remove(start)

    finish = random.choice(available_cells)
    available_cells.remove(finish)

    metadata["start"] = {"row": start[0], "col": start[1]}
    metadata["finish"] = {"row": finish[0], "col": finish[1]}

    # Draw start (black) and finish (blue)
    start_img = np.full((*CELL_SIZE, 3), (0, 0, 0), dtype=np.uint8)
    finish_img = np.full((*CELL_SIZE, 3), (255, 0, 0), dtype=np.uint8)

    paste_object(canvas, start_img, start[1] * CELL_SIZE[0], start[0] * CELL_SIZE[1])
    paste_object(canvas, finish_img, finish[1] * CELL_SIZE[0], finish[0] * CELL_SIZE[1])

    # Load 3 random object types
    objects = load_object_images(ASSET_PATH)

    for obj_type, obj_img in objects.items():
        cell = random.choice(available_cells)
        available_cells.remove(cell)
        paste_object(canvas, obj_img, cell[1] * CELL_SIZE[0], cell[0] * CELL_SIZE[1])
        metadata["objects"].append({"type": obj_type, "row": cell[0], "col": cell[1]})

    # Save map and metadata
    os.makedirs("maps", exist_ok=True)
    cv2.imwrite(MAP_SAVE_PATH, canvas)
    with open(METADATA_SAVE_PATH, "w") as f:
        json.dump(metadata, f, indent=2)

    print("Map and metadata saved!")

if __name__ == "__main__":
    create_map()