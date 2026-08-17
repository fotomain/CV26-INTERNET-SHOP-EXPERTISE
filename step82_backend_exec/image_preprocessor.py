"""
Image Preprocessing and Auto-Optimization Service.
Validates graphic formats, auto-downscales/compresses images exceeding size thresholds,
and converts to normalized RGB JPEG for the ML pipeline.
"""

import os
import io
import logging
from PIL import Image, ImageOps

logger = logging.getLogger("image_preprocessor")

MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024  # 25 MB max upload buffer
TARGET_MAX_FILE_SIZE_BYTES = 1 * 1024 * 1024  # Target 1 MB on disk
MAX_FILES_ALLOWED = 500
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.jfif'}

class ImageValidationError(Exception):
    pass

def validate_and_save_image(file_bytes: bytes, filename: str, target_dir: str, max_size_bytes: int = MAX_FILE_SIZE_BYTES) -> str:
    """
    Validates file integrity, auto-resizes & compresses high-resolution photos,
    and saves normalized RGB JPEG/PNG into target directory.
    """
    if not file_bytes or len(file_bytes) == 0:
        raise ImageValidationError(f"File '{filename}' is empty (0 bytes).")

    ext = os.path.splitext(filename)[1].lower()
    os.makedirs(target_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(filename))[0]

    # If CSV file, write directly
    if ext == '.csv':
        out_path = os.path.join(target_dir, filename)
        with open(out_path, 'wb') as f:
            f.write(file_bytes)
        return out_path

    # Verify and sanitize image
    try:
        img = Image.open(io.BytesIO(file_bytes))
        # Correct orientation based on EXIF if present
        img = ImageOps.exif_transpose(img)
    except Exception as e:
        logger.warning(f"Could not parse image '{filename}': {e}")
        raise ImageValidationError(f"Invalid graphic image '{filename}': {e}")

    # Convert RGBA / Grayscale / CMYK to RGB
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Auto-downscale if large resolution (e.g. > 1600px)
    max_dim = 1200
    w, h = img.size
    if max(w, h) > max_dim:
        scale = max_dim / float(max(w, h))
        new_w, new_h = int(w * scale), int(h * scale)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        logger.info(f"Auto-downscaled '{filename}' from {w}x{h} to {new_w}x{new_h}")

    out_filename = f"{base_name}.jpg"
    out_path = os.path.join(target_dir, out_filename)

    # Save as optimized JPEG
    quality = 90
    img.save(out_path, format="JPEG", quality=quality, optimize=True)

    # If still > 1MB, reduce quality progressively
    file_size = os.path.getsize(out_path)
    while file_size > TARGET_MAX_FILE_SIZE_BYTES and quality > 60:
        quality -= 10
        img.save(out_path, format="JPEG", quality=quality, optimize=True)
        file_size = os.path.getsize(out_path)

    return out_path

def sanitize_uploaded_batch(files_dict: dict[str, bytes], destination_dir: str) -> list[str]:
    """
    Processes a dictionary of {filename: bytes} into destination_dir with validation.
    """
    if len(files_dict) > MAX_FILES_ALLOWED:
        raise ImageValidationError(f"Upload contains {len(files_dict)} files, exceeding maximum of {MAX_FILES_ALLOWED} files.")

    saved_paths = []
    for filename, raw_bytes in files_dict.items():
        try:
            saved_path = validate_and_save_image(raw_bytes, filename, destination_dir)
            saved_paths.append(saved_path)
        except Exception as e:
            logger.warning(f"Skipping corrupted file '{filename}': {e}")

    return saved_paths
