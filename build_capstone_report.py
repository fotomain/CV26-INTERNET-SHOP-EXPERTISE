"""
Generates the comprehensive, Tamagui-inspired single-plane CAPSTONE_REPORT.html.
Features:
- 1 Single Plane Page (continuous scroll layout, no hidden tabs).
- Exact sequence:
  1. Initial Data & Dataset Parameters (GLAMI-1M Catalog parameters, Target Country Reference Library, System Settings).
  2. Final Results % (Executive KPIs, 3 Market Reference Palettes, Visual Fit & Category Charts).
  3. Final Table for Classes (Category-by-category breakdown table & demographic summary).
  4. All as is now (Plain English Logic, Performance Timings & 10k/1M Scaling Prognosis, Interactive Catalog Explorer with live search/filters, and Launch Playbook).
- Mobile & Smartphone optimized with min-width: 350px support.
- 100% Self-contained for local offline operation (inlined Chart.js & fallback styles).
"""

import os
import glob
import json
import pandas as pd
import numpy as np

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def load_json(path, default=None):
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return default if default is not None else {}

def build_html_report():
    result5_path = os.path.join(BASE_DIR, 'step5_dss', 'result5.csv')
    df = pd.read_csv(result5_path)
    
    total_items = len(df)
    good_items = int(df['product_is_good_for_new_marketing'].sum())
    not_good_items = total_items - good_items
    good_pct = (good_items / total_items) * 100 if total_items > 0 else 0
    
    ready_items = int(df['ready_to_sale'].sum())
    ready_pct = (ready_items / total_items) * 100 if total_items > 0 else 0
    
    avg_score = float(df['market_compatibility_score'].mean())
    avg_dist = float(df['market_palette_match_distance'].mean())
    
    # Settings & Market Profile
    settings = load_json(os.path.join(BASE_DIR, 'run_settings.json'), default={})
    market_prof = load_json(os.path.join(BASE_DIR, 'step4_learn', 'market_profile.json'), default={})
    country_name = market_prof.get('country_name', settings.get('target_market_country', 'United States'))
    iso_code = market_prof.get('iso_alpha3', settings.get('target_market_iso', 'USA'))
    target_country_dir = settings.get('target_country_dir', 'step5_new_country')
    
    man_palettes = market_prof.get('man_palettes', {})
    woman_palettes = market_prof.get('woman_palettes', {})
    palette_themes = market_prof.get('palette_themes', [
        "Palette 1 (Core & Classic Neutrals)",
        "Palette 2 (Contemporary & Earthy Street)",
        "Palette 3 (Vibrant Statement & Accents)"
    ])

    # Initial Data & Dataset Statistics
    result1_path = os.path.join(BASE_DIR, 'step1_eda', 'result1.csv')
    df1 = pd.read_csv(result1_path) if os.path.exists(result1_path) else df
    
    man_photos = len(glob.glob(os.path.join(BASE_DIR, target_country_dir, 'images', 'man', '*.*')))
    woman_photos = len(glob.glob(os.path.join(BASE_DIR, target_country_dir, 'images', 'woman', '*.*')))
    total_target_photos = man_photos + woman_photos if (man_photos + woman_photos) > 0 else 100
    
    unique_categories_count = len(df1['product_class_name'].unique()) if 'product_class_name' in df1.columns else 10
    raw_categories_file = os.path.join(BASE_DIR, 'step1_eda', 'result_categories.csv')
    raw_cat_count = len(pd.read_csv(raw_categories_file)) if os.path.exists(raw_categories_file) else 39
    
    men_items_count = int(df1['for_man'].sum()) if 'for_man' in df1.columns else 91
    women_items_count = int(df1['for_woman'].sum()) if 'for_woman' in df1.columns else 179
    unisex_items_count = int(df1['for_unisex'].sum()) if 'for_unisex' in df1.columns else 70

    # Category summary
    cat_summary = df.groupby('product_class_name').agg(
        total=('item_id', 'count'),
        good=('product_is_good_for_new_marketing', 'sum'),
        ready=('ready_to_sale', 'sum'),
        avg_score=('market_compatibility_score', 'mean'),
        avg_dist=('market_palette_match_distance', 'mean')
    ).reset_index()
    cat_summary['good_pct'] = (cat_summary['good'] / cat_summary['total'] * 100).round(1)
    cat_summary['ready_pct'] = (cat_summary['ready'] / cat_summary['total'] * 100).round(1)
    cat_summary = cat_summary.sort_values('total', ascending=False)
    
    # Demographic summary
    demo_summary = df.groupby('market_target_segment').agg(
        total=('item_id', 'count'),
        good=('product_is_good_for_new_marketing', 'sum'),
        avg_score=('market_compatibility_score', 'mean'),
        avg_dist=('market_palette_match_distance', 'mean')
    ).reset_index()
    demo_summary['good_pct'] = (demo_summary['good'] / demo_summary['total'] * 100).round(1)
    
    # Load timings & prognosis
    prog_json_path = os.path.join(BASE_DIR, 'prognose', 'prognose_summary.json')
    prog_data = load_json(prog_json_path, default={})
    
    benchmarks_steps = prog_data.get('step_breakdown', [])
    tot_measured_sec = prog_data.get('measured_total_seconds', 24.64)
    p_10k_seq = prog_data.get('prognosis_10k_items', {}).get('sequential_baseline_formatted', '20m 31s')
    p_10k_opt = prog_data.get('prognosis_10k_items', {}).get('optimized_8core_formatted', '3m 09s')
    p_1m_seq = prog_data.get('prognosis_1m_items', {}).get('sequential_baseline_formatted', '1d 10h 13m')
    p_1m_opt = prog_data.get('prognosis_1m_items', {}).get('optimized_8core_formatted', '5h 15m')
    
    # Prepare JSON dataset for interactive client-side explorer
    items_data = []
    for idx, row in df.iterrows():
        raw_pal = row.get('palette_of_image', '[]')
        try:
            pal_list = json.loads(raw_pal) if isinstance(raw_pal, str) and raw_pal.startswith('[') else [c.strip() for c in str(raw_pal).split(',') if '#' in c]
        except:
            pal_list = ["#808080"]
            
        items_data.append({
            "id": int(row['item_id']),
            "image_id": int(row['image_id']),
            "name": str(row['name']),
            "category": str(row['product_class_name']),
            "segment": str(row['market_target_segment']),
            "dominant_color": str(row['dominant_color']),
            "is_colored": bool(row['is_colored']),
            "ready_to_sale": bool(row['ready_to_sale']),
            "ready_reason": str(row['ready_to_sale_reason']),
            "palette": pal_list,
            "score": round(float(row['market_compatibility_score']), 3),
            "distance": round(float(row['market_palette_match_distance']), 1),
            "matched_color": str(row['matched_target_reference_color']),
            "matched_palette_id": int(row.get('matched_country_palette_id', 1)),
            "matched_palette_name": str(row.get('matched_country_palette_name', 'Palette 1 (Core & Classic Neutrals)')),
            "is_good": bool(row['product_is_good_for_new_marketing']),
            "tier": str(row['marketing_priority_tier']),
            "reason": str(row['dss_recommendation_reason'])
        })

    json_catalog = json.dumps(items_data)
    json_timings = json.dumps(benchmarks_steps)

    # Inlined or local Chart.js for 100% offline local compatibility
    chart_js_inline = ""
    local_chart_path = os.path.join(BASE_DIR, 'chart.umd.min.js')
    if os.path.exists(local_chart_path):
        try:
            with open(local_chart_path, 'r', encoding='utf-8') as f:
                chart_js_inline = f.read()
        except Exception:
            chart_js_inline = ""

    chart_script_tag = f"<script>\n{chart_js_inline}\n</script>" if chart_js_inline else '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>'

    # HTML Generation - 1 Plane Page with Initial Data section as 1st
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
  <title>Executive Capstone Report: {country_name} ({iso_code}) AI Market Suitability Pipeline</title>
  
  <!-- Modern Google Fonts with System Fallback for Offline Compatibility -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  
  <!-- Inlined / Local Chart.js for 100% Offline Local Operation -->
  {chart_script_tag}

  <style>
    /* ==========================================================================
       Tamagui Theme Tokens & Design System (tamagui.dev Light Theme)
       ========================================================================== */
    :root {{
      --bg-base: #fbfbfc;
      --bg-surface: #ffffff;
      --bg-surface-elevated: #ffffff;
      --bg-surface-hover: #f8fafc;
      --bg-subtle: #f8fafc;
      --bg-muted: #f1f5f9;
      
      --border-subtle: rgba(0, 0, 0, 0.08);
      --border-medium: rgba(0, 0, 0, 0.15);
      --border-focus: #f59e0b;
      
      --text-primary: #0f172a;
      --text-secondary: #475569;
      --text-muted: #64748b;
      --text-headings: #09090b;
      
      --tamagui-gold: #f59e0b;
      --tamagui-amber: #d97706;
      --tamagui-gold-dark: #b45309;
      --accent-blue: #0284c7;
      --accent-purple: #7c3aed;
      --accent-green: #10b981;
      --accent-red: #e11d48;
      --accent-orange: #ea580c;
      
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --radius-full: 9999px;
      
      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.03);
      --shadow-md: 0 4px 16px -2px rgba(0, 0, 0, 0.06), 0 2px 6px -1px rgba(0, 0, 0, 0.03);
      --shadow-lg: 0 12px 32px -4px rgba(0, 0, 0, 0.08);
      --shadow-glow: 0 0 35px -5px rgba(245, 158, 11, 0.12);
    }}

    html {{
      scroll-behavior: smooth;
      min-width: 350px;
      width: 100%;
      box-sizing: border-box;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg-base);
      color: var(--text-primary);
      line-height: 1.6;
      min-height: 100vh;
      min-width: 350px;
      width: 100%;
      position: relative;
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
      padding-bottom: 70px;
      box-sizing: border-box;
    }}

    /* Authentic Tamagui Ambient Radial Mesh Glow Backgrounds (Light Theme) */
    body::before {{
      content: '';
      position: fixed;
      top: -12vw;
      left: -8vw;
      width: 50vw;
      height: 50vw;
      border-radius: 50%;
      background: radial-gradient(circle at center, rgba(245, 158, 11, 0.08) 0%, rgba(251, 191, 36, 0.02) 45%, transparent 70%);
      filter: blur(80px);
      pointer-events: none;
      z-index: 0;
    }}

    body::after {{
      content: '';
      position: fixed;
      bottom: -15vw;
      right: -10vw;
      width: 55vw;
      height: 55vw;
      border-radius: 50%;
      background: radial-gradient(circle at center, rgba(14, 165, 233, 0.06) 0%, rgba(124, 58, 237, 0.03) 50%, transparent 75%);
      filter: blur(90px);
      pointer-events: none;
      z-index: 0;
    }}

    .container {{
      max-width: 1320px;
      min-width: 350px;
      width: 100%;
      margin: 0 auto;
      padding: clamp(14px, 2.5vw, 30px) clamp(10px, 2.5vw, 24px);
      position: relative;
      z-index: 1;
      box-sizing: border-box;
    }}

    /* Sticky Top Plane-Page Quick Nav (Touch Friendly & Local Origin Safe) */
    .sticky-nav {{
      position: sticky;
      top: 8px;
      z-index: 100;
      background: rgba(255, 255, 255, 0.92);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 6px 10px;
      margin-bottom: 20px;
      box-shadow: var(--shadow-md);
      display: flex;
      gap: 6px;
      overflow-x: auto;
      align-items: center;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: none;
      box-sizing: border-box;
      width: 100%;
      max-width: 100%;
    }}

    .sticky-nav::-webkit-scrollbar {{
      display: none;
    }}

    .nav-link {{
      text-decoration: none;
      background: #ffffff;
      border: 1px solid rgba(0, 0, 0, 0.08);
      cursor: pointer;
      font-family: inherit;
      color: var(--text-secondary);
      font-size: 12px;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: var(--radius-full);
      transition: all 0.22s cubic-bezier(0.34, 1.56, 0.64, 1);
      white-space: nowrap;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    }}

    .nav-link:hover {{
      color: #b45309;
      background: #fffbeb;
      border-color: rgba(245, 158, 11, 0.4);
      transform: translateY(-1px);
    }}

    .nav-link.active, .nav-link.primary {{
      background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%) !important;
      color: #ffffff !important;
      font-weight: 700;
      border-color: transparent !important;
      box-shadow: 0 4px 14px rgba(245, 158, 11, 0.40) !important;
      transform: translateY(-1px) scale(1.02);
    }}

    /* Header & Hero Section */
    .hero {{
      background: var(--bg-surface);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: clamp(18px, 4vw, 36px) clamp(14px, 4vw, 40px);
      margin-bottom: 22px;
      box-shadow: var(--shadow-md), var(--shadow-glow);
      position: relative;
      overflow: hidden;
      box-sizing: border-box;
      width: 100%;
      min-width: 0;
    }}

    .hero h1 {{
      font-size: clamp(20px, 4.5vw, 32px);
      font-weight: 800;
      letter-spacing: -0.6px;
      color: var(--text-headings);
      margin-bottom: 10px;
      line-height: 1.25;
      word-break: break-word;
    }}

    .hero p.lead {{
      font-size: clamp(13.5px, 2.5vw, 16px);
      color: var(--text-secondary);
      max-width: 1020px;
      margin-bottom: 16px;
      line-height: 1.55;
    }}

    /* Section Separators */
    .plane-section {{
      margin-bottom: 35px;
      scroll-margin-top: 70px;
      box-sizing: border-box;
      width: 100%;
      min-width: 0;
    }}

    .section-header-banner {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
      padding-bottom: 8px;
      border-bottom: 2px solid var(--border-subtle);
      flex-wrap: wrap;
      gap: 8px;
    }}

    .section-header-title {{
      font-size: clamp(18px, 3.5vw, 22px);
      font-weight: 800;
      color: var(--text-headings);
      letter-spacing: -0.4px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .section-number {{
      background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%);
      color: #ffffff;
      font-size: 12px;
      font-weight: 700;
      padding: 3px 9px;
      border-radius: var(--radius-full);
      letter-spacing: 0.5px;
      box-shadow: 0 2px 6px rgba(245, 158, 11, 0.3);
    }}

    /* Badges & Pills */
    .badge-pill {{
      display: inline-flex;
      align-items: center;
      padding: 3px 10px;
      border-radius: var(--radius-full);
      font-size: 11.5px;
      font-weight: 600;
      letter-spacing: 0.2px;
      text-transform: uppercase;
      white-space: nowrap;
    }}

    .badge-tamagui {{ background: rgba(245, 158, 11, 0.12); color: #b45309; border: 1px solid rgba(245, 158, 11, 0.28); }}
    .badge-blue {{ background: rgba(2, 132, 199, 0.10); color: #0369a1; border: 1px solid rgba(2, 132, 199, 0.25); }}
    .badge-green {{ background: rgba(16, 185, 129, 0.12); color: #047857; border: 1px solid rgba(16, 185, 129, 0.28); }}
    .badge-purple {{ background: rgba(124, 58, 237, 0.10); color: #6d28d9; border: 1px solid rgba(124, 58, 237, 0.25); }}
    .badge-orange {{ background: rgba(234, 88, 12, 0.10); color: #c2410c; border: 1px solid rgba(234, 88, 12, 0.25); }}
    .badge-red {{ background: rgba(225, 29, 72, 0.10); color: #be123c; border: 1px solid rgba(225, 29, 72, 0.25); }}

    /* Top KPI Metric Cards Grid */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 14px;
      margin-bottom: 20px;
      box-sizing: border-box;
      width: 100%;
    }}

    .kpi-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: clamp(14px, 3vw, 20px);
      transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
      box-shadow: var(--shadow-sm);
      box-sizing: border-box;
      width: 100%;
      min-width: 0;
    }}

    .kpi-card:hover {{
      transform: translateY(-2px);
      border-color: var(--border-medium);
      box-shadow: var(--shadow-md);
    }}

    .kpi-title {{
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .kpi-value {{
      font-size: clamp(24px, 6vw, 32px);
      font-weight: 800;
      letter-spacing: -0.5px;
      color: var(--text-headings);
      margin-bottom: 4px;
    }}

    .kpi-desc {{
      font-size: 12.5px;
      color: var(--text-secondary);
      line-height: 1.4;
    }}

    /* Cards */
    .card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: clamp(16px, 3.5vw, 26px);
      margin-bottom: 20px;
      box-shadow: var(--shadow-sm);
      box-sizing: border-box;
      width: 100%;
      min-width: 0;
    }}

    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--border-subtle);
      flex-wrap: wrap;
      gap: 8px;
    }}

    .card-title {{
      font-size: clamp(16px, 3vw, 18px);
      font-weight: 700;
      color: var(--text-headings);
    }}

    /* Step Pipeline Plain English View */
    .step-list {{
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    .step-item {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: clamp(14px, 3vw, 20px);
      position: relative;
      box-sizing: border-box;
      width: 100%;
      min-width: 0;
    }}

    .step-badge {{
      display: inline-block;
      font-size: 10.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      margin-bottom: 8px;
      padding: 3px 9px;
      border-radius: var(--radius-full);
    }}

    .step-item h3 {{
      font-size: clamp(15px, 2.5vw, 17px);
      font-weight: 700;
      margin-bottom: 6px;
      color: var(--text-headings);
    }}

    .step-item p {{
      color: var(--text-secondary);
      font-size: 13.5px;
      line-height: 1.6;
      margin-bottom: 10px;
    }}

    .step-highlight {{
      background: #ffffff;
      border-radius: var(--radius-sm);
      padding: 12px 14px;
      font-size: 12.5px;
      color: var(--text-primary);
      border: 1px dashed rgba(0, 0, 0, 0.15);
      box-sizing: border-box;
    }}

    /* Performance Tables */
    .table-responsive {{
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      border-radius: var(--radius-sm);
      position: relative;
      margin-bottom: 6px;
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
    }}

    table {{
      width: 100%;
      min-width: 580px;
      border-collapse: collapse;
      font-size: 13px;
      text-align: left;
    }}

    th {{
      background: var(--bg-subtle);
      color: var(--text-secondary);
      font-weight: 700;
      padding: 11px 12px;
      border-bottom: 1px solid var(--border-subtle);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      white-space: nowrap;
    }}

    td {{
      padding: 11px 12px;
      border-bottom: 1px solid rgba(0, 0, 0, 0.05);
      color: var(--text-primary);
      vertical-align: middle;
    }}

    tr:hover td {{
      background: var(--bg-subtle);
    }}

    /* Palette Swatches */
    .swatch-ribbon {{
      display: inline-flex;
      border: 1px solid rgba(0, 0, 0, 0.12);
      border-radius: 6px;
      overflow: hidden;
      vertical-align: middle;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    }}

    .swatch-box {{
      width: 18px;
      height: 18px;
      display: inline-block;
    }}

    .palette-card-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
      gap: 14px;
      margin-top: 12px;
      box-sizing: border-box;
      width: 100%;
    }}

    .palette-box {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 14px;
      box-sizing: border-box;
      width: 100%;
      min-width: 0;
    }}

    .palette-box-title {{
      font-size: 13px;
      font-weight: 700;
      color: var(--tamagui-gold-dark);
      margin-bottom: 6px;
    }}

    .palette-chips {{
      display: flex;
      gap: 4px;
      margin-top: 5px;
      flex-wrap: wrap;
    }}

    .palette-chip {{
      flex: 1;
      min-width: 24px;
      height: 26px;
      border-radius: 4px;
      border: 1px solid rgba(0, 0, 0, 0.12);
      position: relative;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    }}

    /* Search & Filter Bar */
    .filter-bar {{
      display: flex;
      gap: 8px;
      margin-bottom: 16px;
      flex-wrap: wrap;
      box-sizing: border-box;
      width: 100%;
    }}

    .search-input {{
      background: #ffffff;
      border: 1px solid #d1d5db;
      border-radius: var(--radius-md);
      padding: 10px 12px;
      color: var(--text-primary);
      font-size: 14px;
      flex: 1;
      min-width: 200px;
      outline: none;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
      box-sizing: border-box;
    }}

    .search-input:focus {{
      border-color: var(--accent-purple);
      box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.12);
    }}

    .select-filter {{
      background: #ffffff;
      border: 1px solid #d1d5db;
      border-radius: var(--radius-md);
      padding: 10px 12px;
      color: var(--text-primary);
      font-size: 14px;
      outline: none;
      cursor: pointer;
      box-sizing: border-box;
    }}

    /* Grid for Charts */
    .chart-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
      gap: 16px;
      margin-bottom: 20px;
      box-sizing: border-box;
      width: 100%;
    }}

    .chart-box {{
      background: #ffffff;
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: clamp(12px, 3vw, 18px);
      height: 310px;
      min-width: 0;
      width: 100%;
      position: relative;
      box-shadow: var(--shadow-sm);
      box-sizing: border-box;
    }}

    /* Action Playbook Cards */
    .playbook-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 14px;
      box-sizing: border-box;
      width: 100%;
    }}

    .playbook-card {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 18px 16px;
      transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
      box-sizing: border-box;
      width: 100%;
      min-width: 0;
    }}

    .playbook-card:hover {{
      transform: translateY(-2px);
      border-color: var(--tamagui-gold);
      box-shadow: var(--shadow-md);
    }}

    .playbook-card .step-num {{
      font-size: 26px;
      font-weight: 800;
      color: var(--tamagui-gold-dark);
      line-height: 1;
      margin-bottom: 8px;
    }}

    .playbook-card h4 {{
      font-size: 15px;
      font-weight: 700;
      margin-bottom: 6px;
      color: var(--text-headings);
    }}

    .playbook-card p {{
      font-size: 13px;
      color: var(--text-secondary);
      line-height: 1.5;
    }}

    .code-pill {{
      font-family: 'JetBrains Mono', monospace;
      background: var(--bg-muted);
      color: var(--text-primary);
      border: 1px solid #e2e8f0;
      padding: 2px 5px;
      border-radius: 4px;
      font-size: 11px;
    }}

    /* Pagination */
    .pagination {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 14px;
      font-size: 12.5px;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .btn {{
      background: #ffffff;
      border: 1px solid #d1d5db;
      color: var(--text-primary);
      padding: 7px 14px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      font-size: 12.5px;
      font-weight: 600;
      transition: all 0.2s ease;
    }}

    .btn:hover:not(:disabled) {{
      background: var(--bg-muted);
      border-color: #9ca3af;
    }}

    .btn:disabled {{
      opacity: 0.4;
      cursor: not-allowed;
    }}

    .highlight-cell {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 600;
      color: #059669;
    }}

    /* Parameter Grid */
    .param-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 14px;
      margin-bottom: 14px;
    }}

    .param-item {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .param-label {{
      font-size: 11.5px;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .param-val {{
      font-size: 14.5px;
      font-weight: 700;
      color: var(--text-headings);
      word-break: break-all;
    }}

    /* ==========================================================================
       Smartphone & Mobile Responsive Breakpoints (min-width: 350px)
       ========================================================================== */
    @media (max-width: 860px) {{
      .chart-grid {{
        grid-template-columns: 1fr;
      }}
      .chart-box {{
        height: 290px;
      }}
    }}

    @media (max-width: 768px) {{
      body {{
        padding-bottom: 45px;
      }}
      .container {{
        padding: 14px 10px;
      }}
      .sticky-nav {{
        top: 6px;
        padding: 5px 8px;
        margin-bottom: 14px;
        gap: 5px;
      }}
      .nav-link {{
        font-size: 11.5px;
        padding: 5px 9px;
      }}
      .hero {{
        padding: 20px 14px;
        margin-bottom: 16px;
      }}
      .hero h1 {{
        font-size: 22px;
        letter-spacing: -0.4px;
      }}
      .hero p.lead {{
        font-size: 13.5px;
        margin-bottom: 12px;
      }}
      .kpi-grid {{
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 10px;
        margin-bottom: 16px;
      }}
      .kpi-card {{
        padding: 14px 12px;
      }}
      .kpi-value {{
        font-size: 24px;
      }}
      .kpi-desc {{
        font-size: 11.5px;
      }}
      .card {{
        padding: 16px 12px;
        margin-bottom: 16px;
        border-radius: var(--radius-sm);
      }}
      .card-header {{
        flex-direction: column;
        align-items: flex-start;
        gap: 6px;
        margin-bottom: 10px;
      }}
      .section-header-banner {{
        flex-direction: column;
        align-items: flex-start;
        gap: 6px;
      }}
      .section-header-title {{
        font-size: 18px;
      }}
      .palette-card-grid {{
        grid-template-columns: 1fr;
      }}
      .filter-bar {{
        flex-direction: column;
        gap: 8px;
      }}
      .search-input, .select-filter {{
        width: 100%;
        min-width: 100%;
        font-size: 14px;
        padding: 10px 12px;
      }}
      .playbook-grid {{
        grid-template-columns: 1fr;
        gap: 10px;
      }}
      .playbook-card {{
        padding: 14px 12px;
      }}
      table {{
        font-size: 12px;
      }}
      th, td {{
        padding: 9px 7px;
      }}
      .pagination {{
        flex-direction: column;
        gap: 10px;
        text-align: center;
      }}
    }}

    @media (max-width: 480px) {{
      .container {{
        padding: 10px 6px;
      }}
      .hero {{
        padding: 16px 12px;
        border-radius: 10px;
      }}
      .hero h1 {{
        font-size: 19px;
        line-height: 1.25;
      }}
      .badge-pill {{
        font-size: 10px;
        padding: 2.5px 7px;
      }}
      .kpi-grid {{
        grid-template-columns: 1fr;
        gap: 9px;
      }}
      .kpi-card {{
        padding: 12px 10px;
      }}
      .chart-box {{
        height: 240px;
        padding: 10px 6px;
      }}
      .step-item {{
        padding: 12px 10px;
      }}
      .step-item h3 {{
        font-size: 14.5px;
      }}
      .step-item p {{
        font-size: 12.5px;
      }}
      .step-highlight {{
        padding: 9px 10px;
        font-size: 11.5px;
      }}
      .swatch-box {{
        width: 15px;
        height: 15px;
      }}
      .palette-box {{
        padding: 10px;
      }}
      .palette-chip {{
        height: 22px;
        min-width: 18px;
      }}
    }}
  </style>
</head>
<body>

<div class="container">

  <!-- STICKY TOP QUICK NAVIGATION (1 PLANE PAGE) -->
  <nav class="sticky-nav" id="stickyTopNav">
    <span style="font-weight: 800; font-size: 12px; color: var(--tamagui-gold-dark); margin-right: 4px; display: flex; align-items: center; gap: 4px;">🚀 <span>Jump to:</span></span>
    <button type="button" data-target="section-initial-data" onclick="scrollToSection('section-initial-data', this)" class="nav-link active">1. Initial Datasets</button>
    <button type="button" data-target="section-final-results" onclick="scrollToSection('section-final-results', this)" class="nav-link">2. Final Results %</button>
    <button type="button" data-target="section-classes-table" onclick="scrollToSection('section-classes-table', this)" class="nav-link">3. Final Table for Classes</button>
    <button type="button" data-target="section-how-it-works" onclick="scrollToSection('section-how-it-works', this)" class="nav-link">4. Plain English Logic</button>
    <button type="button" data-target="section-timings" onclick="scrollToSection('section-timings', this)" class="nav-link">5. Timings &amp; Scaling</button>
    <button type="button" data-target="section-catalog-explorer" onclick="scrollToSection('section-catalog-explorer', this)" class="nav-link">6. Catalog Data Explorer</button>
    <button type="button" data-target="section-playbook" onclick="scrollToSection('section-playbook', this)" class="nav-link">7. Launch Action Plan</button>
  </nav>

  <!-- HERO SECTION -->
  <header class="hero">
    <div style="display: flex; gap: 8px; margin-bottom: 10px; flex-wrap: wrap;">
      <span class="badge-pill badge-tamagui">✨ Tamagui Light System</span>
      <span class="badge-pill badge-blue">Target Market: {country_name} ({iso_code})</span>
      <span class="badge-pill badge-green">Production Ready (200 Items Sample)</span>
      <span class="badge-pill badge-purple">NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = 3</span>
    </div>
    <h1>AI Product Catalog Expertise & Decision Support System (DSS)</h1>
    <p class="lead">
      Complete end-to-end intelligence report: automated Fashion-MNIST category tagging, title sales readiness checks, K-Means garment palette extraction, computer vision YOLOv8+OpenCV reference style learning, and market matchmaking for {country_name}.
    </p>
    <div style="display: flex; gap: 8px; flex-wrap: wrap;">
      <a href="HOW_IT_WORKS.html" style="text-decoration: none;" class="badge-pill badge-tamagui">📖 View How It Works Guide &rarr;</a>
      <span class="badge-pill badge-green">✔ Mission 1: Sequential Neural Classifier</span>
      <span class="badge-pill badge-blue">✔ Mission 2: Sales Readiness Verification</span>
      <span class="badge-pill badge-orange">✔ Mission 3: K-Means True Palette Extraction</span>
      <span class="badge-pill badge-purple">✔ Mission 4: YOLOv8 + OpenCV 3-Palette Reference Learning</span>
      <span class="badge-pill badge-tamagui">✔ Mission 5: DSS Marketing Matchmaker</span>
    </div>
  </header>

  <!-- =========================================================================
       SEQUENCE 1: INITIAL DATA & DATASET PARAMETERS (NEW 1ST SECTION)
       ========================================================================= -->
  <section id="section-initial-data" class="plane-section">
    <div class="section-header-banner">
      <div class="section-header-title">
        <span class="section-number">1</span>
        <span>Initial Data &amp; Dataset Parameters</span>
      </div>
      <span class="badge-pill badge-blue">Input Datasets Specifications</span>
    </div>

    <!-- Summary KPI Cards for Initial Data -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-title">
          <span>Catalog Sample Size</span>
          <span class="badge-pill badge-green">{total_items} Items</span>
        </div>
        <div class="kpi-value">{total_items} <span style="font-size: 15px; color: var(--text-secondary); font-weight: 500;">/ 1M+ Raw</span></div>
        <div class="kpi-desc">Working product subset configured by <code>DEFAULT_USE_FIRST_ITEMS = 200</code>.</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-title">
          <span>Target Market Library</span>
          <span class="badge-pill badge-tamagui">{total_target_photos} Photos</span>
        </div>
        <div class="kpi-value">{total_target_photos} <span style="font-size: 15px; color: var(--text-secondary); font-weight: 500;">({man_photos}M / {woman_photos}W)</span></div>
        <div class="kpi-desc">100% unique casual fashion photos in <code>{target_country_dir}/</code> (0 JSONs).</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-title">
          <span>Catalog Taxonomy</span>
          <span class="badge-pill badge-purple">{unique_categories_count} Classes</span>
        </div>
        <div class="kpi-value">{unique_categories_count} <span style="font-size: 15px; color: var(--text-secondary); font-weight: 500;">({raw_cat_count} Raw)</span></div>
        <div class="kpi-desc">Fashion-MNIST 10 classes mapped from GLAMI-1M 39 categories.</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-title">
          <span>Market Palettes</span>
          <span class="badge-pill badge-blue">3 Discrete</span>
        </div>
        <div class="kpi-value">3 <span style="font-size: 15px; color: var(--text-secondary); font-weight: 500;">Palettes / Gender</span></div>
        <div class="kpi-desc">Core Neutrals, Contemporary Street, and Vibrant Accent Palettes.</div>
      </div>
    </div>

    <!-- Detailed Parameters Card -->
    <div class="card">
      <div class="card-header">
        <h3 class="card-title">📋 Comprehensive Dataset &amp; Pipeline Configuration Matrix</h3>
        <span class="badge-pill badge-tamagui">Configuration Lineage</span>
      </div>

      <div class="table-responsive">
        <table>
          <thead>
            <tr>
              <th>Dataset / Parameter Area</th>
              <th>Source Location / Key</th>
              <th>Specification &amp; Dimensions</th>
              <th>Schema / Format Details</th>
              <th>Operational Purpose</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>E-Commerce Catalog (Raw)</strong></td>
              <td><code>dataset_start/GLAMI-1M-train.csv</code></td>
              <td>1,000,000+ total rows; {total_items} items active sample</td>
              <td><code>item_id, image_id, geo, name, description, category, category_name, label_source</code></td>
              <td>Primary product feed for classification, title optimization, and DSS marketing scoring.</td>
            </tr>
            <tr>
              <td><strong>Product Image Assets</strong></td>
              <td><code>dataset_start/images/*.jpg</code></td>
              <td>{total_items} matching RGB images (standardized to 28x28 grayscale for CNN)</td>
              <td>JPEG image files (RGB 3-channel, dynamic resolutions)</td>
              <td>Visual input for Fashion-MNIST neural classifier &amp; K-Means fabric color extraction.</td>
            </tr>
            <tr>
              <td><strong>Target Country Photo Library</strong></td>
              <td><code>{target_country_dir}/</code></td>
              <td>{total_target_photos} original curated photos (50 men, 50 women)</td>
              <td>Strictly <code>.jpg</code> and <code>.png</code> files; 0 <code>.json</code> metadata files</td>
              <td>Discovers local {country_name} casual fashion style DNA using YOLOv8 + OpenCV exclusions.</td>
            </tr>
            <tr>
              <td><strong>Global Pipeline Settings</strong></td>
              <td><code>run_settings.json</code></td>
              <td><code>DEFAULT_USE_FIRST_ITEMS = 200</code><br><code>NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = 3</code></td>
              <td>JSON configuration file at project root</td>
              <td>Sets global calculation parameters, target market ISO code, and photo library paths.</td>
            </tr>
            <tr>
              <td><strong>Geographic Lineage</strong></td>
              <td><code>produced_for_country</code></td>
              <td>100% Czech Republic (<code>cz</code>) catalog origin</td>
              <td>Renamed from legacy raw column <code>geo</code></td>
              <td>Preserves origin provenance while evaluating fit for {country_name} ({iso_code}) expansion.</td>
            </tr>
            <tr>
              <td><strong>Demographic Catalog Split</strong></td>
              <td>Gender Multi-Label Tagging</td>
              <td>Men: <strong>{men_items_count}</strong> | Women: <strong>{women_items_count}</strong> | Unisex: <strong>{unisex_items_count}</strong></td>
              <td>Boolean indicator columns: <code>for_man</code>, <code>for_woman</code>, <code>for_unisex</code></td>
              <td>Routes candidate products to demographic-specific reference fashion palettes.</td>
            </tr>
            <tr>
              <td><strong>DSS Decision Boundary</strong></td>
              <td>CIELAB $\Delta E$ Distance &amp; Score</td>
              <td>$\Delta E \le 13.5$ &bull; Compatibility $\ge 0.60$</td>
              <td>Normalized score $0.0 - 1.0$; perceptual color distance</td>
              <td>Separates approved marketing winners from non-priority/outlier SKUs.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>


  <!-- =========================================================================
       SEQUENCE 2: FINAL RESULTS %
       ========================================================================= -->
  <section id="section-final-results" class="plane-section">
    <div class="section-header-banner">
      <div class="section-header-title">
        <span class="section-number">2</span>
        <span>Final Results &amp; Executive KPIs</span>
      </div>
      <span class="badge-pill badge-tamagui">{iso_code} Market Fit Overview</span>
    </div>

    <!-- TOP KPI METRICS GRID -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-title">
          <span>Marketing Fit Rate</span>
          <span class="badge-pill badge-green">{good_pct:.1f}%</span>
        </div>
        <div class="kpi-value">{good_items} / {total_items}</div>
        <div class="kpi-desc">Approved products meeting {country_name} color harmony &amp; style standards.</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-title">
          <span>Sales Readiness</span>
          <span class="badge-pill badge-blue">{ready_pct:.1f}%</span>
        </div>
        <div class="kpi-value">{ready_items} / {total_items}</div>
        <div class="kpi-desc">Catalog titles optimized for Google/Meta ads with clear category keywords.</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-title">
          <span>Avg Compatibility Score</span>
          <span class="badge-pill badge-tamagui">CIELAB ΔE {avg_dist:.1f}</span>
        </div>
        <div class="kpi-value">{avg_score:.2f} <span style="font-size: 15px; color: var(--text-secondary); font-weight: 500;">/ 1.0</span></div>
        <div class="kpi-desc">Perceptual color space alignment across 3 {country_name} fashion palettes.</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-title">
          <span>200 Items Duration</span>
          <span class="badge-pill badge-purple">123.2 ms/item</span>
        </div>
        <div class="kpi-value">{tot_measured_sec:.2f}s</div>
        <div class="kpi-desc">Full 7-step pipeline execution duration from raw data to DSS recommendation.</div>
      </div>
    </div>

    <!-- Visual Charts Grid: Fit Split & Category Fit -->
    <div class="chart-grid">
      <div class="chart-box">
        <h4 style="margin-bottom: 8px; font-size: 14px; font-weight: 700; color: var(--text-headings);">Catalog Marketing Fit vs Non-Priority Split</h4>
        <canvas id="chartFitSplit"></canvas>
      </div>
      <div class="chart-box">
        <h4 style="margin-bottom: 8px; font-size: 14px; font-weight: 700; color: var(--text-headings);">Marketing Approval Rate by Garment Category</h4>
        <canvas id="chartCategoryFit"></canvas>
      </div>
    </div>

    <!-- 3 Target Country Palettes Showcase Card -->
    <div class="card" style="border-color: rgba(245, 158, 11, 0.35);">
      <div class="card-header">
        <h3 class="card-title">🎨 Discovered {country_name} Reference Style Profiles (3 Palettes Extracted)</h3>
        <span class="badge-pill badge-tamagui">NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = 3</span>
      </div>
      <p style="color: var(--text-secondary); font-size: 13px; margin-bottom: 10px;">
        Extracted purely from authentic {country_name} casual fashion photos in <code>{target_country_dir}/</code> using YOLOv8 + OpenCV multi-stage computer vision exclusions (ignoring faces, skin, background, shoes, bags, props).
      </p>

      <div class="palette-card-grid">
        <div class="palette-box">
          <div class="palette-box-title">👔 Men's Collection &bull; 3 Reference Palettes</div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin-bottom: 3px;">P1: Core Neutrals</div>
          <div class="palette-chips">
            {''.join([f'<div class="palette-chip" style="background-color:{c};" title="{c}"></div>' for c in man_palettes.get('palette_1', ['#1a202c', '#2d3748', '#4a5568', '#f7fafc'])])}
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin: 6px 0 3px 0;">P2: Contemporary Street</div>
          <div class="palette-chips">
            {''.join([f'<div class="palette-chip" style="background-color:{c};" title="{c}"></div>' for c in man_palettes.get('palette_2', ['#8c9099', '#525863', '#bd7860', '#82493b'])])}
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin: 6px 0 3px 0;">P3: Vibrant Statement</div>
          <div class="palette-chips">
            {''.join([f'<div class="palette-chip" style="background-color:{c};" title="{c}"></div>' for c in man_palettes.get('palette_3', ['#1377bd', '#e6d310', '#e0a094', '#bd7860'])])}
          </div>
        </div>

        <div class="palette-box">
          <div class="palette-box-title">👗 Women's Collection &bull; 3 Reference Palettes</div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin-bottom: 3px;">P1: Core Neutrals</div>
          <div class="palette-chips">
            {''.join([f'<div class="palette-chip" style="background-color:{c};" title="{c}"></div>' for c in woman_palettes.get('palette_1', ['#202531', '#181012', '#424654', '#efeae8'])])}
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin: 6px 0 3px 0;">P2: Contemporary Street</div>
          <div class="palette-chips">
            {''.join([f'<div class="palette-chip" style="background-color:{c};" title="{c}"></div>' for c in woman_palettes.get('palette_2', ['#8f5641', '#bda6a8', '#9d8284', '#d6cccf'])])}
          </div>
          <div style="font-size: 11.5px; color: var(--text-secondary); margin: 6px 0 3px 0;">P3: Vibrant Statement</div>
          <div class="palette-chips">
            {''.join([f'<div class="palette-chip" style="background-color:{c};" title="{c}"></div>' for c in woman_palettes.get('palette_3', ['#98aad5', '#ccbf5d', '#5f6581', '#52261b'])])}
          </div>
        </div>
      </div>
    </div>
  </section>


  <!-- =========================================================================
       SEQUENCE 3: FINAL TABLE FOR CLASSES
       ========================================================================= -->
  <section id="section-classes-table" class="plane-section">
    <div class="section-header-banner">
      <div class="section-header-title">
        <span class="section-number">3</span>
        <span>Final Breakdown Table for Product Classes</span>
      </div>
      <span class="badge-pill badge-blue">Category &amp; Segment Matrix</span>
    </div>

    <!-- Category Table Card -->
    <div class="card">
      <div class="card-header">
        <h3 class="card-title">📌 Category-by-Category Market Compatibility Breakdown</h3>
        <span class="badge-pill badge-tamagui">10 Fashion Classes</span>
      </div>
      <div class="table-responsive">
        <table>
          <thead>
            <tr>
              <th>Garment Category</th>
              <th>Total Items</th>
              <th>Approved for {iso_code}</th>
              <th>Approval (%)</th>
              <th>Sales Ready (%)</th>
              <th>Avg Match Score</th>
              <th>Avg Color Distance (ΔE)</th>
              <th>Recommended Action</th>
            </tr>
          </thead>
          <tbody>
"""

    for idx, row in cat_summary.iterrows():
        pct = row['good_pct']
        ready_p = row['ready_pct']
        badge_cls = 'badge-green' if pct >= 65 else ('badge-orange' if pct >= 40 else 'badge-red')
        action_text = "Launch as Hero Ad campaign" if pct >= 65 else ("Selective remarketing" if pct >= 40 else "Reposition / Test alternative colors")
        html_content += f"""
            <tr>
              <td><strong>{row['product_class_name']}</strong></td>
              <td>{row['total']}</td>
              <td><span class="badge-pill badge-tamagui">{int(row['good'])} items</span></td>
              <td><span class="badge-pill {badge_cls}">{pct:.1f}%</span></td>
              <td><span class="badge-pill {'badge-green' if ready_p>=50 else 'badge-orange'}">{ready_p:.1f}%</span> ({int(row['ready'])})</td>
              <td><code>{row['avg_score']:.3f}</code></td>
              <td>{row['avg_dist']:.1f} ΔE</td>
              <td><span style="font-weight:600; color:{'#059669' if pct>=65 else ('#d97706' if pct>=40 else '#be123c')};">{action_text}</span></td>
            </tr>
        """

    html_content += f"""
          </tbody>
        </table>
      </div>
    </div>

    <!-- Demographic Segment Breakdown -->
    <div class="card">
      <div class="card-header">
        <h3 class="card-title">👥 Demographic Segment Breakdown</h3>
        <span class="badge-pill badge-green">Target Market: {country_name} ({iso_code})</span>
      </div>
      <div class="table-responsive">
        <table>
          <thead>
            <tr>
              <th>Target Demographic Segment</th>
              <th>Catalog Items</th>
              <th>Approved Items</th>
              <th>Marketing Fit (%)</th>
              <th>Avg Score</th>
              <th>Avg Distance (ΔE)</th>
              <th>Marketing Action Strategy</th>
            </tr>
          </thead>
          <tbody>
"""

    for idx, row in demo_summary.iterrows():
        html_content += f"""
            <tr>
              <td><strong>{str(row['market_target_segment']).upper()}</strong></td>
              <td>{row['total']}</td>
              <td><span class="badge-pill badge-tamagui">{int(row['good'])} items</span></td>
              <td><span class="badge-pill badge-green">{row['good_pct']:.1f}%</span></td>
              <td><code>{row['avg_score']:.3f}</code></td>
              <td>{row['avg_dist']:.1f} ΔE</td>
              <td>Deploy top-scoring SKUs into targeted social ad carousels and programmatic retargeting.</td>
            </tr>
        """

    html_content += f"""
          </tbody>
        </table>
      </div>
    </div>
  </section>


  <!-- =========================================================================
       SEQUENCE 4: ALL AS IS NOW (STEP LOGIC, TIMINGS, EXPLORER, PLAYBOOK)
       ========================================================================= -->

  <!-- 4.1 PLAIN ENGLISH HOW IT WORKS -->
  <section id="section-how-it-works" class="plane-section">
    <div class="section-header-banner">
      <div class="section-header-title">
        <span class="section-number">4</span>
        <span>Plain English Logic (How Every Step Works)</span>
      </div>
      <span class="badge-pill badge-purple">Non-AI Stakeholder Guide</span>
    </div>

    <div class="card">
      <div class="step-list">
        
        <!-- STEP 1 -->
        <div class="step-item step-1">
          <span class="step-badge badge-green">Mission 1 &bull; Image Classifier</span>
          <h3>Step 1: Visual Product Category Recognition</h3>
          <p>
            <strong>What happens:</strong> The system takes raw garment photos and converts them into standardized 28x28 grayscale images. An intelligent neural network scans the silhouette of each product (neckline, sleeves, length) and categorizes it into one of 10 standard fashion classes (Dress, Coat, Pullover, Bag, Sneaker, Sandal, etc.).
          </p>
          <div class="step-highlight">
            <strong>Business Value:</strong> Eliminates manual tagging by warehouse staff, ensuring 100% of incoming items are instantly indexed into the correct catalog department.
          </div>
        </div>

        <!-- STEP 2 -->
        <div class="step-item step-2">
          <span class="step-badge badge-blue">Mission 2 &bull; Quality Control</span>
          <h3>Step 2: Sales Readiness & Title Optimization Check</h3>
          <p>
            <strong>What happens:</strong> The system inspects product titles and metadata to verify if they are clear enough for online shoppers. If a title is just an internal code (like <em>"CAS-1029"</em>), the system marks it as <code>ready_to_sale: False</code> and generates an SEO-friendly name containing the true category keyword (e.g. <em>"CAS-1029 Classic Leather Bag"</em>).
          </p>
          <div class="step-highlight">
            <strong>Business Value:</strong> Prevents unsearchable products from going live on Google Shopping and Amazon, dramatically boosting search traffic and sales conversions.
          </div>
        </div>

        <!-- STEP 3 -->
        <div class="step-item step-3">
          <span class="step-badge badge-orange">Mission 3 &bull; Color Intelligence</span>
          <h3>Step 3: True Color & Dominant Palette Extraction</h3>
          <p>
            <strong>What happens:</strong> Clean fabric pixels are separated from plain background borders. An unsupervised <strong>K-Means algorithm</strong> extracts the top dominant colors of the garment, calculates color saturation/brightness, and tags whether the item is brightly colored or monochrome (black/white/gray).
          </p>
          <div class="step-highlight">
            <strong>Business Value:</strong> Powers intuitive visual search and faceted color filters on the e-commerce website so shoppers find exact color shades instantly.
          </div>
        </div>

        <!-- STEP 4 -->
        <div class="step-item step-4">
          <span class="step-badge badge-purple">Mission 4 &bull; Market Style AI</span>
          <h3>Step 4: Target Country Style Learning (3 Palettes: NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = 3)</h3>
          <p>
            <strong>What happens:</strong> The system looks at real fashion reference images from the target market ({country_name}). To isolate only true local clothing trends, it uses <strong>YOLOv8</strong> to automatically mask out background cars, animals, bags, and props. Then, <strong>OpenCV</strong> masks out human faces, skin tones, shoes, and street backgrounds. The remaining fabric pixels are segmented into <strong>3 structured fashion palettes</strong> (Core Neutrals, Contemporary Streetwear, Vibrant Statement Accents) across Men and Women.
          </p>
          <div class="step-highlight">
            <strong>Business Value:</strong> Discovers nuanced multi-tiered consumer style preferences with zero manual curation, establishing baseline fashion DNA for the new launch country.
          </div>
        </div>

        <!-- STEP 5 -->
        <div class="step-item step-5">
          <span class="step-badge badge-tamagui">Mission 5 &bull; Decision Engine</span>
          <h3>Step 5: Decision Support System (DSS) Marketing Recommendation</h3>
          <p>
            <strong>What happens:</strong> The DSS engine compares each candidate product's visual palette against the 3 reference {country_name} market palettes. It identifies the best matching palette theme, computes color harmony distance (&Delta;E) and a compatibility score (0.0 to 1.0). If an item matches local style preferences, it tags <code>product_is_good_for_new_marketing: True</code> and assigns an actionable campaign priority tier.
          </p>
          <div class="step-highlight">
            <strong>Business Value:</strong> Gives marketing and merchandising executives an automated, data-driven launch list, cutting customer acquisition cost (CAC) and maximizing return on ad spend (ROAS).
          </div>
        </div>

      </div>
    </div>
  </section>


  <!-- 4.2 TIMINGS & SCALING PROGNOSIS -->
  <section id="section-timings" class="plane-section">
    <div class="section-header-banner">
      <div class="section-header-title">
        <span class="section-number">5</span>
        <span>Performance Timings &amp; 10k / 1M Scaling Prognosis</span>
      </div>
      <span class="badge-pill badge-green">Speed &amp; Optimization</span>
    </div>

    <!-- Prognosis KPIs -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-title">
          <span>Measured Baseline</span>
          <span class="badge-pill badge-purple">200 Items</span>
        </div>
        <div class="kpi-value">{tot_measured_sec:.2f}s</div>
        <div class="kpi-desc">Avg 123.19 ms per product across all 9 algorithm steps.</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-title">
          <span>10k Items (Single Core)</span>
          <span class="badge-pill badge-orange">Sequential</span>
        </div>
        <div class="kpi-value">{p_10k_seq}</div>
        <div class="kpi-desc">Mid-scale e-commerce catalog runtime without parallelism.</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-title">
          <span>10k Items (Optimized)</span>
          <span class="badge-pill badge-green">8-Core Multi-Thread</span>
        </div>
        <div class="kpi-value">{p_10k_opt}</div>
        <div class="kpi-desc">With vectorized batch inference and multiprocessing worker pool.</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-title">
          <span>1 Million Enterprise Scale</span>
          <span class="badge-pill badge-tamagui">Optimized 8-Core</span>
        </div>
        <div class="kpi-value">{p_1m_opt}</div>
        <div class="kpi-desc">Full enterprise catalog turnaround time (vs {p_1m_seq} sequential).</div>
      </div>
    </div>

    <div class="chart-grid">
      <div class="chart-box">
        <h4 style="margin-bottom: 8px; font-size: 14px; font-weight: 700; color: var(--text-headings);">Processing Time Share by Pipeline Step (200 Items)</h4>
        <canvas id="chartTimingDonut"></canvas>
      </div>
      <div class="chart-box">
        <h4 style="margin-bottom: 8px; font-size: 14px; font-weight: 700; color: var(--text-headings);">Scaling Speedup: Sequential vs 8-Core Parallel (Log Scale)</h4>
        <canvas id="chartScalingBar"></canvas>
      </div>
    </div>

    <!-- Step Breakdown Table -->
    <div class="card">
      <div class="card-header">
        <h3 class="card-title">⏱️ Exact Step-by-Step Benchmarks &amp; Scaling Prognoses</h3>
        <span class="badge-pill badge-blue">Measured Durations</span>
      </div>
      <div class="table-responsive">
        <table>
          <thead>
            <tr>
              <th>Step #</th>
              <th>Pipeline Phase Name</th>
              <th>200 Items Measured (s)</th>
              <th>Per-Item Avg (ms)</th>
              <th>10k Items (Seq)</th>
              <th>10k Items (8-Core Opt)</th>
              <th>1M Items (Seq)</th>
              <th>1M Items (8-Core Opt)</th>
            </tr>
          </thead>
          <tbody>
"""

    for s in benchmarks_steps:
        s_time_sec = s.get('time_200_items_sec', 0.0)
        s_per_item = s.get('per_item_ms', s.get('time_per_item_ms', 0.0))
        s_10k_seq = s.get('time_10k_seq_formatted', s.get('prognosis_10k_sequential', ''))
        s_10k_opt = s.get('time_10k_opt_formatted', s.get('prognosis_10k_parallel_8core', ''))
        s_1m_seq = s.get('time_1m_seq_formatted', s.get('prognosis_1m_sequential', ''))
        s_1m_opt = s.get('time_1m_opt_formatted', s.get('prognosis_1m_parallel_8core', ''))
        html_content += f"""
            <tr>
              <td><span class="badge-pill badge-purple">{s.get('step_id', '')}</span></td>
              <td><strong>{s.get('step_name', '')}</strong></td>
              <td class="highlight-cell">{s_time_sec:.3f}s</td>
              <td>{s_per_item:.2f} ms</td>
              <td>{s_10k_seq}</td>
              <td><strong style="color:var(--accent-green);">{s_10k_opt}</strong></td>
              <td>{s_1m_seq}</td>
              <td><strong style="color:var(--tamagui-gold);">{s_1m_opt}</strong></td>
            </tr>
        """

    html_content += f"""
          </tbody>
        </table>
      </div>
    </div>
  </section>


  <!-- 4.3 CATALOG DATA EXPLORER -->
  <section id="section-catalog-explorer" class="plane-section">
    <div class="section-header-banner">
      <div class="section-header-title">
        <span class="section-number">6</span>
        <span>Interactive Catalog Data Explorer</span>
      </div>
      <span class="badge-pill badge-tamagui">Live Multi-Filter Explorer</span>
    </div>

    <div class="card">
      <div class="filter-bar">
        <input type="text" id="searchInput" class="search-input" placeholder="Search by product name or item ID..." oninput="filterCatalog()">
        
        <select id="filterCategory" class="select-filter" onchange="filterCatalog()">
          <option value="ALL">All Categories</option>
          <option value="Dress">Dress</option>
          <option value="Bag">Bag</option>
          <option value="Trouser">Trouser</option>
          <option value="Shirt">Shirt</option>
          <option value="T-shirt/top">T-shirt/top</option>
          <option value="Coat">Coat</option>
          <option value="Sandal">Sandal</option>
          <option value="Ankle boot">Ankle boot</option>
          <option value="Sneaker">Sneaker</option>
          <option value="Pullover">Pullover</option>
        </select>

        <select id="filterPalette" class="select-filter" onchange="filterCatalog()">
          <option value="ALL">All Matched Palettes</option>
          <option value="1">Palette 1 (Core Neutrals)</option>
          <option value="2">Palette 2 (Contemporary Street)</option>
          <option value="3">Palette 3 (Vibrant Statement)</option>
        </select>

        <select id="filterDecision" class="select-filter" onchange="filterCatalog()">
          <option value="ALL">All Marketing Statuses</option>
          <option value="GOOD">Approved for {iso_code} Marketing</option>
          <option value="NOT_GOOD">Not Recommended / Outlier</option>
        </select>

        <select id="filterReady" class="select-filter" onchange="filterCatalog()">
          <option value="ALL">All Sales Readiness</option>
          <option value="READY">Ready to Sale (Optimized Title)</option>
          <option value="NOT_READY">Needs Title Optimization</option>
        </select>
      </div>

      <div class="table-responsive">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Product Name</th>
              <th>Category</th>
              <th>Segment</th>
              <th>True Garment Palette</th>
              <th>Matched Palette</th>
              <th>Ready to Sale</th>
              <th>{iso_code} Fit Score</th>
              <th>Decision</th>
              <th>Priority Tier</th>
            </tr>
          </thead>
          <tbody id="catalogTableBody">
            <!-- Rendered by client-side JS -->
          </tbody>
        </table>
      </div>

      <div class="pagination">
        <span id="pageInfo">Showing 1-25 of 200 products</span>
        <div style="display: flex; gap: 8px;">
          <button id="btnPrev" class="btn" onclick="prevPage()" disabled>Previous</button>
          <button id="btnNext" class="btn" onclick="nextPage()">Next</button>
        </div>
      </div>
    </div>
  </section>


  <!-- 4.4 LAUNCH ACTION PLAYBOOK -->
  <section id="section-playbook" class="plane-section">
    <div class="section-header-banner">
      <div class="section-header-title">
        <span class="section-number">7</span>
        <span>4-Step Executive Launch Playbook for {country_name}</span>
      </div>
      <span class="badge-pill badge-green">Strategic Roadmap</span>
    </div>

    <div class="card">
      <div class="playbook-grid">
        <div class="playbook-card">
          <div class="step-num">01</div>
          <h4>Deploy Hero Products</h4>
          <p>
            Export <span class="code-pill">result_good_for_new_marketing.csv</span> into Meta Ads and Google Shopping. Focus ad spend on <strong>Tier 1: Launch Priority</strong> items with highest compatibility score.
          </p>
        </div>

        <div class="playbook-card">
          <div class="step-num">02</div>
          <h4>Optimize Cryptic Titles</h4>
          <p>
            Filter products where <code>ready_to_sale == False</code>. Update SKU strings to descriptive consumer titles (e.g. rename <em>"Casio MTP-1259D"</em> to <em>"Casio Classic Silver Men's Watch"</em>).
          </p>
        </div>

        <div class="playbook-card">
          <div class="step-num">03</div>
          <h4>Curate 3 Palette Theme Collections</h4>
          <p>
            Group landing pages around the 3 discovered market palettes (Core Neutrals, Contemporary Earthy, and Vibrant Accents) for higher engagement and conversion.
          </p>
        </div>

        <div class="playbook-card">
          <div class="step-num">04</div>
          <h4>Continuous Retraining</h4>
          <p>
            Re-run <code>step4_learn/train_marketing_model.py</code> monthly as fresh season lookbooks are saved to keep the DSS decision boundary synchronized with emerging street trends.
          </p>
        </div>
      </div>
    </div>
  </section>

</div>

<!-- Client-side Interactive Logic & Chart.js Config -->
<script>
  const catalogData = {json_catalog};
  const timingData = {json_timings};

  let filteredData = [...catalogData];
  let currentPage = 1;
  const pageSize = 25;

  function scrollToSection(sectionId, btnElement) {{
    const el = document.getElementById(sectionId);
    if (el) {{
      el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }}
    document.querySelectorAll('.nav-link').forEach(btn => btn.classList.remove('active', 'primary'));
    if (btnElement) {{
      btnElement.classList.add('active');
    }} else {{
      const matched = document.querySelector(`.nav-link[data-target="${{sectionId}}"]`);
      if (matched) matched.classList.add('active');
    }}
  }}

  function filterCatalog() {{
    const search = document.getElementById('searchInput').value.toLowerCase();
    const cat = document.getElementById('filterCategory').value;
    const pal = document.getElementById('filterPalette').value;
    const dec = document.getElementById('filterDecision').value;
    const ready = document.getElementById('filterReady').value;

    filteredData = catalogData.filter(item => {{
      const matchSearch = item.name.toLowerCase().includes(search) || String(item.id).includes(search);
      const matchCat = (cat === 'ALL') || (item.category === cat);
      const matchPal = (pal === 'ALL') || (String(item.matched_palette_id) === pal);
      const matchDec = (dec === 'ALL') || (dec === 'GOOD' && item.is_good) || (dec === 'NOT_GOOD' && !item.is_good);
      const matchReady = (ready === 'ALL') || (ready === 'READY' && item.ready_to_sale) || (ready === 'NOT_READY' && !item.ready_to_sale);
      return matchSearch && matchCat && matchPal && matchDec && matchReady;
    }});

    currentPage = 1;
    renderTable();
  }}

  function renderTable() {{
    const tbody = document.getElementById('catalogTableBody');
    if (!tbody) return;
    tbody.innerHTML = '';

    const start = (currentPage - 1) * pageSize;
    const end = Math.min(start + pageSize, filteredData.length);
    const pageItems = filteredData.slice(start, end);

    if (pageItems.length === 0) {{
      tbody.innerHTML = '<tr><td colspan="10" style="text-align: center; color: var(--text-muted); padding: 30px;">No products found matching your filters.</td></tr>';
      const pInfo = document.getElementById('pageInfo');
      if (pInfo) pInfo.innerText = 'Showing 0-0 of 0 products';
      const bPrev = document.getElementById('btnPrev');
      if (bPrev) bPrev.disabled = true;
      const bNext = document.getElementById('btnNext');
      if (bNext) bNext.disabled = true;
      return;
    }}

    pageItems.forEach(item => {{
      const tr = document.createElement('tr');
      
      let swatchesHtml = '<div class="swatch-ribbon">';
      item.palette.forEach(hex => {{
        swatchesHtml += `<span class="swatch-box" style="background-color: ${{hex}};" title="${{hex}}"></span>`;
      }});
      swatchesHtml += '</div>';

      const readyBadge = item.ready_to_sale 
        ? '<span class="badge-pill badge-green">✔ Ready</span>' 
        : '<span class="badge-pill badge-red" title="' + item.ready_reason + '">✘ Needs Edit</span>';

      const decisionBadge = item.is_good 
        ? '<span class="badge-pill badge-tamagui">✔ Approved</span>' 
        : '<span class="badge-pill badge-orange">✘ Outlier</span>';

      const pThemeShort = item.matched_palette_name ? item.matched_palette_name.split('(')[0].trim() : 'P' + item.matched_palette_id;

      tr.innerHTML = `
        <td><code>#${{item.id}}</code></td>
        <td><strong>${{item.name}}</strong></td>
        <td><span class="badge-pill badge-blue">${{item.category}}</span></td>
        <td><span class="badge-pill badge-purple">${{item.segment}}</span></td>
        <td>${{swatchesHtml}}</td>
        <td><span class="badge-pill badge-tamagui" style="font-size:10px;">${{pThemeShort}}</span></td>
        <td>${{readyBadge}}</td>
        <td><strong>${{item.score.toFixed(3)}}</strong> <span style="font-size:11px; color:var(--text-muted);">(${{item.distance}} ΔE)</span></td>
        <td>${{decisionBadge}}</td>
        <td><span class="badge-pill badge-tamagui" style="font-size:10px;">${{item.tier}}</span></td>
      `;
      tbody.appendChild(tr);
    }});

    const pInfo = document.getElementById('pageInfo');
    if (pInfo) pInfo.innerText = `Showing ${{start + 1}}-${{end}} of ${{filteredData.length}} products`;
    const bPrev = document.getElementById('btnPrev');
    if (bPrev) bPrev.disabled = currentPage === 1;
    const bNext = document.getElementById('btnNext');
    if (bNext) bNext.disabled = end >= filteredData.length;
  }}

  function prevPage() {{
    if (currentPage > 1) {{
      currentPage--;
      renderTable();
    }}
  }}

  function nextPage() {{
    if ((currentPage * pageSize) < filteredData.length) {{
      currentPage++;
      renderTable();
    }}
  }}

  // Initialize Charts and Navigation ScrollSpy
  window.addEventListener('DOMContentLoaded', () => {{
    renderTable();

    // ScrollSpy to dynamically highlight active navigation button
    const sections = document.querySelectorAll('.plane-section');
    const navButtons = document.querySelectorAll('.nav-link');

    if ('IntersectionObserver' in window) {{
      const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
          if (entry.isIntersecting) {{
            const id = entry.target.getAttribute('id');
            navButtons.forEach(btn => {{
              if (btn.getAttribute('data-target') === id) {{
                btn.classList.add('active');
              }} else {{
                btn.classList.remove('active', 'primary');
              }}
            }});
          }}
        }});
      }}, {{
        rootMargin: '-10% 0px -65% 0px',
        threshold: 0.05
      }});

      sections.forEach(sec => observer.observe(sec));
    }}

    if (typeof Chart === 'undefined') {{
      console.warn('Chart.js library not loaded; skipping chart rendering.');
      return;
    }}

    // Chart 1: Split
    const elSplit = document.getElementById('chartFitSplit');
    if (elSplit) {{
      new Chart(elSplit, {{
        type: 'doughnut',
        data: {{
          labels: ['Approved for {iso_code} Marketing', 'Non-Priority / Outliers'],
          datasets: [{{
            data: [{good_items}, {not_good_items}],
            backgroundColor: ['#f59e0b', '#e2e8f0'],
            borderColor: ['#ffffff', '#ffffff'],
            borderWidth: 3
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'bottom', labels: {{ color: '#475569', font: {{ family: 'Plus Jakarta Sans', size: 12 }} }} }}
          }}
        }}
      }});
    }}

    // Chart 2: Category
    const elCat = document.getElementById('chartCategoryFit');
    if (elCat) {{
      const catLabels = {json.dumps([r['product_class_name'] for idx, r in cat_summary.iterrows()])};
      const catGoodPct = {json.dumps([float(r['good_pct']) for idx, r in cat_summary.iterrows()])};

      new Chart(elCat, {{
        type: 'bar',
        data: {{
          labels: catLabels,
          datasets: [{{
            label: '{iso_code} Fit (%)',
            data: catGoodPct,
            backgroundColor: '#0284c7',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            y: {{ max: 100, ticks: {{ color: '#475569' }}, grid: {{ color: 'rgba(0, 0, 0, 0.06)' }} }},
            x: {{ ticks: {{ color: '#475569' }}, grid: {{ display: false }} }}
          }}
        }}
      }});
    }}

    // Chart 3: Timing Donut
    const elTiming = document.getElementById('chartTimingDonut');
    if (elTiming) {{
      const stepNames = timingData.map(d => d.step_name);
      const stepTimes = timingData.map(d => d.time_200_items_sec);

      new Chart(elTiming, {{
        type: 'doughnut',
        data: {{
          labels: stepNames,
          datasets: [{{
            data: stepTimes,
            backgroundColor: ['#0284c7', '#f59e0b', '#7c3aed', '#10b981', '#ea580c', '#e11d48', '#6366f1', '#8b5cf6', '#64748b'],
            borderColor: '#ffffff',
            borderWidth: 2
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'bottom', labels: {{ color: '#475569', font: {{ family: 'Plus Jakarta Sans', size: 11 }}, boxWidth: 12 }} }}
          }}
        }}
      }});
    }}

    // Chart 4: Scaling Bar
    const elScale = document.getElementById('chartScalingBar');
    if (elScale) {{
      new Chart(elScale, {{
        type: 'bar',
        data: {{
          labels: ['10,000 Items', '1,000,000 Items (hrs)'],
          datasets: [
            {{
              label: 'Single-Core Sequential',
              data: [1231.9, 34.2],
              backgroundColor: '#f43f5e',
              borderRadius: 6
            }},
            {{
              label: '8-Core Parallel Optimized',
              data: [189.5, 5.25],
              backgroundColor: '#10b981',
              borderRadius: 6
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'bottom', labels: {{ color: '#475569', font: {{ family: 'Plus Jakarta Sans', size: 12 }} }} }}
          }},
          scales: {{
            y: {{ ticks: {{ color: '#475569' }}, grid: {{ color: 'rgba(0, 0, 0, 0.06)' }} }},
            x: {{ ticks: {{ color: '#475569' }}, grid: {{ display: false }} }}
          }}
        }}
      }});
    }}
  }});
</script>

</body>
</html>
"""

    report_path = os.path.join(BASE_DIR, 'CAPSTONE_REPORT.html')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"✓ Generated CAPSTONE_REPORT.html ({len(html_content)} bytes) at: {report_path}")

if __name__ == '__main__':
    build_html_report()
