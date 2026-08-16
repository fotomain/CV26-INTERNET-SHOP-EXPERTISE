# Business Expertise Report: SMART1 Catalog Readiness Analysis

**Target Entity**: Internet Shop Expansion into New Regional Market  
**Data Scope**: First 100 Products from GLAMI Dataset (`step1_eda/result1.csv`)  
**Methodology**: Computer Vision Exclusions (Faces, Skin, Shoes, Background), Keras Fashion-MNIST Deep Learning Classifier, Colorimetric K-Means Extraction, and Gender Segmentation.

---

## Executive Summary

The internet shop owner seeks to launch a marketing campaign and online store in a new country and requires an expert audit of the existing product catalog.

### SMART1 Core Questions & Answers

| Business Question | Verdict | Key Finding |
| :--- | :---: | :--- |
| **1. Is my internet shop good enough for sales in the new country?** | ⚠️ **NOT YET (Action Required)** | **Severe demographic and category imbalance**. 89% of catalog is womenswear, while menswear is only 12%. Categories are heavily skewed to dresses (41%) while knitwear, footwear, and outerwear are severely underrepresented. |
| **2. Does my internet shop have enough colored products for each `clothes_class_name_word`?** | ⚠️ **PARTIALLY (Category-Dependent)** | **Overall 44% colored vs 56% monochrome**. Dresses (36.6%) and shirts (25.0%) lack sufficient color variety. Key categories (`Pullover`, `Ankle boot`) have zero inventory. |

---

## Detailed Findings

### 1. Fashion-MNIST Category Breakdown (`clothes_class_name_word`)

| Fashion Class | Total Items | Share (%) | Colored Items | Monochrome Items | Colored Ratio (%) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Dress** | 41 | 41.0% | 15 | 26 | 36.6% | ⚠️ Deficient (<40% colored) |
| **T-shirt/top** | 16 | 16.0% | 9 | 7 | 56.2% | ✅ Balanced |
| **Trouser** | 15 | 15.0% | 6 | 9 | 40.0% | ✅ Acceptable |
| **Bag** | 11 | 11.0% | 5 | 6 | 45.5% | ✅ Acceptable |
| **Coat** | 7 | 7.0% | 4 | 3 | 57.1% | ✅ Good Variety |
| **Sandal** | 4 | 4.0% | 2 | 2 | 50.0% | ⚠️ Low Volume |
| **Shirt** | 4 | 4.0% | 1 | 3 | 25.0% | ⚠️ Deficient (<40% colored) |
| **Sneaker** | 2 | 2.0% | 2 | 0 | 100.0% | ⚠️ Critical Low Volume |
| **Pullover** | 0 | 0.0% | 0 | 0 | 0.0% | ❌ Missing Entirely |
| **Ankle boot** | 0 | 0.0% | 0 | 0 | 0.0% | ❌ Missing Entirely |
| **Total** | **100** | **100%** | **44** | **56** | **44.0%** | |

---

### 2. Audience Demographics

- **Women (`for_woman`)**: 89 products (89%)
- **Men (`for_man`)**: 12 products (12%)
- **Unisex (`for_unisex`)**: 1 product (1%)

> [!WARNING]
> If entering a broad fashion market in a new country, launching with 89% women's products will alienate male shoppers and cause high acquisition costs for men's ad campaigns.

---

### 3. Color Extraction & Exclusion Audit

Using OpenCV face cascades, skin masking, and background removal, colors were extracted purely from garment fabrics:
- **Dominant Colors**:
  - Grey: 41%
  - White: 27%
  - Black: 9%
  - Red / Pink / Magenta: 8%
  - Navy / Blue: 6%
  - Beige / Brown: 4%
  - Orange / Green / Yellow: 3%

---

## Actionable Recommendations for Marketing Campaign & Store Launch

1. **Procure Vibrant Assortments for Key Categories**:
   - Stock colored & printed **Dresses** (aim for ≥ 60% colored/floral).
   - Add patterned & colored **Shirts** (currently 75% white/grey).
2. **Fill Critical Inventory Gaps**:
   - Introduce **Pullovers/Sweaters** and **Ankle Boots/Shoes** before launching in temperate or cold climates.
3. **Rebalance Gender Mix**:
   - Expand male catalog from 12% to at least 35-45% of total offerings before launching general marketing campaigns.
4. **Localize for Target Country**:
   - Translate Czech product titles and descriptions into the target country language.
   - Adjust sizing labels according to local regional standards.
