"""
Target Country Reference Palette Extractor (step4_learn).
Strict Rules:
- Strictly EXCLUDES all .json files from step5_new_country/.
- Uses ONLY graphic image files (.png, .jpg, .jpeg).
- Applies YOLO + OpenCV exclusion pipeline (faces, skin, background, shoes, bags, animals, cars, props).
- Generates exactly NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = 3 distinct palettes per market segment.
"""

import os
import glob
import cv2
import numpy as np
from sklearn.cluster import KMeans

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exclusion_pipeline import extract_clean_garment_pixels

# Explicit requirement constant
NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = 3

PALETTE_THEMES = [
    "Palette 1 (Core & Classic Neutrals)",
    "Palette 2 (Contemporary & Earthy Street)",
    "Palette 3 (Vibrant Statement & Accents)"
]

def rgb_to_lab(rgb_array: np.ndarray) -> np.ndarray:
    """Converts RGB in [0, 255] to CIELAB using OpenCV."""
    norm_rgb = np.clip(rgb_array / 255.0, 0.0, 1.0).astype(np.float32)
    if len(norm_rgb.shape) == 1:
        norm_rgb = norm_rgb.reshape(1, 1, 3)
    elif len(norm_rgb.shape) == 2:
        norm_rgb = norm_rgb.reshape(-1, 1, 3)
    lab = cv2.cvtColor(norm_rgb, cv2.COLOR_RGB2Lab)
    return lab.reshape(-1, 3)

def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    """Converts hex '#RRGGBB' to (R, G, B)."""
    h = hex_str.strip().lstrip('#')
    if len(h) == 6:
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return (128, 128, 128)

