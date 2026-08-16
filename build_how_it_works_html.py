"""
Builds HOW_IT_WORKS.html in the Tamagui Light theme style matching CAPSTONE_REPORT.html.
Features:
- Tamagui Light design system tokens, radial ambient glow, and Plus Jakarta Sans / JetBrains Mono typography.
- Mobile & smartphone responsive with min-width: 350px.
- Playful amber-gradient active buttons and automatic ScrollSpy navigation.
- 100% self-contained for local offline operation.
- Complete system architecture in Input -> Operation Sense -> Output format.
"""

import os
import json

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def build_how_it_works_html():
    settings_path = os.path.join(BASE_DIR, 'run_settings.json')
    settings = {}
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
        except Exception:
            pass

    country_name = settings.get('target_market_country', 'United States')
    iso_code = settings.get('target_market_iso', 'USA')
    default_items = settings.get('DEFAULT_USE_FIRST_ITEMS', 200)
    num_palettes = settings.get('NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED', 3)
    target_dir = settings.get('target_country_dir', 'step5_new_country')

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
  <title>System Architecture & Logic Guide: How It Works | {country_name} ({iso_code}) AI DSS</title>
  
  <!-- Modern Google Fonts with System Fallback for Offline Compatibility -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

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

    /* Ambient Radial Mesh Glow Backgrounds */
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

    /* Sticky Quick Nav Bar */
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

    /* Section Structure */
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

    /* Pipeline Step Detail Cards */
    .step-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: clamp(16px, 3vw, 24px);
      margin-bottom: 20px;
      box-shadow: var(--shadow-sm);
    }}

    .step-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .io-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 14px;
      margin-top: 14px;
    }}

    .io-box {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 16px;
    }}

    .io-title {{
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .io-box.input .io-title {{ color: var(--accent-blue); }}
    .io-box.sense .io-title {{ color: var(--tamagui-gold-dark); }}
    .io-box.output .io-title {{ color: var(--accent-green); }}

    .io-box ul {{
      padding-left: 18px;
      font-size: 13px;
      color: var(--text-secondary);
      line-height: 1.6;
    }}

    .io-box p {{
      font-size: 13px;
      color: var(--text-secondary);
      line-height: 1.6;
      margin-bottom: 8px;
    }}

    /* Code Snippets & Pill */
    code, pre {{
      font-family: 'JetBrains Mono', monospace;
    }}

    code {{
      background: var(--bg-muted);
      color: var(--text-primary);
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 12px;
      border: 1px solid #e2e8f0;
    }}

    pre {{
      background: #0f172a;
      color: #f8fafc;
      padding: 14px 16px;
      border-radius: var(--radius-sm);
      font-size: 12.5px;
      overflow-x: auto;
      line-height: 1.5;
      margin: 10px 0;
    }}

    .code-pill {{
      font-family: 'JetBrains Mono', monospace;
      background: var(--bg-muted);
      color: var(--text-primary);
      border: 1px solid #e2e8f0;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 11.5px;
    }}

    /* Tables */
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

    /* Grid for quick stats */
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
      font-size: clamp(22px, 5.5vw, 30px);
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

    /* Mobile Breakpoints */
    @media (max-width: 768px) {{
      .container {{ padding: 14px 10px; }}
      .sticky-nav {{ top: 6px; padding: 5px 8px; margin-bottom: 14px; gap: 5px; }}
      .nav-link {{ font-size: 11.5px; padding: 5px 10px; }}
      .hero {{ padding: 20px 14px; margin-bottom: 16px; }}
      .hero h1 {{ font-size: 22px; }}
      .kpi-grid {{ grid-template-columns: 1fr; gap: 10px; }}
      .io-grid {{ grid-template-columns: 1fr; }}
      table {{ font-size: 12px; }}
      th, td {{ padding: 9px 7px; }}
    }}

    @media (max-width: 480px) {{
      .container {{ padding: 10px 6px; }}
      .hero {{ padding: 16px 12px; }}
      .hero h1 {{ font-size: 19px; }}
    }}
  </style>
</head>
<body>

<div class="container">

  <!-- STICKY TOP QUICK NAVIGATION (DYNAMIC TAMAGUI TONE) -->
  <nav class="sticky-nav" id="stickyTopNav">
    <span style="font-weight: 800; font-size: 12px; color: var(--tamagui-gold-dark); margin-right: 4px; display: flex; align-items: center; gap: 4px;">🚀 <span>Jump to:</span></span>
    <button type="button" data-target="section-settings" onclick="scrollToSection('section-settings', this)" class="nav-link active">⚙️ Settings</button>
    <button type="button" data-target="section-arch" onclick="scrollToSection('section-arch', this)" class="nav-link">🗺️ Architecture</button>
    <button type="button" data-target="section-photo-lib" onclick="scrollToSection('section-photo-lib', this)" class="nav-link">🇺🇸 Photo Library</button>
    <button type="button" data-target="section-palettes" onclick="scrollToSection('section-palettes', this)" class="nav-link">🎨 3 Palettes</button>
    <button type="button" data-target="section-mission1" onclick="scrollToSection('section-mission1', this)" class="nav-link">M1: Classifier</button>
    <button type="button" data-target="section-mission2" onclick="scrollToSection('section-mission2', this)" class="nav-link">M2: Readiness</button>
    <button type="button" data-target="section-mission3" onclick="scrollToSection('section-mission3', this)" class="nav-link">M3: Color DNA</button>
    <button type="button" data-target="section-mission4" onclick="scrollToSection('section-mission4', this)" class="nav-link">M4: Style Learning</button>
    <button type="button" data-target="section-mission5" onclick="scrollToSection('section-mission5', this)" class="nav-link">M5: DSS Matchmaker</button>
    <button type="button" data-target="section-scripts" onclick="scrollToSection('section-scripts', this)" class="nav-link">💻 Scripts</button>
  </nav>

  <!-- HERO HEADER -->
  <header class="hero">
    <div style="display: flex; gap: 8px; margin-bottom: 10px; flex-wrap: wrap;">
      <span class="badge-pill badge-tamagui">✨ Tamagui Light System</span>
      <span class="badge-pill badge-blue">Target Market: {country_name} ({iso_code})</span>
      <span class="badge-pill badge-green">Production Ready (200 Items Sample)</span>
      <span class="badge-pill badge-purple">NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = 3</span>
    </div>
    <h1>System Architecture &amp; Logic Guide (How It Works)</h1>
    <p class="lead">
      End-to-end technical breakdown of the AI Product Catalog Expertise &amp; Decision Support System (DSS). Detailed documentation for every mission following the strict <code>Input -> Operation Sense -> Output</code> operational lineage.
    </p>
    <div style="display: flex; gap: 8px; flex-wrap: wrap;">
      <a href="CAPSTONE_REPORT.html" style="text-decoration: none;" class="badge-pill badge-tamagui">📊 Open Executive Capstone Report &rarr;</a>
      <span class="badge-pill badge-green">✔ Sequential Neural Classifier</span>
      <span class="badge-pill badge-blue">✔ Title Semantic QC</span>
      <span class="badge-pill badge-orange">✔ K-Means Color DNA</span>
      <span class="badge-pill badge-purple">✔ YOLOv8 + OpenCV Style AI</span>
      <span class="badge-pill badge-tamagui">✔ CIELAB DSS Matchmaker</span>
    </div>
  </header>

  <!-- SECTION 1: GLOBAL SETTINGS -->
  <section id="section-settings" class="plane-section">
    <div class="section-header-banner">
      <div class="section-header-title">
        <span class="section-number">1</span>
        <span>Global Configuration: <code>run_settings.json</code></span>
      </div>
      <span class="badge-pill badge-tamagui">Project Root Settings</span>
    </div>

    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-title">
          <span>Catalog Sample Size</span>
          <span class="badge-pill badge-green">DEFAULT_USE_FIRST_ITEMS</span>
        </div>
        <div class="kpi-value">{default_items} Products</div>
        <div class="kpi-desc">Controls working batch size for all downstream calculation steps.</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-title">
          <span>Market Palettes</span>
          <span class="badge-pill badge-purple">NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED</span>
        </div>
        <div class="kpi-value">{num_palettes} Palettes</div>
        <div class="kpi-desc">Core Neutrals, Contemporary Street, and Vibrant Accent Palettes.</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-title">
          <span>Target Country</span>
          <span class="badge-pill badge-blue">target_market_country</span>
        </div>
        <div class="kpi-value">{country_name} ({iso_code})</div>
        <div class="kpi-desc">Target expansion geography for style learning &amp; DSS scoring.</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-title">
          <span>Reference Photos</span>
          <span class="badge-pill badge-tamagui">target_country_dir</span>
        </div>
        <div class="kpi-value"><code>{target_dir}/</code></div>
        <div class="kpi-desc">100 casual photos (50 men, 50 women, 0 JSON files).</div>
      </div>
    </div>
  </section>

  <!-- SECTION 2: HIGH-LEVEL ARCHITECTURE MAP -->
  <section id="section-arch" class="plane-section">
    <div class="section-header-banner">
      <div class="section-header-title">
        <span class="section-number">2</span>
        <span>High-Level Pipeline Architecture Map</span>
      </div>
      <span class="badge-pill badge-blue">Missions 1 to 5</span>
    </div>

    <div class="card">
      <div class="card-header">
        <h3 class="card-title">🗺️ End-to-End Information Flow</h3>
        <span class="badge-pill badge-green">Automated Pipeline</span>
      </div>
      <div class="table-responsive">
        <table>
          <thead>
            <tr>
              <th>Mission Phase</th>
              <th>Folder</th>
              <th>Primary Input</th>
              <th>Core Transformation / AI Sense</th>
              <th>Key Output Artifact</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Mission 1: Product Ingestion &amp; Classification</strong></td>
              <td><code>step1_eda/</code></td>
              <td><code>dataset_start/GLAMI-1M-train.csv</code> &amp; <code>images/</code></td>
              <td>Fashion-MNIST CNN Sequential Model + Python Gender Tagging + Geo Renaming</td>
              <td><code>step1_eda/result1.csv</code> &amp; <code>result_categories.csv</code></td>
            </tr>
            <tr>
              <td><strong>Mission 2: Title Sales Readiness QC</strong></td>
              <td><code>step2_eda/</code></td>
              <td><code>step1_eda/result1.csv</code></td>
              <td>Keyword Alias Matching &amp; SEO Title Generation</td>
              <td><code>step1_eda/result2.csv</code> (<code>ready_to_sale : bool</code>)</td>
            </tr>
            <tr>
              <td><strong>Mission 3: K-Means Color DNA &amp; Prognosis</strong></td>
              <td><code>step3_eda/</code></td>
              <td><code>step1_eda/result2.csv</code> &amp; <code>images/</code></td>
              <td>K-Means Garment Foreground Color Clustering ($K=3$) + Scaling Benchmarks</td>
              <td><code>step1_eda/result3.csv</code> (JSON <code>palette_of_image</code>)</td>
            </tr>
            <tr>
              <td><strong>Mission 4: Target Market Style Learning</strong></td>
              <td><code>step4_learn/</code></td>
              <td><code>{target_dir}/</code> (100 Photos)</td>
              <td>YOLOv8 + OpenCV multi-stage exclusion + 3-Palette CIELAB Clustering</td>
              <td><code>market_model.pkl</code> &amp; <code>market_profile.json</code></td>
            </tr>
            <tr>
              <td><strong>Mission 5: Multi-Palette DSS Marketing Engine</strong></td>
              <td><code>step5_dss/</code></td>
              <td><code>step1_eda/result3.csv</code> &amp; <code>market_model.pkl</code></td>
              <td>Perceptual CIELAB $\Delta E$ Distance Matchmaking + Priority Tiering</td>
              <td><code>result5.csv</code>, <code>result_good_for_new_marketing.csv</code>, <code>CAPSTONE_REPORT.html</code></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- SECTION 3: PHOTO LIBRARY -->
  <section id="section-photo-lib" class="plane-section">
    <div class="section-header-banner">
      <div class="section-header-title">
        <span class="section-number">3</span>
        <span>Reference Photo Library: <code>{target_dir}/</code></span>
      </div>
      <span class="badge-pill badge-green">100 Curated Photos</span>
    </div>

    <div class="card">
      <p style="color: var(--text-secondary); font-size: 13.5px; margin-bottom: 14px;">
        The <code>{target_dir}/</code> directory contains 100 high-quality photos of {country_name} people and celebrities dressed in authentic casual clothing (strictly <code>.jpg</code> and <code>.png</code> image files, 0 <code>.json</code> metadata files):
      </p>

      <div class="io-grid">
        <div class="io-box input">
          <div class="io-title">👔 Men's Collection (50 Photos)</div>
          <p>Location: <code>{target_dir}/images/man/</code></p>
          <ul>
            <li>Brad Pitt, Ryan Gosling, Chris Evans, Leonardo DiCaprio, Keanu Reeves.</li>
            <li>Michael B. Jordan, Pedro Pascal, Timoth&eacute;e Chalamet, George Clooney.</li>
            <li>Casual street jackets, denim, tees, knitwear, and smart casual attire.</li>
          </ul>
        </div>

        <div class="io-box output">
          <div class="io-title">👗 Women's Collection (50 Photos)</div>
          <p>Location: <code>{target_dir}/images/woman/</code></p>
          <ul>
            <li>Jennifer Aniston, Taylor Swift, Zendaya, Emma Stone, Scarlett Johansson.</li>
            <li>Anne Hathaway, Blake Lively, Jennifer Lawrence, Selena Gomez, Margot Robbie.</li>
            <li>Casual streetwear, chic coats, blouses, everyday knitwear, and relaxed denim.</li>
          </ul>
        </div>
      </div>

      <div style="margin-top: 14px; padding: 12px 14px; background: var(--bg-subtle); border-radius: var(--radius-sm); border: 1px solid var(--border-subtle); font-size: 13px; color: var(--text-secondary);">
        <strong>Deduplication Guarantee:</strong> 100% unique photos verified via 64-bit Difference Hashing (<code>dHash</code>) with maximum pairwise similarity strictly below threshold.
      </div>
    </div>
  </section>

  <!-- SECTION 4: 3 REFERENCE PALETTES -->
  <section id="section-palettes" class="plane-section">
    <div class="section-header-banner">
      <div class="section-header-title">
        <span class="section-number">4</span>
        <span>3 Target Country Reference Palettes</span>
      </div>
      <span class="badge-pill badge-purple">NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = 3</span>
    </div>

    <div class="card">
      <p style="color: var(--text-secondary); font-size: 13.5px; margin-bottom: 14px;">
        To avoid oversimplifying market taste into a single flat color list, the system partitions clean image-derived garment colors into <strong>3 structured fashion palettes</strong> per demographic:
      </p>

      <div class="io-grid">
        <div class="io-box">
          <div class="io-title" style="color: #0f172a;">🎨 Palette 1: Core &amp; Classic Neutrals</div>
          <p>Foundational everyday wardrobe staples with balanced luminance and timeless versatility.</p>
          <ul>
            <li><strong>Colors:</strong> Deep Navy, Charcoal, Off-Black, Slate Gray, Crisp Off-White, Classic Beige.</li>
            <li><strong>Role:</strong> High-volume base layer items (T-shirts, trousers, classic coats).</li>
          </ul>
        </div>

        <div class="io-box">
          <div class="io-title" style="color: var(--tamagui-gold-dark);">🎨 Palette 2: Contemporary Streetwear</div>
          <p>Modern seasonal tones reflecting urban streetwear, earthy neutrals, and casual denim aesthetics.</p>
          <ul>
            <li><strong>Colors:</strong> Muted Olive, Warm Terracotta, Camel Brown, Sage Green, Washed Denim.</li>
            <li><strong>Role:</strong> Trend-forward pullovers, casual jackets, layered streetwear.</li>
          </ul>
        </div>

        <div class="io-box">
          <div class="io-title" style="color: var(--accent-purple);">🎨 Palette 3: Vibrant Statement &amp; Accents</div>
          <p>High chromatic saturation and expressive highlight tones for expressive statement fashion.</p>
          <ul>
            <li><strong>Colors:</strong> Amber/Gold, Pastel Pink, Deep Burgundy, Cobalt Blue, Coral Orange.</li>
            <li><strong>Role:</strong> Hero display items, social ad centerpieces, seasonal accents.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- SECTION 5: MISSION 1 -->
  <section id="section-mission1" class="plane-section">
    <div class="section-header-banner">
      <div class="section-header-title">
        <span class="section-number">5</span>
        <span>Mission 1: Product Ingestion &amp; Neural Classification</span>
      </div>
      <span class="badge-pill badge-green">Folder: step1_eda/</span>
    </div>

    <div class="step-card">
      <div class="step-header">
        <h3>Automated Garment Tagging &amp; Provenance Normalization</h3>
        <span class="badge-pill badge-green">TensorFlow/Keras + Pure Python</span>
      </div>

      <div class="io-grid">
        <div class="io-box input">
          <div class="io-title">📥 1. Input</div>
          <ul>
            <li><strong>Dataset File:</strong> <code>dataset_start/GLAMI-1M-train.csv</code> (<code>item_id</code>, <code>image_id</code>, <code>geo</code>, <code>name</code>, <code>description</code>, <code>category</code>, <code>category_name</code>, <code>label_source</code>).</li>
            <li><strong>Product Images:</strong> <code>dataset_start/images/{{image_id}}.jpg</code> (RGB catalog photos).</li>
          </ul>
        </div>

        <div class="io-box sense">
          <div class="io-title">⚙️ 2. Operation Sense (Why &amp; How)</div>
          <ul>
            <li><strong>Geo Normalization:</strong> Renames <code>geo</code> to <code>produced_for_country</code> for unambiguous provenance.</li>
            <li><strong>Neural Classification:</strong> Loads images via OpenCV in grayscale, resizes to (28, 28), inverts bright backgrounds to match Fashion-MNIST convention, and predicts 10 standard classes with confidence.</li>
            <li><strong>Pure Python Gender Tagging:</strong> Evaluates title &amp; category keywords (e.g. <code>mens-</code>, <code>dámské</code>) using zero-dependency string heuristics to set <code>for_man</code>, <code>for_woman</code>, <code>for_unisex</code>.</li>
            <li><strong>Garment Color Extraction:</strong> Detects foreground fabric pixels and tags primary hue, saturation, and brightness.</li>
          </ul>
        </div>

        <div class="io-box output">
          <div class="io-title">📤 3. Output</div>
          <ul>
            <li><strong><code>step1_eda/result1.csv</code>:</strong> Master ingested catalog with predicted class, confidence, gender tags, and primary colors.</li>
            <li><strong><code>step1_eda/result_categories.csv</code>:</strong> Deduplicated raw catalog categories and counts.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- SECTION 6: MISSION 2 -->
  <section id="section-mission2" class="plane-section">
    <div class="section-header-banner">
      <div class="section-header-title">
        <span class="section-number">6</span>
        <span>Mission 2: Title Sales Readiness &amp; Quality Control</span>
      </div>
      <span class="badge-pill badge-blue">Folder: step2_eda/</span>
    </div>

    <div class="step-card">
      <div class="step-header">
        <h3>E-Commerce Marketplace Search &amp; Title Verification</h3>
        <span class="badge-pill badge-blue">Semantic Title Validator</span>
      </div>

      <div class="io-grid">
        <div class="io-box input">
          <div class="io-title">📥 1. Input</div>
          <ul>
            <li><strong>Dataset File:</strong> <code>step1_eda/result1.csv</code> (ingested catalog with classified categories).</li>
          </ul>
        </div>

        <div class="io-box sense">
          <div class="io-title">⚙️ 2. Operation Sense (Why &amp; How)</div>
          <ul>
            <li>Evaluates whether product titles are optimized for Google Shopping, Amazon, and Meta Ads.</li>
            <li>Validates if the title contains the recognized <code>product_class_name</code> keyword or an approved alias.</li>
            <li>Assigns <code>ready_to_sale : bool</code> (<code>True</code> for descriptive names, <code>False</code> for cryptic internal SKU strings like <em>"CAS-1029"</em>).</li>
            <li>Generates <code>suggested_optimized_name</code> with explicit category keywords.</li>
          </ul>
        </div>

        <div class="io-box output">
          <div class="io-title">📤 3. Output</div>
          <ul>
            <li><strong><code>step1_eda/result2.csv</code>:</strong> Catalog enriched with <code>ready_to_sale</code>, rejection reason, and suggested optimized names.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- SECTION 7: MISSION 3 -->
  <section id="section-mission3" class="plane-section">
    <div class="section-header-banner">
      <div class="section-header-title">
        <span class="section-number">7</span>
        <span>Mission 3: K-Means Color DNA &amp; Performance Benchmarks</span>
      </div>
      <span class="badge-pill badge-orange">Folder: step3_eda/</span>
    </div>

    <div class="step-card">
      <div class="step-header">
        <h3>Unsupervised Color Extraction &amp; Enterprise Runtime Prognosis</h3>
        <span class="badge-pill badge-orange">K-Means ($K=3$) + Benchmark Engine</span>
      </div>

      <div class="io-grid">
        <div class="io-box input">
          <div class="io-title">📥 1. Input</div>
          <ul>
            <li><strong>Dataset File:</strong> <code>step1_eda/result2.csv</code>.</li>
            <li><strong>Product Images:</strong> <code>dataset_start/images/{{image_id}}.jpg</code>.</li>
          </ul>
        </div>

        <div class="io-box sense">
          <div class="io-title">⚙️ 2. Operation Sense (Why &amp; How)</div>
          <ul>
            <li>Masks out studio background borders using Otsu/adaptive luminance thresholding.</li>
            <li>Applies K-Means clustering ($K=3$) to extract the top 3 dominant hex colors formatted as valid JSON array: <code>'["#1a202c", "#4a5568", "#cbd5e1"]'</code>.</li>
            <li>Calculates <code>is_colored</code> boolean (chromatic saturation $> 0.18$).</li>
            <li>Measures step-by-step wall-clock runtimes and calculates scaling models for 10,000 items and 1,000,000 enterprise scale (Sequential vs 8-Core Parallel).</li>
          </ul>
        </div>

        <div class="io-box output">
          <div class="io-title">📤 3. Output</div>
          <ul>
            <li><strong><code>step1_eda/result3.csv</code>:</strong> Master catalog with JSON <code>palette_of_image</code>, dominant colors, and saturation tags.</li>
            <li><strong><code>duration/duration_log.md</code>:</strong> Exact step duration breakdown.</li>
            <li><strong><code>prognose/prognose_time.md</code> &amp; <code>prognose_summary.json</code>:</strong> Scalability projections.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- SECTION 8: MISSION 4 -->
  <section id="section-mission4" class="plane-section">
    <div class="section-header-banner">
      <div class="section-header-title">
        <span class="section-number">8</span>
        <span>Mission 4: Target Market Style Learning</span>
      </div>
      <span class="badge-pill badge-purple">Folder: step4_learn/</span>
    </div>

    <div class="step-card">
      <div class="step-header">
        <h3>Computer Vision Reference Style Extraction (3 Palettes)</h3>
        <span class="badge-pill badge-purple">YOLOv8 + OpenCV Exclusion + CIELAB Clustering</span>
      </div>

      <div class="io-grid">
        <div class="io-box input">
          <div class="io-title">📥 1. Input</div>
          <ul>
            <li><strong>Catalog Dataset:</strong> <code>step1_eda/result3.csv</code>.</li>
            <li><strong>Photo Directory:</strong> <code>{target_dir}/</code> (100 curated photos, 0 JSON files).</li>
          </ul>
        </div>

        <div class="io-box sense">
          <div class="io-title">⚙️ 2. Operation Sense (Why &amp; How)</div>
          <ul>
            <li><strong>YOLOv8 Object Exclusion:</strong> Masks out cars, animals, bags, shoes, accessories, and street furniture.</li>
            <li><strong>OpenCV Facial/Skin Masking:</strong> Removes face and exposed skin pixels to prevent skin tones from biasing clothing palettes.</li>
            <li><strong>3-Palette Clustering:</strong> Extracts 12 cluster centroids and groups them into 3 distinct 4-color palettes (Core Neutrals, Contemporary Street, Vibrant Statement) for Men and Women.</li>
            <li><strong>CIELAB Modeling:</strong> Builds perceptual $\Delta E$ nearest-neighbor space.</li>
          </ul>
        </div>

        <div class="io-box output">
          <div class="io-title">📤 3. Output</div>
          <ul>
            <li><strong><code>step4_learn/market_model.pkl</code>:</strong> Serialized multi-palette demographic ML model.</li>
            <li><strong><code>step4_learn/market_profile.json</code>:</strong> Reference color DNA across all 3 palettes.</li>
            <li><strong><code>step4_dss/result5.csv</code>:</strong> Candidate catalog scored against reference palettes.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- SECTION 9: MISSION 5 -->
  <section id="section-mission5" class="plane-section">
    <div class="section-header-banner">
      <div class="section-header-title">
        <span class="section-number">9</span>
        <span>Mission 5: Decision Support System (DSS) Marketing Engine</span>
      </div>
      <span class="badge-pill badge-tamagui">Folder: step5_dss/</span>
    </div>

    <div class="step-card">
      <div class="step-header">
        <h3>Perceptual Color Matchmaking &amp; Priority Tiering</h3>
        <span class="badge-pill badge-tamagui">Multi-Palette DSS Engine</span>
      </div>

      <div class="io-grid">
        <div class="io-box input">
          <div class="io-title">📥 1. Input</div>
          <ul>
            <li><strong>Candidate Catalog:</strong> <code>step1_eda/result3.csv</code>.</li>
            <li><strong>Market Model:</strong> <code>step4_learn/market_model.pkl</code>.</li>
          </ul>
        </div>

        <div class="io-box sense">
          <div class="io-title">⚙️ 2. Operation Sense (Why &amp; How)</div>
          <ul>
            <li>Matches each product against all 3 {country_name} palettes, finding the closest theme.</li>
            <li>Computes CIELAB $\Delta E$ distance and normalized compatibility score ($0.0 - 1.0$).</li>
            <li>Sets <code>product_is_good_for_new_marketing : bool</code> (<code>True</code> if $\Delta E \le 13.5$ and score $\ge 0.60$).</li>
            <li>Assigns Priority Tiers: <strong>Tier 1: Prime Candidate</strong>, <strong>Tier 2: Standard</strong>, <strong>Tier 3: Non-Priority</strong>.</li>
            <li>Compiles filtered winner/loser datasets and builds the single-plane executive capstone report (<code>CAPSTONE_REPORT.html</code>).</li>
          </ul>
        </div>

        <div class="io-box output">
          <div class="io-title">📤 3. Output</div>
          <ul>
            <li><strong><code>step5_dss/result5.csv</code>:</strong> Master DSS result with compatibility metrics.</li>
            <li><strong><code>step5_dss/result_good_for_new_marketing.csv</code>:</strong> Approved marketing SKUs.</li>
            <li><strong><code>step5_dss/result_not_good_for_new_marketing.csv</code>:</strong> Excluded/outlier SKUs.</li>
            <li><strong><code>step5_dss/dss_summary_report.md</code>:</strong> Executive markdown summary.</li>
            <li><strong><code>CAPSTONE_REPORT.html</code>:</strong> Executive web application.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- SECTION 10: EXECUTION SCRIPTS -->
  <section id="section-scripts" class="plane-section">
    <div class="section-header-banner">
      <div class="section-header-title">
        <span class="section-number">10</span>
        <span>Execution Scripts &amp; Command Line Reference</span>
      </div>
      <span class="badge-pill badge-green">Production Runners</span>
    </div>

    <div class="card">
      <div class="io-grid">
        <div class="io-box">
          <div class="io-title">🍎 macOS / Linux Master Runner</div>
          <p>Runs all calculation steps from Mission 1 through Mission 5 and generates reports:</p>
          <pre>./run_all_mac</pre>
          <p style="margin-top: 10px;">To view executive capstone report:</p>
          <pre>./open_report_mac</pre>
        </div>

        <div class="io-box">
          <div class="io-title">🪟 Windows Master Runner</div>
          <p>Runs all calculation steps from Mission 1 through Mission 5 and generates reports:</p>
          <pre>run_all_win.bat</pre>
          <p style="margin-top: 10px;">To view executive capstone report:</p>
          <pre>open_report_win.bat</pre>
        </div>
      </div>

      <div style="margin-top: 14px;" class="io-box sense">
        <div class="io-title">🌍 Dynamic Target Country Runner</div>
        <p>Run the entire pipeline for any custom target country photo library:</p>
        <pre># macOS / Linux:
./run_dss_for_country_mac step5_new_country "United States" USA

# Windows:
run_dss_for_country_win.bat step5_new_country "United States" USA</pre>
      </div>

      <div style="margin-top: 14px;" class="io-box output">
        <div class="io-title">💾 Save Codebase to GitHub (Automated Branch ok_YY-MM-DD-HH-MM)</div>
        <p>Creates a clean timestamped branch, excludes raw <code>dataset_start/</code>, and pushes to remote <code>https://github.com/fotomain/cv26repo.git</code>:</p>
        <pre># macOS / Linux:
./run_save_to_github_mac
# or shortcut: ./run_save_to_github

# Windows:
run_save_to_github_win.bat
REM or shortcut: run_save_to_github_win</pre>
      </div>
    </div>
  </section>

</div>

<!-- Client-side Interactive Navigation Logic -->
<script>
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

  // ScrollSpy to dynamically highlight active navigation button
  window.addEventListener('DOMContentLoaded', () => {{
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
  }});
</script>

</body>
</html>
"""

    report_path = os.path.join(BASE_DIR, 'HOW_IT_WORKS.html')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"✓ Generated HOW_IT_WORKS.html ({len(html_content)} bytes) at: {report_path}")

if __name__ == '__main__':
    build_how_it_works_html()
