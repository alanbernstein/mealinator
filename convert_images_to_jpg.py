#!/usr/bin/env python3
"""
Convert WebP images to JPG for better compatibility with older devices.

This script:
1. Finds all .webp images in the images directory
2. Converts them to .jpg using ImageMagick
3. Keeps the webp originals (you can delete them later if desired)
"""

import subprocess
import os
import glob

IMAGES_DIR = "images"
THUMBNAILS_DIR = "images/thumbnails"

def convert_webp_to_jpg(webp_path, quality=85):
    """
    Convert a webp image to jpg using ImageMagick.

    Args:
        webp_path: Path to the .webp file
        quality: JPG quality (0-100, default 85)

    Returns:
        Path to the created .jpg file or None if conversion failed
    """
    jpg_path = webp_path.replace('.webp', '.jpg')

    try:
        # Use ImageMagick's convert command
        result = subprocess.run(
            ['convert', webp_path, '-quality', str(quality), jpg_path],
            check=True,
            capture_output=True,
            text=True
        )
        return jpg_path
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to convert {webp_path}")
        print(f"  Error: {e.stderr if e.stderr else str(e)}")
        return None
    except Exception as e:
        print(f"✗ Unexpected error converting {webp_path}")
        print(f"  Error: {str(e)}")
        return None

def convert_all_images():
    """Convert all webp images in both directories to jpg."""

    # Convert full-size images
    print("Converting full-size images...")
    full_size_webp = glob.glob(f"{IMAGES_DIR}/*.webp")
    full_success = 0

    for webp_path in full_size_webp:
        jpg_path = convert_webp_to_jpg(webp_path, quality=85)
        if jpg_path:
            filename = os.path.basename(jpg_path)
            print(f"✓ {filename}")
            full_success += 1

    print(f"\nFull-size: {full_success}/{len(full_size_webp)} converted")

    # Convert thumbnails
    print("\nConverting thumbnails...")
    thumbnail_webp = glob.glob(f"{THUMBNAILS_DIR}/*.webp")
    thumb_success = 0

    for webp_path in thumbnail_webp:
        jpg_path = convert_webp_to_jpg(webp_path, quality=80)
        if jpg_path:
            filename = os.path.basename(jpg_path)
            print(f"✓ {filename}")
            thumb_success += 1

    print(f"\nThumbnails: {thumb_success}/{len(thumbnail_webp)} converted")

    print(f"\n{'='*60}")
    print(f"Conversion complete!")
    print(f"Total: {full_success + thumb_success}/{len(full_size_webp) + len(thumbnail_webp)} images converted")
    print(f"\nNote: WebP originals are kept. You can delete them manually if desired:")
    print(f"  rm images/*.webp")
    print(f"  rm images/thumbnails/*.webp")

if __name__ == "__main__":
    # Check if ImageMagick is available
    try:
        subprocess.run(['convert', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: ImageMagick is not installed or 'convert' command not found.")
        print("Please install ImageMagick:")
        print("  Ubuntu/Debian: sudo apt-get install imagemagick")
        print("  macOS: brew install imagemagick")
        exit(1)

    convert_all_images()
