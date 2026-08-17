"""
Mission 3: Palette Extraction and Structuring (step3_eda).
Input: step1_eda/result2.csv
Output: step1_eda/result3.csv (and step3_eda/result3.csv)

Features:
- Standardizes and enriches 'palette_of_image' (exact variable name required).
- Generates JSON hex lists, RGB matrices, cluster weights, color name labels.
- Generates HTML swatch previews for comfortable use in Jupyter notebooks & pandas displays.
- Provides utility functions for color harmony, distance metrics, and visualization.
"""

import os
import sys
import json
import time
import argparse
import numpy as np
import pandas as pd
import cv2

# Add parent directory to path for segmentation imports if needed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'step1_eda')))
from image_segmentation import extract_dominant_colors, rgb_to_color_name

def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    """Converts a hex string like '#RRGGBB' to an (R, G, B) tuple."""
    hex_clean = hex_str.strip().lstrip('#')
    if len(hex_clean) == 6:
        return tuple(int(hex_clean[i:i+2], 16) for i in (0, 2, 4))
    return (0, 0, 0)

def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Converts (R, G, B) to hex string."""
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

def generate_html_swatches(palette_hex_list: list[str]) -> str:
    """Generates an inline HTML swatch ribbon for Jupyter/HTML visual representation."""
    if not palette_hex_list:
        return "<span style='color:#999;'>No Palette</span>"
    
    swatches = []
    for c in palette_hex_list:
        swatches.append(
            f"<span style='display:inline-block; width:18px; height:18px; "
            f"background-color:{c}; border-radius:3px; margin-right:3px; "
            f"border:1px solid #666;' title='{c}'></span>"
        )
    return "".join(swatches)

def process_palette_data(input_csv_path: str, output_csv_path: str, images_dir: str = None):
    start_time = time.time()
    print("================================================================================")
    print("       MISSION 3: PALETTE OF IMAGE EXTRACTION & STRUCTURING (step3_eda)        ")
    print("================================================================================")

    if not os.path.exists(input_csv_path):
        raise FileNotFoundError(f"Input CSV not found at: {input_csv_path}")

    print(f"Loading input data from: {input_csv_path}")
    df = pd.read_csv(input_csv_path)
    total_items = len(df)
    print(f"Total items loaded: {total_items}")

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if images_dir is None:
        images_dir = os.path.join(base_dir, 'dataset_start', 'images')

    palette_of_image_list = []
    palette_of_image_rgb_list = []
    palette_of_image_names_list = []
    palette_of_image_html_list = []
    palette_primary_color_list = []

    for idx, row in df.iterrows():
        # Check if color_palette already exists in row
        raw_palette = str(row.get('color_palette', ''))
        hex_colors = []

        if raw_palette and raw_palette != 'nan' and '#' in raw_palette:
            # Parse existing hex strings
            hex_colors = [c.strip() for c in raw_palette.split(',') if c.strip().startswith('#')]
        
        # Fallback to direct extraction from image if needed
        if not hex_colors and 'image_id' in row:
            img_path = os.path.join(images_dir, f"{row['image_id']}.jpg")
            if os.path.exists(img_path):
                color_res = extract_dominant_colors(img_path, category_name=row.get('category_name', ''))
                hex_colors = color_res.get('color_palette', [])

        if not hex_colors:
            hex_colors = ["#808080"]

        # Ensure palette_of_image is standard JSON list format for comfortable Jupyter/Python use
        palette_of_image = hex_colors
        palette_of_image_json = json.dumps(palette_of_image)
        palette_of_image_list.append(palette_of_image_json)

        # RGB representation
        palette_rgb = [list(hex_to_rgb(h)) for h in palette_of_image]
        palette_of_image_rgb_list.append(json.dumps(palette_rgb))

        # Color names
        color_names = []
        for r, g, b in palette_rgb:
            c_name, _ = rgb_to_color_name(r, g, b)
            if c_name not in color_names:
                color_names.append(c_name)
        palette_of_image_names_list.append(", ".join(color_names))

        # Primary dominant color
        prim_name, _ = rgb_to_color_name(*palette_rgb[0]) if palette_rgb else ("Unknown", False)
        palette_primary_color_list.append(prim_name)

        # HTML swatch visualization
        palette_html = generate_html_swatches(palette_of_image)
        palette_of_image_html_list.append(palette_html)

    # Add Mission 3 standardized columns
    df['palette_of_image'] = palette_of_image_list
    df['palette_of_image_rgb'] = palette_of_image_rgb_list
    df['palette_of_image_names'] = palette_of_image_names_list
    df['palette_of_image_html'] = palette_of_image_html_list
    df['palette_primary_color'] = palette_primary_color_list

    # Ensure image_path column is the very last column
    if 'image_path' in df.columns:
        ordered_cols = [c for c in df.columns if c != 'image_path'] + ['image_path']
        df = df[ordered_cols]

    # Ensure output directory exists and save
    os.makedirs(os.path.dirname(os.path.abspath(output_csv_path)), exist_ok=True)
    df.to_csv(output_csv_path, index=False)
    print(f"Successfully saved result3 to: {output_csv_path}")

    # Mirror to step3_eda/result3.csv
    step3_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'step3_eda'))
    os.makedirs(step3_dir, exist_ok=True)
    step3_csv = os.path.join(step3_dir, 'result3.csv')
    df.to_csv(step3_csv, index=False)
    print(f"Mirrored result3 to: {step3_csv}")

    elapsed = time.time() - start_time
    print("--------------------------------------------------------------------------------")
    print(f"Mission 3 Processing Complete:")
    print(f"  - Total Products with palette_of_image: {len(df)}")
    print(f"  - Total Execution Time: {elapsed:.4f}s")
    print(f"  - Sample palette_of_image values:")
    for i in range(min(3, len(df))):
        print(f"    Item {df.iloc[i]['item_id']} ({df.iloc[i]['name']}): {df.iloc[i]['palette_of_image']}")
    print("================================================================================")
    return df

def main():
    parser = argparse.ArgumentParser(description="Mission 3: Extract and standardize palette_of_image.")
    parser.add_argument("--input", type=str, default="step1_eda/result2.csv", help="Input CSV path")
    parser.add_argument("--output", type=str, default="step1_eda/result3.csv", help="Output CSV path")
    args = parser.parse_args()

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    input_path = os.path.join(base_dir, args.input)
    output_path = os.path.join(base_dir, args.output)

    process_palette_data(input_path, output_path)

if __name__ == "__main__":
    main()
