"""
Decision Support System (DSS) Marketing Decision Engine (step5_dss).
Mission 5: Evaluates candidate products from step1_eda/result3.csv against
target market profiles using NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = 3 country reference palettes.

Outputs:
- step5_dss/result5.csv (Full DSS output)
- step5_dss/result_good_for_new_marketing.csv (Approved SKUs)
- step5_dss/result_not_good_for_new_marketing.csv (Excluded SKUs)
"""

import os
import sys
import json
import time
import pickle
import argparse
import pandas as pd
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'step4_learn'))
from train_marketing_model import CountryMarketingSuitabilityModel, train_and_export_model

def execute_dss_engine(input_csv_path: str = None, output_csv_path: str = None) -> pd.DataFrame:
    start_time = time.time()
    print("================================================================================")
    print("       MISSION 5: DECISION SUPPORT SYSTEM (DSS) DECISION ENGINE (step5_dss)     ")
    print("       Using NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = 3 Reference Palettes       ")
    print("================================================================================")

    if input_csv_path is None:
        input_csv_path = os.path.join(BASE_DIR, 'step1_eda', 'result3.csv')
    if output_csv_path is None:
        output_csv_path = os.path.join(BASE_DIR, 'step5_dss', 'result5.csv')

    model_pkl_path = os.path.join(BASE_DIR, 'step4_learn', 'market_model.pkl')

    # Load or train model
    if not os.path.exists(model_pkl_path):
        print(f"Market model not found at {model_pkl_path}. Initiating training...")
        train_and_export_model(base_dir=BASE_DIR, input_csv_path=input_csv_path)

    print(f"Loading trained Country Marketing Model from: {model_pkl_path}")
    with open(model_pkl_path, 'rb') as f:
        model = pickle.load(f)

    print(f"Target Market: {model.country_name} ({model.iso_alpha3})")
    print(f"Loading candidate product catalog from: {input_csv_path}")
    df = pd.read_csv(input_csv_path)
    total_items = len(df)
    print(f"Total candidate products: {total_items}")

    target_segments = []
    comp_scores = []
    distances = []
    matched_colors = []
    matched_p_ids = []
    matched_p_names = []
    matched_p_colors = []
    is_good_list = []
    tiers = []
    reasons = []

    for idx, row in df.iterrows():
        raw_pal = row.get('palette_of_image', '[]')
        try:
            pal_list = json.loads(raw_pal) if isinstance(raw_pal, str) and raw_pal.startswith('[') else [c.strip() for c in str(raw_pal).split(',') if '#' in c]
        except:
            pal_list = ["#808080"]

        res = model.evaluate_palette(
            palette_hex_list=pal_list,
            for_man=bool(row.get('for_man', False)),
            for_woman=bool(row.get('for_woman', False)),
            for_unisex=bool(row.get('for_unisex', False)),
            product_name=str(row.get('name', ''))
        )

        target_segments.append(res['target_gender_segment'])
        comp_scores.append(res['market_compatibility_score'])
        distances.append(res['market_palette_match_distance'])
        matched_colors.append(res['matched_target_color'])
        matched_p_ids.append(res.get('matched_country_palette_id', 1))
        matched_p_names.append(res.get('matched_country_palette_name', 'Palette 1 (Core & Classic Neutrals)'))
        matched_p_colors.append(res.get('matched_country_palette_colors', '[]'))
        is_good_list.append(res['product_is_good_for_new_marketing'])
        tiers.append(res['marketing_priority_tier'])
        reasons.append(res['dss_recommendation_reason'])

    df_out = df.copy()
    df_out['market_target_segment'] = target_segments
    df_out['market_compatibility_score'] = comp_scores
    df_out['market_palette_match_distance'] = distances
    df_out['matched_target_reference_color'] = matched_colors
    df_out['matched_country_palette_id'] = matched_p_ids
    df_out['matched_country_palette_name'] = matched_p_names
    df_out['matched_country_palette_colors'] = matched_p_colors
    df_out['product_is_good_for_new_marketing'] = is_good_list
    df_out['marketing_priority_tier'] = tiers
    df_out['dss_recommendation_reason'] = reasons

    # Ensure image_path column is the very last column in all CSV files
    if 'image_path' in df_out.columns:
        ordered_cols = [c for c in df_out.columns if c != 'image_path'] + ['image_path']
        df_out = df_out[ordered_cols]

    # Ensure output directory exists and save full result5.csv
    os.makedirs(os.path.dirname(os.path.abspath(output_csv_path)), exist_ok=True)
    df_out.to_csv(output_csv_path, index=False)
    print(f"✓ Saved full DSS result to: {output_csv_path}")

    # Generate dedicated Good vs Not Good subsets
    step5_dir = os.path.dirname(os.path.abspath(output_csv_path))
    good_csv_path = os.path.join(step5_dir, 'result_good_for_new_marketing.csv')
    not_good_csv_path = os.path.join(step5_dir, 'result_not_good_for_new_marketing.csv')

    df_good = df_out[df_out['product_is_good_for_new_marketing'] == True].copy()
    df_not_good = df_out[df_out['product_is_good_for_new_marketing'] == False].copy()

    df_good.to_csv(good_csv_path, index=False)
    df_not_good.to_csv(not_good_csv_path, index=False)
    print(f"✓ Saved Good Marketing subset to: {good_csv_path} ({len(df_good)} items)")
    print(f"✓ Saved Not Good Marketing subset to: {not_good_csv_path} ({len(df_not_good)} items)")

    # Mirror output to step1_eda/result5.csv
    step1_csv = os.path.join(BASE_DIR, 'step1_eda', 'result5.csv')
    df_out.to_csv(step1_csv, index=False)
    print(f"✓ Mirrored DSS results to: {step1_csv}")

    elapsed = time.time() - start_time
    good_count = len(df_good)
    good_pct = (good_count / total_items) * 100 if total_items > 0 else 0

    print("--------------------------------------------------------------------------------")
    print(f"DSS Evaluation Final Summary:")
    print(f"  - Total Products Evaluated       : {total_items}")
    print(f"  - Good for New Marketing (True)  : {good_count} ({good_pct:.1f}%)")
    print(f"  - Not Recommended (False)        : {len(df_not_good)} ({100 - good_pct:.1f}%)")
    print(f"  - Average Compatibility Score    : {df_out['market_compatibility_score'].mean():.4f}")
    print(f"  - Average Palette Match Distance : {df_out['market_palette_match_distance'].mean():.2f} ΔE")
    print(f"  - DSS Decision Execution Time    : {elapsed:.4f}s")
    print("================================================================================")
    return df_out

def main():
    parser = argparse.ArgumentParser(description="Mission 5: DSS Decision Engine for Marketing Suitability.")
    parser.add_argument("--input-csv", type=str, default=None, help="Path to input product catalog (result3.csv)")
    parser.add_argument("--output-csv", type=str, default=None, help="Path to output DSS decision catalog (result5.csv)")
    args = parser.parse_args()

    execute_dss_engine(input_csv_path=args.input_csv, output_csv_path=args.output_csv)

if __name__ == "__main__":
    main()
