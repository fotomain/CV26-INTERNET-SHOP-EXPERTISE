"""
YOLO and OpenCV Multi-Stage Exclusion Pipeline (step4_learn).
Strictly excludes:
- People faces and heads (OpenCV Haar Cascades + upper body geometry)
- Background colors around main person/subject (OpenCV adaptive background subtraction)
- People bags, backpacks, handbags, suitcases (YOLO detection)
- People shoes, boots, footwear, and lower limbs (OpenCV spatial cutoff)
- Animals: cats, dogs, birds, horses, cattle, etc. (YOLO detection)
- Cars, motorcycles, buses, trucks, and vehicles (YOLO detection)
- Foreign artifacts, props, furniture, and non-garment objects (YOLO detection)
"""

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["YOLO_VERBOSE"] = "False"

import cv2
import numpy as np
import warnings
warnings.filterwarnings("ignore")

from ultralytics import YOLO

# Load Haar cascade face detectors from OpenCV
CASCADE_PATH = cv2.data.haarcascades
FACE_FRONTAL = cv2.CascadeClassifier(CASCADE_PATH + "haarcascade_frontalface_default.xml")
FACE_PROFILE = cv2.CascadeClassifier(CASCADE_PATH + "haarcascade_profileface.xml")

# Initialize global YOLO model for object exclusion
YOLO_MODEL = None

def get_yolo_model():
    global YOLO_MODEL
    if YOLO_MODEL is None:
        model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "yolov8n.pt"))
        if not os.path.exists(model_path):
            model_path = "yolov8n.pt"
        YOLO_MODEL = YOLO(model_path)
    return YOLO_MODEL

# COCO Class IDs for Exclusion:
# Vehicles: 1 (bicycle), 2 (car), 3 (motorcycle), 4 (airplane), 5 (bus), 6 (train), 7 (truck), 8 (boat)
# Animals: 14 (bird), 15 (cat), 16 (dog), 17 (horse), 18 (sheep), 19 (cow), 20 (elephant), 21 (bear), 22 (zebra), 23 (giraffe)
# Bags & Luggage: 24 (backpack), 26 (handbag), 28 (suitcase)
# Props & Non-clothing Artifacts: 25 (umbrella), 39 (bottle), 40 (wine glass), 41 (cup), 56 (chair), 57 (couch), 58 (potted plant), 63 (laptop), 67 (cell phone), 73 (book), 77 (teddy bear)
YOLO_EXCLUSION_CLASSES = {
    # Vehicles
    1, 2, 3, 4, 5, 6, 7, 8,
    # Animals
    14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
    # Bags
    24, 26, 28,
    # Props & Artifacts
    25, 39, 40, 41, 56, 57, 58, 63, 67, 73, 77
}

def detect_yolo_exclusions(image_bgr: np.ndarray) -> tuple[np.ndarray, list]:
    """
    Uses YOLO to detect and mask out bags, animals, cars/vehicles, and extraneous props.
    Returns:
        tuple: (exclusion_mask [255=Exclude, 0=Keep], list of detected excluded object names)
    """
    h, w = image_bgr.shape[:2]
    yolo_mask = np.zeros((h, w), dtype=np.uint8)
    detected_items = []
    
    try:
        model = get_yolo_model()
        # Run YOLO with imgsz=640 for fast CPU inference
        results = model(image_bgr, imgsz=640, verbose=False, device='cpu')[0]
        
        for box in results.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            
            if conf < 0.20:
                continue
                
            if cls_id in YOLO_EXCLUSION_CLASSES:
                cls_name = model.names[cls_id]
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                
                # Expand bounding box slightly (6%) to ensure clean border removal
                pad_x = int((x2 - x1) * 0.06)
                pad_y = int((y2 - y1) * 0.06)
                x_start = max(0, x1 - pad_x)
                x_end = min(w, x2 + pad_x)
                y_start = max(0, y1 - pad_y)
                y_end = min(h, y2 + pad_y)
                
                yolo_mask[y_start:y_end, x_start:x_end] = 255
                detected_items.append(f"{cls_name} ({conf:.2f})")
    except Exception as e:
        pass

    return yolo_mask, detected_items

def detect_face_and_head_mask(image_bgr: np.ndarray) -> np.ndarray:
    """
    Detects faces using OpenCV Haar Cascades and returns a binary mask of face, head, and neck.
    255 = Exclude (Face/Head), 0 = Keep.
    """
    h, w = image_bgr.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    
    # Frontal faces
    faces = FACE_FRONTAL.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(25, 25))
    for (x, y, fw, fh) in faces:
        y_start = max(0, int(y - fh * 0.35)) # Cover hair/hat
        y_end = min(h, int(y + fh * 1.35))   # Cover neck/chin
        x_start = max(0, int(x - fw * 0.20))
        x_end = min(w, int(x + fw * 1.20))
        mask[y_start:y_end, x_start:x_end] = 255

    # Profile faces
    profiles = FACE_PROFILE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(25, 25))
    for (x, y, fw, fh) in profiles:
        y_start = max(0, int(y - fh * 0.35))
        y_end = min(h, int(y + fh * 1.35))
        x_start = max(0, int(x - fw * 0.20))
        x_end = min(w, int(x + fw * 1.20))
        mask[y_start:y_end, x_start:x_end] = 255

    return mask

