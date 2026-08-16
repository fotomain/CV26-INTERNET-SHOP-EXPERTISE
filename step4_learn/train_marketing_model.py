"""
Mission 4: Train Marketing Compatibility Model (step4_learn).
Input: step1_eda/result3.csv and step5_new_country/ images (.jpg/.png only, zero JSONs).
Number of Required Target Country Palettes: NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = 3.

Outputs:
- step4_learn/market_model.pkl & step4_learn/market_profile.json
- step4_dss/result5.csv (stored model evaluation data with 3-palette matching metrics)
"""

import os
import sys
import json
import pickle
import time
import argparse
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# Import extractor and constant
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from country_palette_extractor import (
    NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED,
    PALETTE_THEMES,
    extract_country_profiles_from_images,
    rgb_to_lab,
    hex_to_rgb,
    rgb_to_hex
)

class CountryMarketingSuitabilityModel:
    """
    Gender-aware Machine Learning model that evaluates whether a product's color palette
    aligns with consumer fashion preferences across NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = 3
    distinct country reference palettes.
    """
    def __init__(self, profiles: dict, delta_e_good_threshold: float = 14.0, score_threshold: float = 0.60):
        self.profiles = profiles
        self.delta_e_good_threshold = delta_e_good_threshold
        self.score_threshold = score_threshold
        self.country_name = profiles.get('country_name', 'United States')
        self.iso_alpha3 = profiles.get('iso_alpha3', 'USA')
        self.number_palettes_required = NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED
        self.palette_themes = PALETTE_THEMES
        
        # Build Nearest Neighbors models for each of the 3 palettes per gender
        self.gender_subpalette_models = {}
        self.global_models = {}

        for gender in ['man', 'woman', 'unisex']:
            g_prof = profiles[gender]
            self.gender_subpalette_models[gender] = []
            
            # Models for each individual palette (1, 2, 3)
            for p_idx in range(self.number_palettes_required):
                p_hex = g_prof['palettes'][p_idx]
                p_rgb = np.array([hex_to_rgb(h) for h in p_hex])
                p_lab = rgb_to_lab(p_rgb)
                
                nbrs = NearestNeighbors(n_neighbors=1, algorithm='auto', metric='euclidean').fit(p_lab)
                self.gender_subpalette_models[gender].append({
                    "palette_id": p_idx + 1,
                    "theme_name": self.palette_themes[p_idx],
                    "nbrs": nbrs,
                    "lab": p_lab,
                    "hex_list": p_hex
                })

            # Global gender model across all sampled and centroid colors
            lab_centers = np.array(g_prof['cluster_centers_lab'])
            if len(g_prof.get('sampled_lab', [])) > 0:
                sampled_lab = np.array(g_prof['sampled_lab'])
                combined_lab = np.vstack([lab_centers, sampled_lab])
            else:
                combined_lab = lab_centers
                
            global_nbrs = NearestNeighbors(n_neighbors=1, algorithm='auto', metric='euclidean').fit(combined_lab)
            self.global_models[gender] = (global_nbrs, combined_lab, g_prof['palette_hex'])

    def evaluate_palette(self, palette_hex_list: list[str], for_man: bool, for_woman: bool, for_unisex: bool, product_name: str = "") -> dict:
        """
        Evaluates a single product's palette against the target country's 3 distinct reference palettes.
        
        Returns:
            dict with decision metrics, best matching palette (1, 2, or 3), and 'product_is_good_for_new_marketing : bool'.
        """
        if not palette_hex_list:
            palette_hex_list = ["#808080"]

        # Determine target demographic
        if for_unisex or (for_man and for_woman):
            target_gender = 'unisex'
            segment_name = 'Unisex'
        elif for_man and not for_woman:
            target_gender = 'man'
            segment_name = 'Men'
        elif for_woman and not for_man:
            target_gender = 'woman'
            segment_name = 'Women'
        else:
            target_gender = 'unisex'
            segment_name = 'Unisex'

        product_rgb = np.array([hex_to_rgb(h) for h in palette_hex_list])
        product_lab = rgb_to_lab(product_rgb)

        # Evaluate fit against each of the 3 sub-palettes
        sub_results = []
        for p_model in self.gender_subpalette_models[target_gender]:
            nbrs = p_model['nbrs']
            distances, indices = nbrs.kneighbors(product_lab)
            min_dist = distances.flatten()
            
            p_dom_dist = float(min_dist[0])
            p_avg_dist = float(np.mean(min_dist))
            p_composite = 0.60 * p_dom_dist + 0.40 * p_avg_dist
            p_score = float(np.clip(np.exp(-p_composite / 20.0), 0.0, 1.0))
            
            best_swatch_idx = int(np.argmin(min_dist))
            best_target_color = p_model['hex_list'][min(int(indices[best_swatch_idx][0]), len(p_model['hex_list'])-1)]

            sub_results.append({
                "palette_id": p_model['palette_id'],
                "theme_name": p_model['theme_name'],
                "palette_colors": p_model['hex_list'],
                "composite_distance": p_composite,
                "score": p_score,
                "matched_color": best_target_color
            })

        # Select the best matching palette among the 3
        best_palette_match = min(sub_results, key=lambda x: x['composite_distance'])
        best_p_id = best_palette_match['palette_id']
        best_p_theme = best_palette_match['theme_name']
        best_p_colors = best_palette_match['palette_colors']
        composite_distance = best_palette_match['composite_distance']
        compatibility_score = best_palette_match['score']
        nearest_target_hex = best_palette_match['matched_color']

        # Marketing Decision Rule:
        is_good = bool(composite_distance <= self.delta_e_good_threshold and compatibility_score >= self.score_threshold)

        # Priority Tiers
        if compatibility_score >= 0.72 and composite_distance <= 10.0:
            tier = "Tier 1: Prime Marketing Candidate"
            reason = f"Excellent color match (ΔE={composite_distance:.1f}) for {segment_name} with {best_p_theme}."
        elif is_good:
            tier = "Tier 2: Standard Marketing Candidate"
            reason = f"Solid alignment (ΔE={composite_distance:.1f}, score={compatibility_score:.2f}) with {best_p_theme}."
        else:
            tier = "Tier 3: Non-Priority / Neutral"
            reason = f"Palette deviation (ΔE={composite_distance:.1f}) exceeds target country baseline."

        return {
            "market_compatibility_score": round(compatibility_score, 4),
            "market_palette_match_distance": round(composite_distance, 2),
            "product_is_good_for_new_marketing": is_good,
            "matched_target_color": nearest_target_hex,
            "matched_country_palette_id": best_p_id,
            "matched_country_palette_name": best_p_theme,
            "matched_country_palette_colors": json.dumps(best_p_colors),
            "target_gender_segment": segment_name,
            "marketing_priority_tier": tier,
            "dss_recommendation_reason": reason
        }

