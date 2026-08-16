"""
Mission 2: E-commerce Product Catalog Readiness Processing (step2_eda).
Input: step1_eda/result1.csv
Output: step1_eda/result2.csv (and step2_eda/result2.csv)

Rule:
- Pure Python logic (no neural networks / heavy models).
- Adds the 'ready_to_sale' boolean field.
- If the product name contains the product_class_name (or class keywords), ready_to_sale = True, otherwise False.
"""

import os
import sys
import time
import argparse
import unicodedata
import pandas as pd

# Class keyword mappings (multilingual Czech/English + normalized tokens)
CLASS_KEYWORD_MAP = {
    "t-shirt/top": [
        "t-shirt", "tshirt", "t shirt", "triko", "tričko", "top", "tee", "tank",
        "tílko", "trika", "trička", "t-shirty", "t-shirta", "crop top", "blůza", "polo", "polokošile"
    ],
    "trouser": [
        "trouser", "trousers", "pants", "kalhoty", "kraťasy", "shorts", "šortky",
        "legíny", "leggings", "jeans", "džíny", "tepláky", "slipy", "boxerky", "kalhotky"
    ],
    "pullover": [
        "pullover", "sweater", "svetr", "mikina", "sweatshirt", "jumper", "hoodie",
        "kardigan", "cardigan", "rolák", "pletený", "svetry", "mikiny"
    ],
    "dress": [
        "dress", "šaty", "sukně", "skirt", "večerní šaty", "letní šaty", "koktejlky",
        "šatičky", "sukně", "maxišaty", "pouzdrové šaty"
    ],
    "coat": [
        "coat", "kabát", "bunda", "jacket", "župan", "bathrobe", "vest", "vesta",
        "parka", "plášť", "sako", "blejzr", "blazer", "větrovka", "pončo", "kabátky", "bundy"
    ],
    "sandal": [
        "sandal", "sandals", "sandály", "sandálky", "flip-flops", "žabky", "slides",
        "pantofle", "papuče", "podpatky", "heels", "lodičky", "espadrilky", "espadrilles", "nazouváky"
    ],
    "shirt": [
        "shirt", "shirts", "košile", "halenka", "blouse", "blůzka", "košilka", "polokošile"
    ],
    "sneaker": [
        "sneaker", "sneakers", "boty", "tenisky", "shoes", "polobotky", "kecky",
        "běžecké boty", "cvičky", "teniska", "mokasíny"
    ],
    "bag": [
        "bag", "bags", "taška", "kabelka", "batoh", "backpack", "wallet", "peněženka",
        "psaníčko", "vak", "brašna", "kufřík", "pouzdro", "hodinky", "watch", "náušnice",
        "earring", "šperk", "náramek", "řetízek", "prsten"
    ],
    "ankle boot": [
        "boot", "boots", "kozačky", "kotníkové boty", "ankle boot", "válenky",
        "sněhule", "chelsea", "perka", "holínky"
    ]
}

def normalize_text(text: str) -> str:
    """Normalizes text by lowercasing and removing accents for robust matching."""
    if not isinstance(text, str):
        return ""
    text_lower = text.lower()
    # Normalize unicode to remove diacritics
    nfkd = unicodedata.normalize('NFKD', text_lower)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

def check_ready_to_sale(product_name: str, product_class_name: str) -> tuple[bool, str]:
    """
    Evaluates whether a product is ready to sale based on product name containing product class name.
    
    Returns:
        tuple (is_ready_to_sale: bool, match_reason: str)
    """
    if not isinstance(product_name, str) or not product_name.strip():
        return False, "Empty product name"
    
    if not isinstance(product_class_name, str) or not product_class_name.strip():
        return False, "Missing product class"

    name_norm = normalize_text(product_name)
    class_raw_norm = normalize_text(product_class_name)
    class_key = product_class_name.lower().strip()

    # 1. Exact raw substring match
    if class_raw_norm in name_norm:
        return True, f"Exact class substring '{product_class_name}' found in name"
    
    # 2. Check individual slash-separated words (e.g., 't-shirt' or 'top' from 'T-shirt/top')
    for part in product_class_name.split('/'):
        part_norm = normalize_text(part.strip())
        if len(part_norm) >= 3 and part_norm in name_norm:
            return True, f"Class component '{part.strip()}' found in name"

    # 3. Multilingual keyword / semantic lookup
    keywords = CLASS_KEYWORD_MAP.get(class_key, [])
    for kw in keywords:
        kw_norm = normalize_text(kw)
        if kw_norm and kw_norm in name_norm:
            return True, f"Relevant keyword '{kw}' found in name"

    return False, "Product class not explicitly described in name"