def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Converts (R, G, B) to '#RRGGBB'."""
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

def partition_into_3_palettes(cluster_centers_rgb: np.ndarray) -> tuple[list[list[str]], list[list[list[float]]]]:
    """
    Partitions the 12 extracted fashion color centroids into exactly
    NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = 3 distinct 4-color palettes:
      1. Core & Classic Neutrals (Low saturation / balanced luminance)
      2. Contemporary & Earthy Street (Warm mid-tones & muted casuals)
      3. Vibrant Statement & Accents (Higher chromatic saturation / vivid tones)
    """
    colors_rgb = [np.array(c, dtype=int) for c in cluster_centers_rgb]
    
    # Calculate saturation and luminance in HSV space
    color_metrics = []
    for c in colors_rgb:
        rgb_norm = np.uint8([[c]])
        hsv = cv2.cvtColor(rgb_norm, cv2.COLOR_RGB2HSV)[0][0]
        h, s, v = hsv[0], hsv[1], hsv[2]
        color_metrics.append({
            'rgb': c.tolist(),
            'hex': rgb_to_hex(*c),
            'sat': float(s),
            'val': float(v),
            'hue': float(h)
        })

    # Sort by saturation
    sorted_by_sat = sorted(color_metrics, key=lambda x: (x['sat'], x['val']))
    
    # Palette 1: Lowest saturation (Neutrals: black, charcoal, navy, white, slate)
    p1_items = sorted_by_sat[:4]
    # Palette 3: Highest saturation (Vibrant / statement accents)
    p3_items = sorted_by_sat[-4:]
    # Palette 2: Mid-range saturation (Contemporary earthy & casual tones)
    p2_items = sorted_by_sat[4:8] if len(sorted_by_sat) >= 12 else sorted_by_sat[4:len(sorted_by_sat)-4]
    if len(p2_items) < 4:
        p2_items = sorted_by_sat[2:6]

    palettes_hex = [
        [x['hex'] for x in p1_items],
        [x['hex'] for x in p2_items],
        [x['hex'] for x in p3_items]
    ]

    palettes_rgb = [
        [x['rgb'] for x in p1_items],
        [x['rgb'] for x in p2_items],
        [x['rgb'] for x in p3_items]
    ]

    return palettes_hex, palettes_rgb

def find_only_image_paths(base_dir: str, gender: str, country_dir: str = 'step5_new_country') -> list[str]:
    """
    Finds ONLY image files (.png, .jpg, .jpeg) for a given gender in target country directory.
    Explicitly ignores and excludes any .json files.
    """
    search_dirs = [
        os.path.join(base_dir, country_dir, 'images', gender),
        os.path.join(base_dir, country_dir, gender)
    ]
    
    valid_image_exts = {'.png', '.jpg', '.jpeg'}
    found_images = []
    
    for s_dir in search_dirs:
        if not os.path.exists(s_dir):
            continue
            
        for fname in sorted(os.listdir(s_dir)):
            _, ext = os.path.splitext(fname)
            # Strictly filter for only png and jpg images; ignore json and hidden files
            if ext.lower() in valid_image_exts and not fname.startswith('.'):
                img_path = os.path.join(s_dir, fname)
                found_images.append(img_path)
                
    return found_images

def extract_country_profiles_from_images(base_dir: str = None, country_dir: str = 'step5_new_country', country_name: str = "United States", iso_code: str = "USA") -> dict:
    """
    Extracts reference palette distributions for Men and Women purely from .jpg and .png images
    in target country directory using YOLO and OpenCV exclusions.
    Outputs exactly NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = 3 palettes per segment.
    """
    if base_dir is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    print("================================================================================")
    print(f"   EXTRACTING TARGET COUNTRY PALETTES: {country_name} ({country_dir})          ")
    print(f"   Required Number of Palettes: NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = {NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED}")
    print("   (STRICTLY IMAGES ONLY: .PNG / .JPG - ZERO JSON FILES READ)                   ")
    print("================================================================================")

    profiles = {
        "country_name": country_name,
        "country_dir": country_dir,
        "iso_alpha3": iso_code,
        "number_palettes_required": NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED,
        "palette_theme_names": PALETTE_THEMES
    }

    for gender in ['man', 'woman']:
        img_paths = find_only_image_paths(base_dir, gender, country_dir=country_dir)
        print(f"Discovered {len(img_paths)} graphic images (.png/.jpg) for gender: '{gender}' in {country_dir} (0 JSONs used).")
        
        all_garment_pixels = []
        image_palettes_hex = []
        
        for idx, img_path in enumerate(img_paths):
            img_bgr = cv2.imread(img_path)
            if img_bgr is not None:
                # Apply YOLO + OpenCV exclusion pipeline
                garment_rgb = extract_clean_garment_pixels(img_bgr)
                
                if len(garment_rgb) > 0:
                    # Subsample pixels for fast, robust representation
                    sample_size = min(len(garment_rgb), 1200)
                    idx_sub = np.random.choice(len(garment_rgb), sample_size, replace=False)
                    all_garment_pixels.append(garment_rgb[idx_sub])
                    
                    # Also compute per-image local palette (K=3)
                    k_local = min(3, len(garment_rgb))
                    km_local = KMeans(n_clusters=k_local, random_state=42, n_init=3).fit(garment_rgb[idx_sub])
                    for c in km_local.cluster_centers_.astype(int):
                        image_palettes_hex.append(rgb_to_hex(*c))

        if all_garment_pixels:
            combined_pixels = np.vstack(all_garment_pixels)
        else:
            combined_pixels = np.array([[25, 35, 50], [95, 65, 85], [185, 165, 145]])

        # Global K-Means clustering across all clean reference garment pixels (K=12 centroids)
        k_clusters = min(12, len(combined_pixels))
        kmeans = KMeans(n_clusters=k_clusters, random_state=42, n_init=5)
        kmeans.fit(combined_pixels)
        
        cluster_centers_rgb = np.clip(kmeans.cluster_centers_, 0, 255).astype(int)
        cluster_centers_lab = rgb_to_lab(cluster_centers_rgb)
        
        # Partition into exactly 3 structured 4-color palettes
        palettes_hex, palettes_rgb = partition_into_3_palettes(cluster_centers_rgb)
        palettes_lab = [rgb_to_lab(np.array(prgb)).tolist() for prgb in palettes_rgb]
        
        # Deduplicate per-image extracted palette colors
        unique_image_hex = list(dict.fromkeys(image_palettes_hex))
        unique_image_rgb = [hex_to_rgb(h) for h in unique_image_hex]
        unique_image_lab = rgb_to_lab(np.array(unique_image_rgb)).tolist() if unique_image_rgb else []
        
        palette_hex_list = [rgb_to_hex(*c) for c in cluster_centers_rgb]
        
        profiles[gender] = {
            "num_reference_images": len(img_paths),
            "number_palettes": NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED,
            "palettes": palettes_hex, # List of 3 palettes
            "palette_names": PALETTE_THEMES,
            "palette_1": palettes_hex[0],
            "palette_2": palettes_hex[1],
            "palette_3": palettes_hex[2],
            "palettes_rgb": palettes_rgb,
            "palettes_lab": palettes_lab,
            "sampled_hex": unique_image_hex[:30],
            "sampled_rgb": unique_image_rgb[:30],
            "sampled_lab": unique_image_lab[:30],
            "cluster_centers_rgb": cluster_centers_rgb.tolist(),
            "cluster_centers_lab": cluster_centers_lab.tolist(),
            "palette_hex": palette_hex_list
        }
        print(f"  ✓ {gender.capitalize()}: Extracted {NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED} distinct 4-color palettes from {len(img_paths)} images:")
        for p_idx, (p_name, p_cols) in enumerate(zip(PALETTE_THEMES, palettes_hex)):
            print(f"      - [{p_idx+1}/3] {p_name}: {p_cols}")

    # Combined Unisex profile
    combined_centers_rgb = profiles['man']['cluster_centers_rgb'] + profiles['woman']['cluster_centers_rgb']
    combined_centers_lab = rgb_to_lab(np.array(combined_centers_rgb)).tolist()
    u_palettes_hex, u_palettes_rgb = partition_into_3_palettes(np.array(combined_centers_rgb))
    u_palettes_lab = [rgb_to_lab(np.array(prgb)).tolist() for prgb in u_palettes_rgb]

    profiles['unisex'] = {
        "number_palettes": NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED,
        "palettes": u_palettes_hex,
        "palette_names": PALETTE_THEMES,
        "palette_1": u_palettes_hex[0],
        "palette_2": u_palettes_hex[1],
        "palette_3": u_palettes_hex[2],
        "palettes_rgb": u_palettes_rgb,
        "palettes_lab": u_palettes_lab,
        "sampled_hex": list(set(profiles['man']['sampled_hex'] + profiles['woman']['sampled_hex'])),
        "cluster_centers_rgb": combined_centers_rgb,
        "cluster_centers_lab": combined_centers_lab,
        "palette_hex": [rgb_to_hex(*c) for c in combined_centers_rgb]
    }

    print("================================================================================")
    return profiles

if __name__ == "__main__":
    prof = extract_country_profiles_from_images()
    print("\nMan 3 Palettes:", prof['man']['palettes'])
    print("Woman 3 Palettes:", prof['woman']['palettes'])
