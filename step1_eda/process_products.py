"""
Mission 1: Product Catalog Expertise & EDA Pipeline (step1_eda).
Inputs:
- dataset_start/GLAMI-1M-train.csv
- dataset_start/images/

Key Requirements:
- Fashion-MNIST Sequential classifier predicting 'product_class_name' (fallback: 'noclothes')
- Pure Python keyword-based gender tagging: for_man, for_woman, for_unisex
- Renames 'geo' field to 'produced_for_country'
- Exports full categories list to 'step1_eda/result_categories.csv'
- Stores output into 'step1_eda/result1.csv'
"""

import os
import sys
import time
import argparse
from datetime import datetime
import pandas as pd
import numpy as np

# Add step1_eda directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model_trainer import train_or_load_model, classify_product_image, class_names
from gender_classifier import classify_gender
from image_segmentation import extract_dominant_colors

class StepTimer:
    """Helper to track step durations."""
    def __init__(self):
        self.pipeline_start = time.time()
        self.step_start = time.time()
        self.step_history = []

    def start_step(self, step_name: str):
        self.step_start = time.time()
        print(f"\n>>> Starting Step: {step_name}")

    def end_step(self, step_name: str) -> float:
        elapsed = time.time() - self.step_start
        print(f"✓ Completed: {step_name} [{elapsed:.2f}s]")
        self.step_history.append((step_name, elapsed))
        return elapsed

