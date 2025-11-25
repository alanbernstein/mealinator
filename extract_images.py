#!/usr/bin/env python3
"""
Extract recipe images from Mealie Docker container.

This script:
1. Queries the database for all recipes with images
2. Copies images from the Mealie container to local directories
3. Creates both original and thumbnail versions for the website
"""

import sqlite3
import subprocess
import os

DB_PATH = "mealie.db"
CONTAINER_NAME = "mealie"
IMAGES_DIR = "images"
THUMBNAILS_DIR = "images/thumbnails"

def extract_images():
    # Create output directories
    os.makedirs(IMAGES_DIR, exist_ok=True)
    os.makedirs(THUMBNAILS_DIR, exist_ok=True)

    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all recipes with their IDs and slugs
    cursor.execute("SELECT id, slug, image FROM recipes WHERE image IS NOT NULL AND image != ''")
    recipes = cursor.fetchall()

    success_count = 0
    error_count = 0

    for recipe_id, slug, image_code in recipes:
        # Format the ID with dashes (Mealie uses UUID format)
        # The ID in the database is stored without dashes, but the directory uses dashes
        formatted_id = f"{recipe_id[:8]}-{recipe_id[8:12]}-{recipe_id[12:16]}-{recipe_id[16:20]}-{recipe_id[20:]}"

        # Source paths in container
        container_original = f"/app/data/recipes/{formatted_id}/images/original.webp"
        container_min = f"/app/data/recipes/{formatted_id}/images/min-original.webp"
        container_tiny = f"/app/data/recipes/{formatted_id}/images/tiny-original.webp"

        # Destination paths
        local_original = f"{IMAGES_DIR}/mealie-{slug}.webp"
        local_thumbnail = f"{THUMBNAILS_DIR}/mealie-{slug}.webp"

        try:
            # Copy original image (for recipe page)
            result = subprocess.run(
                ["docker", "cp", f"{CONTAINER_NAME}:{container_original}", local_original],
                check=True,
                capture_output=True,
                text=True
            )

            # Copy thumbnail (for index page)
            # Try min-original first, fall back to tiny if not available
            try:
                subprocess.run(
                    ["docker", "cp", f"{CONTAINER_NAME}:{container_min}", local_thumbnail],
                    check=True,
                    capture_output=True,
                    text=True
                )
            except subprocess.CalledProcessError:
                # Fall back to tiny
                subprocess.run(
                    ["docker", "cp", f"{CONTAINER_NAME}:{container_tiny}", local_thumbnail],
                    check=True,
                    capture_output=True,
                    text=True
                )

            print(f"✓ Copied images for: {slug}")
            success_count += 1

        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to copy images for: {slug} (ID: {formatted_id})")
            print(f"  Error: {e.stderr if e.stderr else str(e)}")
            error_count += 1
        except Exception as e:
            print(f"✗ Unexpected error for: {slug}")
            print(f"  Error: {str(e)}")
            error_count += 1

    conn.close()

    print(f"\nExtraction complete!")
    print(f"Success: {success_count} recipes")
    print(f"Errors: {error_count} recipes")
    print(f"Total: {len(recipes)} recipes in database")

if __name__ == "__main__":
    extract_images()
