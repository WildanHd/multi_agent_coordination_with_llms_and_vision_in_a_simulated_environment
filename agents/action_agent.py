import pygame
import json
import time
from word2number import w2n

CELL_SIZE = 64  # Assuming 5x5 grid
AGENT_COLOR = (255, 0, 0)
AGENT_RADIUS = 20

DIRECTION_MAP = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0)
}

def get_pixel_position(grid_x, grid_y):
    return (grid_x * CELL_SIZE + CELL_SIZE // 2, grid_y * CELL_SIZE + CELL_SIZE // 2)

def extract_direction_and_steps(step_text):
    """Extract direction and number of steps from text like 'move two grid right'"""
    direction = None
    for d in DIRECTION_MAP:
        if d in step_text:
            direction = d
            break

    # Extract the number using word2number
    count = 1  # default
    try:
        words = step_text.replace("-", " ").split()
        for i, word in enumerate(words):
            try:
                count = w2n.word_to_num(word)
                break
            except:
                continue
    except:
        pass

    return direction, count

def animate_route_on_map(map_path, vision_json_path, route_json_path):
    # Load vision agent output
    with open(vision_json_path) as f:
        vision_data = json.load(f)

    # Load processing agent output (list of steps)
    with open(route_json_path) as f:
        route_data = json.load(f)
        steps = route_data.get("route", [])

    # Find the start position
    start = None
    for obj in vision_data["objects"]:
        if obj["type"] == "start_position":
            start = tuple(obj["position"])
            break
    if not start:
        print("Start position not found.")
        return

    # Initialize pygame
    pygame.init()
    map_img = pygame.image.load(map_path)
    screen = pygame.display.set_mode(map_img.get_size())
    pygame.display.set_caption("Action Agent - Animation")

    clock = pygame.time.Clock()
    position = start

    for step in steps:
        # Handle quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Draw map
        screen.blit(map_img, (0, 0))

        # Draw agent at current position
        pixel_pos = get_pixel_position(*position)
        pygame.draw.circle(screen, AGENT_COLOR, pixel_pos, AGENT_RADIUS)

        # Update display
        pygame.display.flip()
        time.sleep(1)

        # Update position based on step
        direction, count = extract_direction_and_steps(step)
        if direction:
            dx, dy = DIRECTION_MAP[direction]
            for _ in range(count):
                new_x = position[0] + dx
                new_y = position[1] + dy
                if 0 <= new_x < 5 and 0 <= new_y < 5:
                    position = (new_x, new_y)

                    # Redraw everything for each move
                    screen.blit(map_img, (0, 0))
                    pygame.draw.circle(screen, AGENT_COLOR, get_pixel_position(*position), AGENT_RADIUS)
                    pygame.display.flip()
                    time.sleep(0.5)


    # Final frame
    screen.blit(map_img, (0, 0))
    pygame.draw.circle(screen, AGENT_COLOR, get_pixel_position(*position), AGENT_RADIUS)
    pygame.display.flip()

    print("Animation complete. Close the window to exit.")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
