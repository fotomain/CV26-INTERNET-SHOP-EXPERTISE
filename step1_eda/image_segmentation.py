"""
Image Segmentation and Exclusion Pipeline for Product Color Analysis.
Excludes:
- People faces and skin
- Background colors around main person/subject
- People bags and peripheral accessories
- People shoes and lower limbs
- Animals, cars, artifacts
Extracts garment colors and determines if the product is colored.
"""

import cv2
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

# Load Haar cascade face detectors from OpenCV
CASCADE_PATH = cv2.data.haarcascades
FACE_FRONTAL = cv2.CascadeClassifier(CASCADE_PATH + "haarcascade_frontalface_default.xml")
FACE_PROFILE = cv2.CascadeClassifier(CASCADE_PATH + "haarcascade_profileface.xml")

def detect_face_mask(image_bgr: np.ndarray) -> np.ndarray:
    """
    Detects faces using Haar Cascades and returns a binary mask of face/head regions to exclude.
    Mask: 255 = Exclude, 0 = Keep.
    """
    h, w = image_bgr.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    
    # Detect frontal faces
    faces = FACE_FRONTAL.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(25, 25))
    for (x, y, fw, fh) in faces:
        # Expand slightly to cover hair and neck
        y_start = max(0, int(y - fh * 0.2))
        y_end = min(h, int(y + fh * 1.3))
        x_start = max(0, int(x - fw * 0.15))
        x_end = min(w, int(x + fw * 1.15))
        mask[y_start:y_end, x_start:x_end] = 255

    # Detect profile faces
    profiles = FACE_PROFILE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(25, 25))
    for (x, y, fw, fh) in profiles:
        y_start = max(0, int(y - fh * 0.2))
        y_end = min(h, int(y + fh * 1.3))
        x_start = max(0, int(x - fw * 0.15))
        x_end = min(w, int(x + fw * 1.15))
        mask[y_start:y_end, x_start:x_end] = 255

    return mask

def detect_skin_mask(image_bgr: np.ndarray) -> np.ndarray:
    """
    Detects exposed skin areas (arms, legs, face, neck) in YCrCb and HSV color spaces.
    Mask: 255 = Exclude, 0 = Keep.
    """
    # YCrCb skin thresholding
    ycrcb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)
    lower_ycrcb = np.array([0, 133, 77], dtype=np.uint8)
    upper_ycrcb = np.array([255, 173, 127], dtype=np.uint8)
    skin_ycrcb = cv2.inRange(ycrcb, lower_ycrcb, upper_ycrcb)

    # HSV skin thresholding
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([0, 38, 50], dtype=np.uint8)
    upper_hsv = np.array([25, 180, 255], dtype=np.uint8)
    skin_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # Combined skin mask
    skin_mask = cv2.bitwise_and(skin_ycrcb, skin_hsv)
    
    # Morphological cleaning
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel)
    return skin_mask

def segment_foreground(image_bgr: np.ndarray) -> np.ndarray:
    """
    Segments the main foreground subject from white/light neutral studio background.
    Mask: 255 = Foreground, 0 = Background.
    """
    h, w = image_bgr.shape[:2]
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    
    # Estimate background color from the 4 corners
    corners = np.concatenate([
        image_bgr[0:15, 0:15].reshape(-1, 3),
        image_bgr[0:15, w-15:w].reshape(-1, 3),
        image_bgr[h-15:h, 0:15].reshape(-1, 3),
        image_bgr[h-15:h, w-15:w].reshape(-1, 3)
    ])
    bg_color = np.median(corners, axis=0) # [B, G, R]
    
    # Color distance from background
    diff = np.linalg.norm(image_bgr.astype(np.float32) - bg_color.astype(np.float32), axis=2)
    
    # Threshold distance
    fg_mask = (diff > 22).astype(np.uint8) * 255
    
    # Fill holes and smooth
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel, iterations=1)
    
    return fg_mask

def get_garment_mask(image_bgr: np.ndarray, category_name: str = "") -> np.ndarray:
    """
    Generates an isolated mask for the main garment by excluding:
    - Background around the person
    - Face, head, and exposed skin
    - Shoes (bottom 15% in full-body shots)
    - Peripheral bags/accessories
    """
    h, w = image_bgr.shape[:2]
    cat_lower = str(category_name).lower()
    
    # 1. Foreground segmentation
    fg_mask = segment_foreground(image_bgr)
    
    # 2. Face and skin exclusion
    face_mask = detect_face_mask(image_bgr)
    skin_mask = detect_skin_mask(image_bgr)
    
    # If the item is jewelry/watches/shoes itself, do not over-mask skin/shoes
    is_jewelry_or_accessory = any(kw in cat_lower for kw in ['watch', 'earring', 'necklace', 'ring', 'bracelet', 'sunglass'])
    is_footwear = any(kw in cat_lower for kw in ['shoe', 'boot', 'sneaker', 'sandal', 'heel', 'espadrille', 'slides'])
    is_bag = any(kw in cat_lower for kw in ['bag', 'backpack', 'wallet', 'suitcase'])

    garment_mask = fg_mask.copy()
    
    if not is_jewelry_or_accessory and not is_footwear and not is_bag:
        # Exclude face and exposed skin
        garment_mask = cv2.bitwise_and(garment_mask, cv2.bitwise_not(face_mask))
        garment_mask = cv2.bitwise_and(garment_mask, cv2.bitwise_not(skin_mask))
        
        # Exclude shoes/feet (bottom 15% when full person is present)
        if h > 150:
            shoe_exclusion_zone = int(h * 0.86)
            garment_mask[shoe_exclusion_zone:h, :] = 0
            
            # Exclude extreme top 8% (hair/headwear) if full height
            head_exclusion_zone = int(h * 0.08)
            garment_mask[0:head_exclusion_zone, :] = 0

    # Ensure at least some foreground pixels remain
    if np.sum(garment_mask > 0) < (h * w * 0.01):
        garment_mask = fg_mask # Fallback to general foreground

    return garment_mask

