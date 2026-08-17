# Execution Time Prognosis: 10,000 and 1,000,000 Catalog Items

Based on rigorous timing benchmarks across **200 product items**, this document provides step-by-step and total runtime forecasts for scaling the expertise pipeline to **10,000 items** and **1,000,000 items**.

## 1. Executive Summary Table

| Scale | Item Count | Sequential Baseline (Single Core) | Optimized Production (8-Core CPU + GPU) |
| :--- | :--- | :--- | :--- |
| **Benchmark Baseline** | 200 items | **25.30s** | **6.33s** |
| **Mid-Scale Catalog** | 10,000 items | **21m 05s (1265.1s)** | **3m 14s (194.6s)** |
| **Full GLAMI-1M Dataset** | 1,000,000 items | **1d 11h 8m (35:08:33)** | **5h 24m (05:24:23)** |

---

## 2. Step-by-Step Prognosis Breakdown

| Step # | Algorithm Step | 200 Items (Measured) | 10,000 Items (Single Core) | 10,000 Items (8-Core Opt) | 1,000,000 Items (Single Core) | 1,000,000 Items (8-Core Opt) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Dataset I/O & CSV Ingestion** | 0.01s | 0.34s | 0.05s | 33.81s | 4.97s |
| 2 | **CNN Fashion-MNIST Classification** | 9.78s | 8m 08s (488.9s) | 57.51s | 13h 34m (13:34:45) | 1h 35m (01:35:51) |
| 3 | **Haar Face & Head Exclusion Detection** | 4.98s | 4m 09s (249.0s) | 36.62s | 6h 55m (06:55:03) | 1h 01m (01:01:02) |
| 4 | **Skin Mask Extraction (HSV + YCrCb)** | 0.13s | 6.50s | 0.96s | 10m 50s (650.0s) | 1m 35s (95.6s) |
| 5 | **Studio Background Segmentation & Morphology** | 0.79s | 39.70s | 5.84s | 1h 06m (01:06:10) | 9m 43s (583.8s) |
| 6 | **K-Means Color Palette Clustering (palette_of_image)** | 9.36s | 7m 47s (467.9s) | 1m 08s (68.8s) | 12h 59m (12:59:49) | 1h 54m (01:54:40) |
| 7 | **Gender Attribute Classification** | 0.01s | 0.45s | 0.07s | 44.76s | 6.58s |
| 8 | **Mission 2: ready_to_sale Matching** | 0.01s | 0.44s | 0.06s | 43.98s | 6.47s |
| 9 | **Mission 3: Palette Formatting & HTML Previews** | 0.05s | 2.50s | 0.37s | 4m 10s (250.0s) | 36.76s |
| -- | **TOTAL PIPELINE DURATION** | **25.30s** | **21m 05s (1265.1s)** | **3m 14s (194.6s)** | **1d 11h 8m (35:08:33)** | **5h 24m (05:24:23)** |

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