def train_and_export_model(base_dir: str = None, input_csv_path: str = None, country_dir: str = None, country_name: str = None, iso_code: str = None):
    if base_dir is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
    # Read defaults from run_settings.json if not specified
    settings_path = os.path.join(base_dir, 'run_settings.json')
    settings = {}
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
        except Exception:
            pass

    if country_dir is None:
        country_dir = settings.get('target_country_dir', 'step5_new_country')
    if country_name is None:
        country_name = settings.get('target_market_country', 'United States')
    if iso_code is None:
        iso_code = settings.get('target_market_iso', 'USA')

    if input_csv_path is None:
        input_csv_path = os.path.join(base_dir, 'step1_eda', 'result3.csv')

    start_time = time.time()
    print("================================================================================")
    print(f"       MISSION 4: TRAINING TARGET COUNTRY MARKETING COMPATIBILITY MODEL         ")
    print(f"       Target Country: {country_name} | Folder: {country_dir}                   ")
    print(f"       Required Palettes: NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = {NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED}")
    print("       (Excluding JSON files, YOLO + OpenCV Computer Vision Exclusions)         ")
    print("================================================================================")

    # 1. Extract 3 reference country palettes strictly from images
    profiles = extract_country_profiles_from_images(base_dir, country_dir=country_dir, country_name=country_name, iso_code=iso_code)

    # 2. Train and fit Model
    print("Fitting CIELAB Nearest Neighbor & 3-Palette Density Model...")
    model = CountryMarketingSuitabilityModel(profiles=profiles, delta_e_good_threshold=13.5, score_threshold=0.60)

    # 3. Save Model Artifacts
    step4_learn_dir = os.path.join(base_dir, 'step4_learn')
    os.makedirs(step4_learn_dir, exist_ok=True)
    
    model_pkl_path = os.path.join(step4_learn_dir, 'market_model.pkl')
    with open(model_pkl_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"✓ Saved trained model to: {model_pkl_path}")

    # Save JSON summary profile with 3 structured palettes
    profile_json_path = os.path.join(step4_learn_dir, 'market_profile.json')
    with open(profile_json_path, 'w', encoding='utf-8') as f:
        clean_prof = {
            "country_name": profiles['country_name'],
            "country_dir": profiles['country_dir'],
            "iso_alpha3": profiles['iso_alpha3'],
            "number_palettes_required": NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED,
            "palette_themes": PALETTE_THEMES,
            "man_palettes": {
                "palette_1": profiles['man']['palette_1'],
                "palette_2": profiles['man']['palette_2'],
                "palette_3": profiles['man']['palette_3'],
                "all_palettes": profiles['man']['palettes']
            },
            "woman_palettes": {
                "palette_1": profiles['woman']['palette_1'],
                "palette_2": profiles['woman']['palette_2'],
                "palette_3": profiles['woman']['palette_3'],
                "all_palettes": profiles['woman']['palettes']
            },
            "unisex_palettes": {
                "palette_1": profiles['unisex']['palette_1'],
                "palette_2": profiles['unisex']['palette_2'],
                "palette_3": profiles['unisex']['palette_3'],
                "all_palettes": profiles['unisex']['palettes']
            }
        }
        json.dump(clean_prof, f, indent=2)
    print(f"✓ Saved 3-palette country market profile JSON to: {profile_json_path}")

    # 4. Evaluate Input Catalog (result3.csv) and Export Model Data to step4_dss/result5.csv
    print(f"\nEvaluating catalog from: {input_csv_path}")
    if not os.path.exists(input_csv_path):
        raise FileNotFoundError(f"Input CSV not found: {input_csv_path}")
        
    df = pd.read_csv(input_csv_path)
    total_items = len(df)
    print(f"Loaded {total_items} items.")

    comp_scores = []
    distances = []
    is_good_list = []
    matched_colors = []
    matched_p_ids = []
    matched_p_names = []
    matched_p_colors = []
    target_segments = []
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

        comp_scores.append(res['market_compatibility_score'])
        distances.append(res['market_palette_match_distance'])
        is_good_list.append(res['product_is_good_for_new_marketing'])
        matched_colors.append(res['matched_target_color'])
        matched_p_ids.append(res['matched_country_palette_id'])
        matched_p_names.append(res['matched_country_palette_name'])
        matched_p_colors.append(res['matched_country_palette_colors'])
        target_segments.append(res['target_gender_segment'])
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

    # Save to step4_dss/result5.csv
    step4_dss_dir = os.path.join(base_dir, 'step4_dss')
    os.makedirs(step4_dss_dir, exist_ok=True)
    out_csv = os.path.join(step4_dss_dir, 'result5.csv')
    df_out.to_csv(out_csv, index=False)
    print(f"✓ Saved intermediate 3-palette model data to: {out_csv}")

    elapsed = time.time() - start_time
    good_count = sum(is_good_list)
    good_pct = (good_count / total_items) * 100 if total_items > 0 else 0

    print("--------------------------------------------------------------------------------")
    print(f"Model Training & Evaluation Summary:")
    print(f"  - Products Evaluated       : {total_items}")
    print(f"  - Good for New Marketing   : {good_count} ({good_pct:.1f}%)")
    print(f"  - Not Recommended          : {total_items - good_count} ({100 - good_pct:.1f}%)")
    print(f"  - Training & Inference Time: {elapsed:.3f}s")
    print("================================================================================")
    return df_out

def main():
    parser = argparse.ArgumentParser(description="Mission 4: Train target country marketing compatibility model.")
    parser.add_argument("--country-dir", type=str, default=None, help="Directory containing target country images (e.g. step5_new_country or usa_lib)")
    parser.add_argument("--country-name", type=str, default=None, help="Target country display name (e.g. 'United States')")
    parser.add_argument("--iso-code", type=str, default=None, help="Target country ISO code (e.g. 'USA')")
    args = parser.parse_args()

    train_and_export_model(country_dir=args.country_dir, country_name=args.country_name, iso_code=args.iso_code)

if __name__ == "__main__":
    main()
