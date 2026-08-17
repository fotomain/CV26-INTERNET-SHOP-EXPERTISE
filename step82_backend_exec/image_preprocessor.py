"""
Image Preprocessing and Validation Service.
Enforces size constraints (1MB max), validates graphic formats (.jpg/.png),
and prepares candidate and target country lookbook images.
"""

import os
import io
import logging
from PIL import Image

logger = logging.getLogger("image_preprocessor")

MAX_FILE_SIZE_BYTES = 1 * 1024 * 1024  # 1 MB
MAX_FILES_ALLOWED = 200
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}

class ImageValidationError(Exception):
    pass

def validate_and_save_image(file_bytes: bytes, filename: str, target_dir: str, max_size_bytes: int = MAX_FILE_SIZE_BYTES) -> str:
    """
    Validates file size, integrity, graphic consistency, and saves as RGB JPEG/PNG.
    """
    if len(file_bytes) > max_size_bytes:
        raise ImageValidationError(f"File '{filename}' exceeds {max_size_bytes / (1024*1024):.1f}MB limit (actual: {len(file_bytes)/1024:.1f}KB)")

    ext = os.path.splitext(filename)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS and not ext == '.csv':
        raise ImageValidationError(f"Unsupported file format '{ext}' for file '{filename}'. Allowed: {', '.join(SUPPORTED_EXTENSIONS)}")

    # If CSV file, write directly
    if ext == '.csv':
        out_path = os.path.join(target_dir, filename)
        os.makedirs(target_dir, exist_ok=True)
        with open(out_path, 'wb') as f:
            f.write(file_bytes)
        return out_path

    # Verify and sanitize image
    try:
        img = Image.open(io.BytesIO(file_bytes))
        img.verify()
    except Exception as e:
        raise ImageValidationError(f"Corrupted or invalid graphic image file '{filename}': {e}")

    # Re-open for actual processing (verify closes the image)
    img = Image.open(io.BytesIO(file_bytes))
    
    # Convert RGBA / Grayscale / CMYK to RGB
    if img.mode != 'RGB':
        img = img.convert('RGB')

    os.makedirs(target_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(filename))[0]
    out_filename = f"{base_name}.jpg"
    out_path = os.path.join(target_dir, out_filename)

    img.save(out_path, format="JPEG", quality=92)
    return out_path

def sanitize_uploaded_batch(files_dict: dict[str, bytes], destination_dir: str) -> list[str]:
    """
    Processes a dictionary of {filename: bytes} into destination_dir with validation.
    """
    if len(files_dict) > MAX_FILES_ALLOWED:
        raise ImageValidationError(f"Upload contains {len(files_dict)} files, exceeding maximum of {MAX_FILES_ALLOWED} files.")

    saved_paths = []
    for filename, raw_bytes in files_dict.items():
        saved_path = validate_and_save_image(raw_bytes, filename, destination_dir)
        saved_paths.append(saved_path)

    return saved_paths