def load_run_settings(base_dir):
    settings_file = os.path.join(base_dir, 'run_settings.json')
    if os.path.exists(settings_file):
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    settings = load_run_settings(base_dir)
    default_n_items = settings.get('DEFAULT_USE_FIRST_ITEMS', 200)

    parser = argparse.ArgumentParser(description="Mission 1: Process product catalog from dataset_start/.")
    parser.add_argument("--n-items", type=int, default=default_n_items, help=f"Number of product items to process (default: {default_n_items} from run_settings.json)")
    args = parser.parse_args()
    n_items = args.n_items

    timer = StepTimer()
    
    # Locate dataset_start directory
    data_csv_candidates = [
        os.path.join(base_dir, 'dataset_start', 'GLAMI-1M-train.csv'),
        os.path.join(base_dir, '..', 'dataset_start', 'GLAMI-1M-train.csv'),
        '/Users/mgtimber/CV26/dataset_start/GLAMI-1M-train.csv'
    ]
    data_csv_path = None
    for p in data_csv_candidates:
        if os.path.exists(p):
            data_csv_path = p
            break

    if data_csv_path is None:
        raise FileNotFoundError("Could not locate dataset_start/GLAMI-1M-train.csv")

    images_dir_candidates = [
        os.path.join(os.path.dirname(data_csv_path), 'images'),
        os.path.join(base_dir, 'dataset_start', 'images'),
        '/Users/mgtimber/CV26/dataset_start/images'
    ]
    images_dir = None
    for p in images_dir_candidates:
        if os.path.exists(p):
            images_dir = p
            break

    output_csv_path = os.path.join(base_dir, 'step1_eda', 'result1.csv')
    categories_csv_path = os.path.join(base_dir, 'step1_eda', 'result_categories.csv')

    print("================================================================================")
    print(f"      MISSION 1: INTERNET SHOP PRODUCT CATALOG EXPERTISE ({n_items} ITEMS)")
    print(f"      Input Data: {data_csv_path}")
    print(f"      Images Dir: {images_dir}")
    print("================================================================================")

    # -------------------------------------------------------------------------
    # STEP 1: Load Input Dataset & Export Full Categories List
    # -------------------------------------------------------------------------
    timer.start_step(f"1. Load Input Dataset (First {n_items} Products)")
    df = pd.read_csv(data_csv_path, nrows=n_items)
    print(f"Loaded {len(df)} products. Original Columns: {list(df.columns)}")

    # Rename geo -> produced_for_country
    if 'geo' in df.columns:
        df = df.rename(columns={'geo': 'produced_for_country'})
        print("✓ Renamed column: 'geo' -> 'produced_for_country'")

    # Export full categories list
    full_cats = df[['category', 'category_name']].drop_duplicates().sort_values('category').reset_index(drop=True)
    full_cats['category_count'] = df.groupby('category')['category'].transform('count')
    full_cats.to_csv(categories_csv_path, index=False)
    print(f"✓ Saved full categories list ({len(full_cats)} unique categories) to: {categories_csv_path}")
    timer.end_step("1. Load Input Dataset & Export Categories")

    # -------------------------------------------------------------------------
    # STEP 2: Train / Load Fashion-MNIST Sequential Classifier
    # -------------------------------------------------------------------------
    timer.start_step("2. Train / Load Fashion-MNIST Sequential Classifier")
    model = train_or_load_model(epochs=5)
    timer.end_step("2. Train / Load Fashion-MNIST Classifier")

    # -------------------------------------------------------------------------
    # STEP 3: Classify Images with Fashion-MNIST (with 'noclothes' fallback)
    # -------------------------------------------------------------------------
    timer.start_step("3. Product Image Classification (Fashion-MNIST inference)")
    product_classes = []
    clothes_class_words = []
    confidences = []

    for idx, row in df.iterrows():
        img_id = row['image_id']
        img_path = os.path.join(images_dir, f"{img_id}.jpg") if images_dir else ""
        
        pred_res = classify_product_image(model, img_path, category_name=row.get('category_name', ''))
        product_classes.append(pred_res['product_class_name'])
        clothes_class_words.append(pred_res['clothes_class_name_word'])
        confidences.append(pred_res['confidence'])

    df['clothes_class_name_word'] = clothes_class_words
    df['product_class_name'] = product_classes
    df['classification_confidence'] = confidences
    timer.end_step("3. Product Image Classification")

    # -------------------------------------------------------------------------
    # STEP 4: Gender Classification (Pure Python Keyword Matching)
    # -------------------------------------------------------------------------
    timer.start_step("4. Gender Tagging (for_man, for_woman, for_unisex)")
    for_man_list = []
    for_woman_list = []
    for_unisex_list = []

    for idx, row in df.iterrows():
        g_res = classify_gender(
            category_id=row.get('category'),
            category_name=row.get('category_name'),
            product_name=str(row.get('name', ''))
        )
        for_man_list.append(g_res['for_man'])
        for_woman_list.append(g_res['for_woman'])
        for_unisex_list.append(g_res['for_unisex'])

    df['for_man'] = for_man_list
    df['for_woman'] = for_woman_list
    df['for_unisex'] = for_unisex_list
    timer.end_step("4. Gender Tagging")

    # -------------------------------------------------------------------------
    # STEP 5: Color Extraction & Exclusions
    # -------------------------------------------------------------------------
    timer.start_step("5. True Garment Color Extraction & Visual Analysis")
    is_colored_list = []
    dom_color_list = []
    avg_sat_list = []
    avg_bright_list = []
    color_palette_list = []

    for idx, row in df.iterrows():
        img_id = row['image_id']
        img_path = os.path.join(images_dir, f"{img_id}.jpg") if images_dir else ""
        color_res = extract_dominant_colors(img_path, n_clusters=4, category_name=row.get('category_name', ''))

        is_colored_list.append(color_res['is_colored'])
        dom_color_list.append(color_res['dominant_color'])
        avg_sat_list.append(color_res['avg_saturation'])
        avg_bright_list.append(color_res['avg_brightness'])
        color_palette_list.append(color_res['color_palette'])

    df['is_colored'] = is_colored_list
    df['dominant_color'] = dom_color_list
    df['avg_saturation'] = avg_sat_list
    df['avg_brightness'] = avg_bright_list
    df['color_palette'] = color_palette_list
    timer.end_step("5. True Garment Color Extraction")

    # -------------------------------------------------------------------------
    # STEP 6: Save Output Dataset result1.csv
    # -------------------------------------------------------------------------
    timer.start_step("6. Save Output result1.csv")
    
    # Standard column order
    ordered_cols = [
        'item_id', 'image_id', 'produced_for_country', 'name', 'description',
        'category', 'category_name', 'clothes_class_name_word', 'product_class_name',
        'for_man', 'for_woman', 'for_unisex', 'is_colored', 'dominant_color',
        'avg_saturation', 'avg_brightness', 'color_palette', 'label_source',
        'classification_confidence'
    ]
    final_cols = [c for c in ordered_cols if c in df.columns] + [c for c in df.columns if c not in ordered_cols]
    if 'image_path' in final_cols:
        final_cols = [c for c in final_cols if c != 'image_path'] + ['image_path']
    df = df[final_cols]

    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df.to_csv(output_csv_path, index=False)
    print(f"✓ Saved {len(df)} processed items to: {output_csv_path}")
    timer.end_step("6. Save Output result1.csv")

    total_time = time.time() - timer.pipeline_start
    print("================================================================================")
    print(f"Mission 1 Completed Successfully in {total_time:.2f}s!")
    print(f"  - Output Dataset: {output_csv_path} ({len(df)} rows)")
    print(f"  - Categories List: {categories_csv_path} ({len(full_cats)} categories)")
    print(f"  - Gender Distribution: Men: {df['for_man'].sum()}, Women: {df['for_woman'].sum()}, Unisex: {df['for_unisex'].sum()}")
    print("================================================================================")
    return df

if __name__ == "__main__":
    main()