def process_ready_to_sale(input_csv_path: str, output_csv_path: str):
    start_time = time.time()
    print("================================================================================")
    print("       MISSION 2: PRODUCT CATALOG READINESS (ready_to_sale EVALUATION)         ")
    print("================================================================================")
    
    # Check input path with fallback
    if not os.path.exists(input_csv_path):
        alt_path = input_csv_path.replace("step1_eda", "step1_eda_")
        if os.path.exists(alt_path):
            input_csv_path = alt_path
        else:
            raise FileNotFoundError(f"Input file not found at: {input_csv_path}")

    print(f"Loading input data from: {input_csv_path}")
    df = pd.read_csv(input_csv_path)
    total_items = len(df)
    print(f"Total items to process: {total_items}")

    ready_to_sale_list = []
    reasons_list = []

    for idx, row in df.iterrows():
        p_name = row.get('name', '')
        p_class = row.get('product_class_name', row.get('clothes_class_name_word', ''))
        
        is_ready, reason = check_ready_to_sale(p_name, p_class)
        ready_to_sale_list.append(is_ready)
        reasons_list.append(reason)

    df['ready_to_sale'] = ready_to_sale_list
    df['ready_to_sale_reason'] = reasons_list

    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_csv_path)), exist_ok=True)
    df.to_csv(output_csv_path, index=False)
    print(f"Successfully saved result to: {output_csv_path}")

    # Also mirror to step2_eda/result2.csv for local accessibility
    step2_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'step2_eda'))
    os.makedirs(step2_dir, exist_ok=True)
    step2_csv = os.path.join(step2_dir, 'result2.csv')
    df.to_csv(step2_csv, index=False)
    print(f"Mirrored result to: {step2_csv}")

    elapsed = time.time() - start_time
    ready_count = df['ready_to_sale'].sum()
    ready_pct = (ready_count / total_items) * 100 if total_items > 0 else 0

    print("--------------------------------------------------------------------------------")
    print(f"Summary Statistics:")
    print(f"  - Total Products Processed : {total_items}")
    print(f"  - Ready to Sale (True)     : {ready_count} ({ready_pct:.1f}%)")
    print(f"  - Not Ready to Sale (False): {total_items - ready_count} ({100 - ready_pct:.1f}%)")
    print(f"  - Processing Time          : {elapsed:.4f} seconds ({elapsed/total_items*1000:.2f} ms/item)")
    print("--------------------------------------------------------------------------------")
    print("Ready to Sale Breakdown by Product Class:")
    breakdown = df.groupby('product_class_name')['ready_to_sale'].agg(['count', 'sum'])
    breakdown['ready_pct'] = (breakdown['sum'] / breakdown['count'] * 100).round(1)
    breakdown.columns = ['Total', 'Ready to Sale', 'Ready (%)']
    print(breakdown.sort_values('Total', ascending=False).to_string())
    print("================================================================================")
    return df

def main():
    parser = argparse.ArgumentParser(description="Mission 2: Add ready_to_sale field to product catalog.")
    parser.add_argument("--input", type=str, default="step1_eda/result1.csv", help="Input CSV path")
    parser.add_argument("--output", type=str, default="step1_eda/result2.csv", help="Output CSV path")
    args = parser.parse_args()

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    input_path = os.path.join(base_dir, args.input)
    output_path = os.path.join(base_dir, args.output)

    process_ready_to_sale(input_path, output_path)

if __name__ == "__main__":
    main()
