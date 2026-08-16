"""
EDA and SMART1 Expertise Analysis Script.
Generates statistical summaries, visualizations, and answers the SMART1 business questions:
1. Is my internet shop good enough for the sales in the new country?
2. Does my internet shop have enough colored products for this country for each clothes_class_name_word?
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual style
sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

PLOTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'plots'))
os.makedirs(PLOTS_DIR, exist_ok=True)

def generate_eda_reports(csv_path: str):
    df = pd.read_csv(csv_path)
    total_items = len(df)

    print(f"Loaded {total_items} items from {csv_path} for EDA.")

    # -------------------------------------------------------------------------
    # 1. Fashion-MNIST Class Distribution Plot
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    class_counts = df['clothes_class_name_word'].value_counts()
    palette = sns.color_palette("mako", len(class_counts))
    bars = ax.bar(class_counts.index, class_counts.values, color=palette, width=0.6)
    
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.5, f"{int(h)} ({h/total_items:.1%})",
                ha='center', va='bottom', fontsize=10, fontweight='bold')
        
    ax.set_title("Catalog Distribution by Fashion-MNIST Class (clothes_class_name_word)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Fashion Category", fontweight='bold')
    ax.set_ylabel("Product Count", fontweight='bold')
    ax.set_ylim(0, max(class_counts.values) + 6)
    plt.xticks(rotation=25, ha='right')
    plt.tight_layout()
    p1 = os.path.join(PLOTS_DIR, "1_class_distribution.png")
    plt.savefig(p1)
    plt.close()
    print(f"Saved: {p1}")

    # -------------------------------------------------------------------------
    # 2. Gender Target Breakdown
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    gender_data = {
        'Women (for_woman)': df['for_woman'].sum(),
        'Men (for_man)': df['for_man'].sum(),
        'Unisex (for_unisex)': df['for_unisex'].sum()
    }
    g_colors = ['#E64A19', '#1976D2', '#388E3C']
    bars = ax.bar(gender_data.keys(), gender_data.values(), color=g_colors, width=0.5)
    
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 1, f"{int(h)}% of catalog",
                ha='center', va='bottom', fontsize=11, fontweight='bold')
        
    ax.set_title("Audience Demographics Breakdown", fontsize=14, fontweight='bold', pad=15)
    ax.set_ylabel("Products Count", fontweight='bold')
    ax.set_ylim(0, 105)
    plt.tight_layout()
    p2 = os.path.join(PLOTS_DIR, "2_gender_breakdown.png")
    plt.savefig(p2)
    plt.close()
    print(f"Saved: {p2}")

    # -------------------------------------------------------------------------
    # 3. Colored vs Monochrome per clothes_class_name_word
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ct = pd.crosstab(df['clothes_class_name_word'], df['is_colored']).rename(columns={False: 'Monochrome/Neutral', True: 'Colored/Chromatic'})
    
    ct_pct = ct.div(ct.sum(axis=1), axis=0) * 100
    
    ct.plot(kind='bar', stacked=True, color=['#78909C', '#FF7043'], ax=ax, width=0.65)
    
    for idx, (c_name, row) in enumerate(ct.iterrows()):
        total = row.sum()
        c_val = row.get('Colored/Chromatic', 0)
        c_pct = (c_val / total) * 100 if total > 0 else 0
        ax.text(idx, total + 0.8, f"{c_pct:.0f}% Colored", ha='center', fontsize=9, fontweight='bold', color='#D84315')

    ax.set_title("Colored vs Monochrome Products by Category (SMART1 Evaluation)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Fashion Category (clothes_class_name_word)", fontweight='bold')
    ax.set_ylabel("Product Count", fontweight='bold')
    ax.legend(title="Product Coloration", loc='upper right')
    plt.xticks(rotation=25, ha='right')
    plt.tight_layout()
    p3 = os.path.join(PLOTS_DIR, "3_colored_vs_monochrome_by_class.png")
    plt.savefig(p3)
    plt.close()
    print(f"Saved: {p3}")

    # -------------------------------------------------------------------------
    # 4. Dominant Colors Distribution
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    color_counts = df['dominant_color'].value_counts()
    
    # Map color names to representative hexes for visual appeal
    color_map = {
        'Grey': '#9E9E9E', 'White': '#ECEFF1', 'Black': '#212121', 'Red': '#E53935',
        'Pink/Magenta': '#EC407A', 'Navy Blue': '#1A237E', 'Blue': '#1E88E5',
        'Beige/Khaki': '#D7CCC8', 'Purple': '#8E24AA', 'Brown': '#6D4C41',
        'Orange': '#FB8C00', 'Green': '#43A047', 'Yellow': '#FDD835'
    }
    bar_colors = [color_map.get(c, '#78909C') for c in color_counts.index]
    
    bars = ax.bar(color_counts.index, color_counts.values, color=bar_colors, edgecolor='#424242', linewidth=1, width=0.6)
    
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.5, f"{int(h)}",
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_title("Dominant Garment Colors Across Catalog", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Extracted Color", fontweight='bold')
    ax.set_ylabel("Product Count", fontweight='bold')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    p4 = os.path.join(PLOTS_DIR, "4_dominant_colors_palette.png")
    plt.savefig(p4)
    plt.close()
    print(f"Saved: {p4}")

    # -------------------------------------------------------------------------
    # Generate SMART1 Summary Markdown
    # -------------------------------------------------------------------------
    class_summary = []
    for cls_name in df['clothes_class_name_word'].unique():
        sub = df[df['clothes_class_name_word'] == cls_name]
        c_count = sub['is_colored'].sum()
        tot = len(sub)
        pct = (c_count / tot) * 100
        colors_list = ", ".join(sub['dominant_color'].value_counts().head(3).index.tolist())
        class_summary.append({
            "Category": cls_name,
            "Total Items": tot,
            "Colored Items": c_count,
            "Monochrome Items": tot - c_count,
            "Colored Share (%)": f"{pct:.1f}%",
            "Top Colors": colors_list,
            "Color Variety Sufficiency": "Good (≥40%)" if pct >= 40 else "Deficient (<40%)"
        })
        
    summary_df = pd.DataFrame(class_summary).sort_values("Total Items", ascending=False)
    print("\nSMART1 Class-Level Breakdown:\n", summary_df.to_string(index=False))
    return summary_df

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    csv_file = os.path.join(base_dir, 'step1_eda', 'result1.csv')
    generate_eda_reports(csv_file)
