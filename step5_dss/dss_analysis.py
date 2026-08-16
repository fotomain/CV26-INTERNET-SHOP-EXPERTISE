"""
DSS Analysis and Summary Report Generator (step5_dss).
Generates step5_dss/dss_summary_report.md based on step5_dss/result5.csv.
"""

import os
import json
import pandas as pd
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def generate_dss_report(result5_path: str = None, report_output_path: str = None):
    if result5_path is None:
        result5_path = os.path.join(BASE_DIR, 'step5_dss', 'result5.csv')
    if report_output_path is None:
        report_output_path = os.path.join(BASE_DIR, 'step5_dss', 'dss_summary_report.md')

    # Load country settings
    settings_path = os.path.join(BASE_DIR, 'run_settings.json')
    country_name = "United States"
    iso_code = "USA"
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
                country_name = cfg.get('target_market_country', country_name)
                iso_code = cfg.get('target_market_iso', iso_code)
        except Exception:
            pass

    df = pd.read_csv(result5_path)
    total_items = len(df)
    good_items = df['product_is_good_for_new_marketing'].sum()
    good_pct = (good_items / total_items) * 100
    
    # Priority tiers
    tier_counts = df['marketing_priority_tier'].value_counts()

    # 3-Palette breakdown
    palette_breakdown = {}
    if 'matched_country_palette_name' in df.columns:
        p_counts = df['matched_country_palette_name'].value_counts()
        for p_name, p_cnt in p_counts.items():
            palette_breakdown[p_name] = {
                "count": int(p_cnt),
                "share": round((p_cnt / total_items) * 100, 1)
            }
    
    # Category summary
    cat_summary = df.groupby('product_class_name').agg(
        total=('item_id', 'count'),
        good=('product_is_good_for_new_marketing', 'sum'),
        avg_score=('market_compatibility_score', 'mean'),
        avg_dist=('market_palette_match_distance', 'mean')
    ).reset_index()
    cat_summary['good_pct'] = (cat_summary['good'] / cat_summary['total'] * 100).round(1)
    cat_summary['avg_score'] = cat_summary['avg_score'].round(3)
    cat_summary['avg_dist'] = cat_summary['avg_dist'].round(1)
    cat_summary = cat_summary.sort_values('total', ascending=False)

    # Gender summary
    gender_summary = df.groupby('market_target_segment').agg(
        total=('item_id', 'count'),
        good=('product_is_good_for_new_marketing', 'sum'),
        avg_score=('market_compatibility_score', 'mean')
    ).reset_index()
    gender_summary['good_pct'] = (gender_summary['good'] / gender_summary['total'] * 100).round(1)
    gender_summary['avg_score'] = gender_summary['avg_score'].round(3)

    md_lines = [
        f"# Decision Support System (DSS) Report: {country_name} ({iso_code}) Marketing Suitability",
        "",
        f"**Target Market**: {country_name} ({iso_code})  ",
        f"**Number of Target Palettes Used**: `NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = 3`  ",
        f"**Catalog Sample Size**: {total_items} items  ",
        f"**Products Recommended for Marketing (`product_is_good_for_new_marketing = True`)**: **{good_items} / {total_items} ({good_pct:.1f}%)**  ",
        f"**Average Market Compatibility Score**: `{df['market_compatibility_score'].mean():.3f}`  ",
        f"**Average Color Distance to Target Palettes**: `{df['market_palette_match_distance'].mean():.1f} ΔE`  ",
        "",
        "---",
        "",
        "## 1. Executive Summary & 3-Palette Fashion Alignment",
        "",
        f"The Decision Support System evaluated candidate catalog items against {country_name}'s image-derived fashion palettes across 3 distinct aesthetic clusters:",
        ""
    ]

    for p_name, p_info in palette_breakdown.items():
        md_lines.append(f"- **{p_name}**: **{p_info['count']} SKUs ({p_info['share']}%)** matched as best stylistic fit.")

    md_lines.extend([
        "",
        "| Marketing Priority Tier | Product Count | Share of Catalog (%) | Recommendation |",
        "| :--- | :---: | :---: | :--- |"
    ])

    for tier_name, count in tier_counts.items():
        pct = (count / total_items) * 100
        rec = "Immediate Hero Product Ads & Paid Acquisition" if "Tier 1" in tier_name else ("Standard Catalog Inclusion" if "Tier 2" in tier_name else "Organic / Secondary Listing Only")
        md_lines.append(f"| **{tier_name}** | {count} | {pct:.1f}% | {rec} |")

    md_lines.extend([
        "",
        "---",
        "",
        "## 2. Market Suitability Breakdown by Demographic Segment",
        "",
        "| Target Segment | Total Items | Recommended for Marketing | Suitability (%) | Mean Compatibility Score |",
        "| :--- | :---: | :---: | :---: | :---: |"
    ])

    for idx, row in gender_summary.iterrows():
        md_lines.append(
            f"| **{row['market_target_segment']}** | {row['total']} | {row['good']} | **{row['good_pct']}%** | {row['avg_score']} |"
        )

    md_lines.extend([
        "",
        "---",
        "",
        "## 3. Market Suitability Breakdown by Fashion Category",
        "",
        "| Fashion Category (`product_class_name`) | Total Items | Recommended for Marketing | Suitability (%) | Mean Distance (ΔE) | Mean Score |",
        "| :--- | :---: | :---: | :---: | :---: | :---: |"
    ])

    for idx, row in cat_summary.iterrows():
        md_lines.append(
            f"| **{row['product_class_name']}** | {row['total']} | {row['good']} | **{row['good_pct']}%** | {row['avg_dist']} ΔE | {row['avg_score']} |"
        )

    md_lines.extend([
        "",
        "---",
        "",
        "## 4. Top Recommended Products for Marketing Launch",
        "",
        "| Item ID | Product Name | Category | Matched Palette | Compatibility Score | Readiness |",
        "| :---: | :--- | :--- | :--- | :---: | :---: |"
    ])

    top_products = df.sort_values('market_compatibility_score', ascending=False).head(8)
    for idx, row in top_products.iterrows():
        r_status = "Ready" if row['ready_to_sale'] else "Unready"
        p_theme = row.get('matched_country_palette_name', 'Palette 1')
        md_lines.append(
            f"| `{row['item_id']}` | **{str(row['name'])[:35]}** | {row['product_class_name']} | {p_theme} | `{row['market_compatibility_score']:.3f}` | {r_status} |"
        )

    md_lines.extend([
        "",
        "---",
        "",
        "## 5. Strategic Merchandising & Campaign Directives",
        "",
        "1. **Launch Paid Search with Tier 1 Products**: Focus ad spend on the top-matching SKUs with high compatibility scores (>0.72).",
        f"2. **Feature Palette 1 & 2 in Core Collections**: Ensure core neutral and contemporary earthy streetwear hero SKUs lead collection landing pages.",
        "3. **Combine `ready_to_sale` and `product_is_good_for_new_marketing`**: Ensure products approved for marketing also have complete catalog metadata (`ready_to_sale = True`) before syndicating feeds.",
        ""
    ])

    report_content = "\n".join(md_lines)
    with open(report_output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    print(f"✓ Saved DSS Summary Report to: {report_output_path}")

if __name__ == "__main__":
    generate_dss_report()
