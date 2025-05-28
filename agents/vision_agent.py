import cv2
import os
import json
import torch
from ultralytics import YOLO
import numpy as np

# YOU STILL HAVE TO DEFINE THE NUMBER OF GRID

class VisionAgent:

    def pixel_to_grid(x, y, img_width, img_height, grid_size=5):
        cell_width = img_width // grid_size
        cell_height = img_height // grid_size
        return [x // cell_width, y // cell_height]


    def detect_with_yolo(image_path, model, img_width, img_height):
        results = model(image_path)
        detections = []

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls)
                label = model.names[cls_id]
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                grid_pos = VisionAgent.pixel_to_grid(center_x, center_y, img_width, img_height)
                detections.append({
                    "type": label,
                    "condition": f"{label} detected",
                    "position": grid_pos
                })
        return detections


    def detect_start_finish_by_color(img):
        detections = []
        height, width = img.shape[:2]

        def get_grid_pos(c):
            M = cv2.moments(c)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                return [cx * 5 // width, cy * 5 // height]
            return None

        def is_rectangle(contour, epsilon_ratio=0.05):
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon_ratio * peri, True)
            return len(approx) == 4 and cv2.isContourConvex(approx)

        # Helper to process color mask
        def process_color(mask, label, condition):
            local_detections = []
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for c in contours:
                if is_rectangle(c) and cv2.contourArea(c) > 100:  # optional: filter small areas
                    grid = get_grid_pos(c)
                    if grid:
                        local_detections.append({
                            "type": label,
                            "condition": condition,
                            "position": grid
                        })
            return local_detections

        # Detect black rectangles (start)
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([50, 50, 50])
        mask_black = cv2.inRange(img, lower_black, upper_black)
        detections += process_color(mask_black, "start_position", "starting point")

        # Detect blue rectangles (finish)
        lower_blue = np.array([100, 0, 0])
        upper_blue = np.array([255, 100, 100])
        mask_blue = cv2.inRange(img, lower_blue, upper_blue)
        detections += process_color(mask_blue, "finish_position", "goal point")

        return detections


    def run_vision_agent(image_path, output_path):
        # Load YOLO CPU model (default yolov8n, you can change it)
        model = YOLO('yolov8n.pt')
        model.to('cpu')

        # Load image
        img = cv2.imread(image_path)
        height, width = img.shape[:2]
        
        # Run YOLO
        yolo_detections = VisionAgent.detect_with_yolo(image_path, model, width, height)

        # Run OpenCV color detection
        color_detections = VisionAgent.detect_start_finish_by_color(img)

        # Combine
        all_detections = yolo_detections + color_detections

        result = {"objects": all_detections}

        # Save result to JSON
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"Detections saved to {output_path}")
