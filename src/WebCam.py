import os
import sys
import cv2
import numpy as np
import time
import tempfile
from ultralytics import YOLO
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config.settings import *

# Configuration constants
CONFIDENCE = 0.5
FONT_SCALE = 1
THICKNESS = 1
FPS = 20
DEFAULT_WIDTH = 1080
DEFAULT_HEIGHT = 720

# Load YOLO model and labels
try:
    labels = open(COCO_NAMES).read().strip().split("\n")
    colors = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")
    model = YOLO(str(YOLO_MODEL))
    print("[OK] YOLO model loaded successfully")
except Exception as e:
    print(f"[ERROR] Error loading YOLO model: {e}")
    # Don't exit, just use None and handle gracefully
    model = None
    labels = []
    colors = []

def record_from_webcam(duration=5, output_path=None):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Webcam not found or not accessible.")
        return None

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    if output_path is None:
        temp_file = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
        output_path = temp_file.name

    out = cv2.VideoWriter(output_path, fourcc, 20.0, (frame_width, frame_height))

    start_time = time.time()
    while int(time.time() - start_time) < duration:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()
    return output_path