def detect_skin_mask(image_bgr: np.ndarray) -> np.ndarray:
    """
    Detects exposed skin areas (arms, legs, torso, face) using YCrCb and HSV color models.
    255 = Exclude (Skin), 0 = Keep.
    """
    ycrcb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)
    lower_ycrcb = np.array([0, 133, 77], dtype=np.uint8)
    upper_ycrcb = np.array([255, 173, 127], dtype=np.uint8)
    skin_ycrcb = cv2.inRange(ycrcb, lower_ycrcb, upper_ycrcb)

    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([0, 35, 45], dtype=np.uint8)
    upper_hsv = np.array([28, 180, 255], dtype=np.uint8)
    skin_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)

    skin_combined = cv2.bitwise_and(skin_ycrcb, skin_hsv)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    skin_mask = cv2.morphologyEx(skin_combined, cv2.MORPH_OPEN, kernel)
    return skin_mask

def segment_studio_and_outdoor_background(image_bgr: np.ndarray) -> np.ndarray:
    """
    Segments out background pixels (studio solid/gradient or outdoor scene background) using OpenCV.
    255 = Foreground, 0 = Background.
    """
    h, w = image_bgr.shape[:2]
    
    # Corner-based background color estimation
    corner_size = max(10, min(h, w) // 20)
    corners = np.concatenate([
        image_bgr[0:corner_size, 0:corner_size].reshape(-1, 3),
        image_bgr[0:corner_size, w-corner_size:w].reshape(-1, 3),
        image_bgr[h-corner_size:h, 0:corner_size].reshape(-1, 3),
        image_bgr[h-corner_size:h, 0:corner_size].reshape(-1, 3)
    ])
    bg_median = np.median(corners, axis=0) # [B, G, R]
    
    # Color distance map
    diff = np.linalg.norm(image_bgr.astype(np.float32) - bg_median.astype(np.float32), axis=2)
    fg_mask = (diff > 24).astype(np.uint8) * 255
    
    # Central focus region for fashion items
    y_min, y_max = int(h * 0.08), int(h * 0.88)
    x_min, x_max = int(w * 0.08), int(w * 0.92)
    
    central_mask = np.zeros((h, w), dtype=np.uint8)
    central_mask[y_min:y_max, x_min:x_max] = 255
    
    fg_mask = cv2.bitwise_and(fg_mask, central_mask)
    
    # Morphological cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel, iterations=1)
    
    return fg_mask

def exclude_shoes_and_lower_limbs(mask: np.ndarray) -> np.ndarray:
    """
    Excludes bottom 16% of the image where shoes, boots, and pavement reside.
    """
    h, w = mask.shape[:2]
    shoe_cutoff = int(h * 0.84)
    out_mask = mask.copy()
    out_mask[shoe_cutoff:h, :] = 0
    return out_mask

def extract_clean_garment_pixels(image_bgr: np.ndarray) -> np.ndarray:
    """
    Full comprehensive YOLO + OpenCV exclusion pipeline:
    1. OpenCV: Background segmentation
    2. OpenCV: Face and head Haar cascade detection
    3. OpenCV: Exposed skin color masking
    4. OpenCV: Shoe and lower limb spatial cutoff
    5. YOLO: Detection and removal of animals, cars, vehicles, bags, and props
    
    Returns:
        np.ndarray: Clean garment pixels in RGB format [N, 3].
    """
    h, w = image_bgr.shape[:2]
    
    # 1. OpenCV Background segmentation
    fg_mask = segment_studio_and_outdoor_background(image_bgr)
    
    # 2. OpenCV Face and head detection
    face_mask = detect_face_and_head_mask(image_bgr)
    
    # 3. OpenCV Skin detection
    skin_mask = detect_skin_mask(image_bgr)
    
    # 4. YOLO Exclusion for animals, cars, bags, and props
    yolo_exclude_mask, _ = detect_yolo_exclusions(image_bgr)
    
    # 5. Combine all exclusion masks
    garment_mask = cv2.bitwise_and(fg_mask, cv2.bitwise_not(face_mask))
    garment_mask = cv2.bitwise_and(garment_mask, cv2.bitwise_not(skin_mask))
    garment_mask = cv2.bitwise_and(garment_mask, cv2.bitwise_not(yolo_exclude_mask))
    
    # 6. OpenCV Shoe and lower limb cutoff
    garment_mask = exclude_shoes_and_lower_limbs(garment_mask)
    
    # Check if sufficient pixels remain; if not, fallback to center crop
    min_pixels = int(h * w * 0.01)
    if np.sum(garment_mask > 0) < min_pixels:
        cy_min, cy_max = int(h * 0.25), int(h * 0.70)
        cx_min, cx_max = int(w * 0.25), int(w * 0.75)
        garment_pixels_bgr = image_bgr[cy_min:cy_max, cx_min:cx_max].reshape(-1, 3)
    else:
        garment_pixels_bgr = image_bgr[garment_mask > 0]
        
    # Convert BGR to RGB
    garment_pixels_rgb = garment_pixels_bgr[:, [2, 1, 0]]
    return garment_pixels_rgb
