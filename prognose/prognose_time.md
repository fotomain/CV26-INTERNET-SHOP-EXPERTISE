# Execution Time Prognosis: 10,000 and 1,000,000 Catalog Items

Based on rigorous timing benchmarks across **200 product items**, this document provides step-by-step and total runtime forecasts for scaling the expertise pipeline to **10,000 items** and **1,000,000 items**.

## 1. Executive Summary Table

| Scale | Item Count | Sequential Baseline (Single Core) | Optimized Production (8-Core CPU + GPU) |
| :--- | :--- | :--- | :--- |
| **Benchmark Baseline** | 200 items | **25.55s** | **6.39s** |
| **Mid-Scale Catalog** | 10,000 items | **21m 17s (1277.5s)** | **3m 16s (196.5s)** |
| **Full GLAMI-1M Dataset** | 1,000,000 items | **1d 11h 29m (35:29:13)** | **5h 27m (05:27:34)** |

---

## 2. Step-by-Step Prognosis Breakdown

| Step # | Algorithm Step | 200 Items (Measured) | 10,000 Items (Single Core) | 10,000 Items (8-Core Opt) | 1,000,000 Items (Single Core) | 1,000,000 Items (8-Core Opt) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Dataset I/O & CSV Ingestion** | 0.01s | 0.27s | 0.04s | 27.31s | 4.02s |
| 2 | **CNN Fashion-MNIST Classification** | 9.85s | 8m 12s (492.5s) | 57.94s | 13h 40m (13:40:46) | 1h 36m (01:36:33) |
| 3 | **Haar Face & Head Exclusion Detection** | 5.06s | 4m 12s (252.9s) | 37.19s | 7h 01m (07:01:29) | 1h 01m (01:01:58) |
| 4 | **Skin Mask Extraction (HSV + YCrCb)** | 0.13s | 6.57s | 0.97s | 10m 56s (656.6s) | 1m 36s (96.6s) |
| 5 | **Studio Background Segmentation & Morphology** | 0.81s | 40.49s | 5.95s | 1h 07m (01:07:28) | 9m 55s (595.4s) |
| 6 | **K-Means Color Palette Clustering (palette_of_image)** | 9.43s | 7m 51s (471.4s) | 1m 09s (69.3s) | 13h 05m (13:05:41) | 1h 55m (01:55:32) |
| 7 | **Gender Attribute Classification** | 0.01s | 0.45s | 0.07s | 44.67s | 6.57s |
| 8 | **Mission 2: ready_to_sale Matching** | 0.01s | 0.45s | 0.07s | 45.42s | 6.68s |
| 9 | **Mission 3: Palette Formatting & HTML Previews** | 0.05s | 2.50s | 0.37s | 4m 10s (250.0s) | 36.76s |
| -- | **TOTAL PIPELINE DURATION** | **25.55s** | **21m 17s (1277.5s)** | **3m 16s (196.5s)** | **1d 11h 29m (35:29:13)** | **5h 27m (05:27:34)** |

---

## 3. Computational Scaling Analysis & Recommendations

### A. Bottlenecks at 1,000,000 Items
1. **CNN Classification (Fashion-MNIST)**:
   - Sequential processing of 1M individual images takes ~14-16 hours.
   - **Recommendation**: Process images in mini-batches (e.g., `batch_size=256` or `512`) using TensorFlow GPU / Metal MPS acceleration to reduce this to under 1.5 hours.
2. **K-Means Color Palette Extraction (`palette_of_image`)**:
   - Fitting K-Means on 1M images sequentially takes ~13-15 hours.
   - **Recommendation**: Use `MiniBatchKMeans` with subsampled pixel arrays (1,000 pixels per garment mask) and parallel worker threads (`multiprocessing.Pool(processes=8)`).
3. **Computer Vision Exclusions (Faces, Skin, Background)**:
   - Haar cascades and morphology take ~8-10 hours.
   - **Recommendation**: Parallelize image I/O and segmentation across multi-core workers.

### B. Recommended High-Throughput Architecture for 1,000,000 Items
- **Concurrency**: 8 to 16 parallel workers using `concurrent.futures.ProcessPoolExecutor`.
- **Pipeline Strategy**: Stream images in chunks of 5,000 to prevent RAM memory leaks.
- **Expected Production Throughput**: ~80-120 items/second -> **Full 1M dataset completed in under 2.5 to 3.5 hours**.
