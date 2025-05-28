import cv2
import os
import random

def list_image_files(folder_path, extensions={'.png', '.jpg', '.jpeg'}):
    return [
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and os.path.splitext(f)[1].lower() in extensions
    ]

def load_and_display_map(map_path):
    img = cv2.imread(map_path)
    if img is None:
        raise ValueError(f"Cannot load image at {map_path}")
    cv2.imshow("Simulation Environment", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))

    map_folder = os.path.join(base_dir, 'assets/generated_maps/')
    #map_folder = "/Users/wildanhidayat/Documents/GitHub/multi_agent_coordination_with_llms_and_vision_in_a_simulated_environment/assets/generated_maps"
    
    # Import all map file name
    map_images = list_image_files(map_folder)
    
    # Choose one map randomly
    map_file = random.choice(map_images)  

    # Define the map path
    full_path = os.path.join(map_folder, map_file)

    # Load and display the selected map
    load_and_display_map(full_path)