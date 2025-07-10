
import os
import sys
import cv2
import numpy as np
import time
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


# Refactored for Streamlit: Expose a function for live recording
def record_live_video(recording_duration=30, show_window=False):
    """
    Record video from webcam for a given duration (seconds).
    Returns the path to the saved video file, or None on failure.
    If show_window=True, shows OpenCV window (for local use only).
    """
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return None
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, DEFAULT_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, DEFAULT_HEIGHT)
        cap.set(cv2.CAP_PROP_FPS, FPS)
        _, image = cap.read()
        if image is None:
            cap.release()
            return None
        new_width = DEFAULT_WIDTH
        new_height = DEFAULT_HEIGHT
        os.makedirs(OUTPUT_VIDEOS_DIR, exist_ok=True)
        os.makedirs(UPLOADS_DIR, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_filename = UPLOADS_DIR / f'live_recording_{timestamp}.mp4'
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(str(output_filename), fourcc, FPS, (new_width, new_height))
        if not out.isOpened():
            cap.release()
            return None
        start_time = time.time()
        while True:
            _, image = cap.read()
            if image is None:
                break
            elapsed_time = time.time() - start_time
            if elapsed_time >= recording_duration:
                break
            image = cv2.resize(image, (new_width, new_height))
            out.write(image)
            if show_window:
                cv2.imshow("Webcam Recording - Press 'q' to stop", image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        cap.release()
        out.release()
        if show_window:
            cv2.destroyAllWindows()
        return str(output_filename)
    except Exception as e:
        if 'cap' in locals():
            cap.release()
        if 'out' in locals():
            out.release()
        if show_window:
            cv2.destroyAllWindows()
        return None
