# Decision Support System (DSS) Report: United States (USA) Marketing Suitability

**Target Market**: United States (USA)  
**Number of Target Palettes Used**: `NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = 3`  
**Catalog Sample Size**: 200 items  
**Products Recommended for Marketing (`product_is_good_for_new_marketing = True`)**: **62 / 200 (31.0%)**  
**Average Market Compatibility Score**: `0.508`  
**Average Color Distance to Target Palettes**: `14.8 ΔE`  

---

## 1. Executive Summary & 3-Palette Fashion Alignment

The Decision Support System evaluated candidate catalog items against United States's image-derived fashion palettes across 3 distinct aesthetic clusters:

- **Palette 1 (Core & Classic Neutrals)**: **110 SKUs (55.0%)** matched as best stylistic fit.
- **Palette 2 (Contemporary & Earthy Street)**: **64 SKUs (32.0%)** matched as best stylistic fit.
- **Palette 3 (Vibrant Statement & Accents)**: **26 SKUs (13.0%)** matched as best stylistic fit.

| Marketing Priority Tier | Product Count | Share of Catalog (%) | Recommendation |
| :--- | :---: | :---: | :--- |
| **Tier 3: Non-Priority / Neutral** | 138 | 69.0% | Organic / Secondary Listing Only |
| **Tier 2: Standard Marketing Candidate** | 52 | 26.0% | Standard Catalog Inclusion |
| **Tier 1: Prime Marketing Candidate** | 10 | 5.0% | Immediate Hero Product Ads & Paid Acquisition |

---

## 2. Market Suitability Breakdown by Demographic Segment

| Target Segment | Total Items | Recommended for Marketing | Suitability (%) | Mean Compatibility Score |
| :--- | :---: | :---: | :---: | :---: |
| **Men** | 21 | 11 | **52.4%** | 0.539 |
| **Unisex** | 70 | 19 | **27.1%** | 0.507 |
| **Women** | 109 | 32 | **29.4%** | 0.502 |

---

## 3. Market Suitability Breakdown by Fashion Category

| Fashion Category (`product_class_name`) | Total Items | Recommended for Marketing | Suitability (%) | Mean Distance (ΔE) | Mean Score |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Dress** | 52 | 16 | **30.8%** | 14.7 ΔE | 0.515 |
| **Bag** | 43 | 13 | **30.2%** | 15.4 ΔE | 0.492 |
| **T-shirt/top** | 27 | 7 | **25.9%** | 17.5 ΔE | 0.465 |
| **Trouser** | 25 | 12 | **48.0%** | 12.5 ΔE | 0.56 |
| **Shirt** | 24 | 4 | **16.7%** | 13.7 ΔE | 0.514 |
| **Sandal** | 9 | 2 | **22.2%** | 14.6 ΔE | 0.497 |
| **Coat** | 8 | 4 | **50.0%** | 16.0 ΔE | 0.502 |
| **Ankle boot** | 6 | 2 | **33.3%** | 13.3 ΔE | 0.522 |
| **Sneaker** | 4 | 0 | **0.0%** | 16.3 ΔE | 0.45 |
| **Pullover** | 2 | 2 | **100.0%** | 9.5 ΔE | 0.622 |

---

## 4. Top Recommended Products for Marketing Launch

| Item ID | Product Name | Category | Matched Palette | Compatibility Score | Readiness |
| :---: | :--- | :--- | :--- | :---: | :---: |
| `98` | **Tanga Gabidar 121** | Trouser | Palette 1 (Core & Classic Neutrals) | `0.838` | Unready |
| `121` | **Naf Naf Krátké šaty LYMELL** | Dress | Palette 1 (Core & Classic Neutrals) | `0.773` | Ready |
| `106` | **Společenské šaty s krajkou Katrus K** | Shirt | Palette 1 (Core & Classic Neutrals) | `0.772` | Unready |
| `85` | **BCBGeneration Krátké šaty 617437** | Dress | Palette 1 (Core & Classic Neutrals) | `0.747` | Ready |
| `32` | **Béžové šaty Katrus K057** | Dress | Palette 1 (Core & Classic Neutrals) | `0.742` | Ready |
| `12` | **Těhotenský top s potiskem Mamalicio** | T-shirt/top | Palette 1 (Core & Classic Neutrals) | `0.734` | Ready |
| `161` | **Veneziana Beautifull Punčochy 1 2 N** | Bag | Palette 2 (Contemporary & Earthy Street) | `0.732` | Unready |
| `41` | **Dámské šaty Figl M202 béžové** | Dress | Palette 1 (Core & Classic Neutrals) | `0.722` | Ready |

---

## 5. Strategic Merchandising & Campaign Directives

1. **Launch Paid Search with Tier 1 Products**: Focus ad spend on the top-matching SKUs with high compatibility scores (>0.72).
2. **Feature Palette 1 & 2 in Core Collections**: Ensure core neutral and contemporary earthy streetwear hero SKUs lead collection landing pages.
3. **Combine `ready_to_sale` and `product_is_good_for_new_marketing`**: Ensure products approved for marketing also have complete catalog metadata (`ready_to_sale = True`) before syndicating feeds.