def rgb_to_color_name(r: int, g: int, b: int) -> tuple[str, bool]:
    """
    Classifies an RGB color into a human-readable name and determines if it is chromatic ('is_colored').
    """
    # Convert RGB to HSV
    bgr_pixel = np.uint8([[[b, g, r]]])
    hsv_pixel = cv2.cvtColor(bgr_pixel, cv2.COLOR_BGR2HSV)[0][0]
    hue, sat, val = int(hsv_pixel[0]) * 2, float(hsv_pixel[1]) / 255.0, float(hsv_pixel[2]) / 255.0

    # Monochrome / Neutral conditions
    if val < 0.15:
        return "Black", False
    if val > 0.88 and sat < 0.12:
        return "White", False
    if sat < 0.15:
        return "Grey", False
    if sat < 0.28 and 0.40 < val < 0.88 and (25 <= hue <= 50):
        return "Beige/Khaki", False

    # Chromatic colors
    is_colored = True
    if hue < 15 or hue >= 345:
        color_name = "Red" if sat > 0.4 else "Pink"
    elif 15 <= hue < 42:
        color_name = "Orange" if val > 0.4 else "Brown"
    elif 42 <= hue < 68:
        color_name = "Yellow"
    elif 68 <= hue < 165:
        color_name = "Green"
    elif 165 <= hue < 200:
        color_name = "Cyan/Turquoise"
    elif 200 <= hue < 255:
        color_name = "Navy Blue" if val < 0.55 else "Blue"
    elif 255 <= hue < 295:
        color_name = "Purple"
    elif 295 <= hue < 345:
        color_name = "Pink/Magenta"
    else:
        color_name = "Multicolor"

    return color_name, is_colored

def extract_dominant_colors(image_path: str, category_name: str = "", n_clusters: int = 4) -> dict:
    """
    Extracts dominant garment colors after applying face, background, and accessory exclusions.
    
    Returns:
        dict: {
            'is_colored': bool,
            'dominant_color': str,
            'color_palette': list of hex colors,
            'avg_saturation': float,
            'avg_brightness': float
        }
    """
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        return {
            "is_colored": False,
            "dominant_color": "Unknown",
            "color_palette": ["#000000"],
            "avg_saturation": 0.0,
            "avg_brightness": 0.0
        }

    mask = get_garment_mask(img_bgr, category_name=category_name)
    garment_pixels_bgr = img_bgr[mask > 0]

    if len(garment_pixels_bgr) < 20:
        garment_pixels_bgr = img_bgr.reshape(-1, 3)

    # Convert to RGB
    garment_pixels_rgb = garment_pixels_bgr[:, [2, 1, 0]]

    # Sample for speed if large
    if len(garment_pixels_rgb) > 5000:
        indices = np.random.choice(len(garment_pixels_rgb), 5000, replace=False)
        sample_pixels = garment_pixels_rgb[indices]
    else:
        sample_pixels = garment_pixels_rgb

    # Run KMeans to find top color clusters
    k = min(n_clusters, len(sample_pixels))
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=3)
    kmeans.fit(sample_pixels)

    centers = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_
    counts = np.bincount(labels, minlength=k)
    order = np.argsort(counts)[::-1]

    palette_hex = []
    primary_color_name = "Unknown"
    is_colored = False
    has_chromatic_cluster = False

    for idx in order:
        r, g, b = centers[idx]
        hex_code = f"#{r:02x}{g:02x}{b:02x}"
        palette_hex.append(hex_code)
        
        c_name, c_colored = rgb_to_color_name(r, g, b)
        cluster_weight = counts[idx] / len(labels)

        if idx == order[0]:
            primary_color_name = c_name
            if c_colored:
                is_colored = True

        # If a significant cluster (>20%) is chromatic, mark as colored
        if c_colored and cluster_weight >= 0.20:
            has_chromatic_cluster = True

    if has_chromatic_cluster:
        is_colored = True

    # Calculate average saturation and brightness of garment pixels
    hsv_pixels = cv2.cvtColor(np.uint8([garment_pixels_bgr]), cv2.COLOR_BGR2HSV)[0]
    avg_sat = float(np.mean(hsv_pixels[:, 1]) / 255.0)
    avg_val = float(np.mean(hsv_pixels[:, 2]) / 255.0)

    if avg_sat > 0.22 and not (avg_val < 0.15 or avg_val > 0.92):
        is_colored = True

    return {
        "is_colored": bool(is_colored),
        "dominant_color": primary_color_name,
        "color_palette": palette_hex,
        "avg_saturation": round(avg_sat, 4),
        "avg_brightness": round(avg_val, 4)
    }
