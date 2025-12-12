#!/usr/bin/env python3
"""
EXIF Batch Photo Processor
===========================
Processes historical photos from Desktop temp folders, extracting EXIF dates,
organizing by date, compressing, renaming, and moving to proper Google Drive folders.

Perfect for backfilling thousands of historical garden photos!

Setup:
    1. PAUSE Google Drive sync! ⏸️
    2. Create temp folders on Desktop: ~/Desktop/garden_photos_temp/
    3. Inside that folder, create: basil_001_temp, strawberry_001_temp, etc.
    4. Drop all historical photos for each plant into its temp folder
    5. Run: python3 chatgpt/batch_process_photos.py
    6. Photos are automatically organized by EXIF date, compressed, renamed, moved
    7. Delete ~/Desktop/garden_photos_temp when done
    8. RESUME Google Drive sync ▶️ (uploads final compressed photos once)

Benefits:
    - Temp folders never sync to cloud (saves bandwidth!)
    - Process locally, upload once
    - Clean up before syncing

Usage from project root:
    python3 chatgpt/batch_process_photos.py

Or click "Run Python File" button in Cursor/VS Code
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from PIL import Image, ImageOps
import pillow_heif

# Register HEIC support
pillow_heif.register_heif_opener()

# Configuration
COMPRESSION_QUALITY = 85
PHOTO_BASE_PATH = Path("/Users/jodisilverman/Library/CloudStorage/GoogleDrive-jodimsilverman@gmail.com/My Drive/Garden Photos")
TEMP_BASE_PATH = Path.home() / "Desktop" / "garden_photos_temp"

def get_photo_date(file_path):
    """
    Extract date from photo EXIF data or file creation date
    Returns (datetime, source) tuple
    """
    try:
        # Try EXIF DateTimeOriginal first (most accurate)
        img = Image.open(file_path)
        exif = img._getexif()

        if exif:
            # EXIF tag 36867 = DateTimeOriginal
            date_str = exif.get(36867)
            if date_str:
                date_obj = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                return (date_obj, 'EXIF')

        # Fallback to file creation time
        creation_time = file_path.stat().st_birthtime
        date_obj = datetime.fromtimestamp(creation_time)
        return (date_obj, 'FileCreation')

    except Exception as e:
        # Last resort: file modification time
        mod_time = file_path.stat().st_mtime
        date_obj = datetime.fromtimestamp(mod_time)
        return (date_obj, 'FileModification')

def get_sequential_number(filename):
    """
    Extract sequential number from filename if it exists
    IMG_0158.jpeg -> 158
    IMG_FCA.jpeg -> None
    """
    import re
    # Match patterns like IMG_0158, IMG_159, etc.
    match = re.search(r'IMG_(\d+)', filename)
    if match:
        return int(match.group(1))
    return None

def sort_photos_by_date(photos):
    """
    Sort photos intelligently:
    1. By EXIF/creation date
    2. By sequential number (if available)
    3. By filename (alphabetically)
    """
    def sort_key(photo_tuple):
        file_path, date_obj, source = photo_tuple
        seq_num = get_sequential_number(file_path.name)
        # Return tuple: (datetime, seq_number or 999999, filename)
        return (date_obj, seq_num if seq_num is not None else 999999, file_path.name)

    return sorted(photos, key=sort_key)

def compress_and_save(input_path, output_path):
    """
    Compress image with EXIF orientation correction
    Returns True if successful
    """
    try:
        # Save to temp file first (better HEIC support)
        temp_path = output_path.parent / f"temp_{input_path.name}"
        shutil.copy(input_path, temp_path)

        # Open and apply EXIF orientation
        img = Image.open(temp_path)

        # Fix orientation based on EXIF data
        try:
            img = ImageOps.exif_transpose(img)
        except Exception as exif_error:
            print(f"      ⚠️  Could not apply EXIF orientation: {exif_error}")

        # Convert RGBA to RGB if necessary (for PNG with transparency)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # Save with compression
        img.save(
            output_path,
            'JPEG',
            quality=COMPRESSION_QUALITY,
            optimize=True,
            progressive=True
        )

        # Delete temp file
        if temp_path.exists():
            temp_path.unlink()

        return True

    except Exception as e:
        print(f"      ❌ Error processing {input_path.name}: {e}")
        if temp_path.exists():
            temp_path.unlink()
        return False

def get_file_hash(file_path):
    """
    Calculate SHA256 hash of file content
    Used to detect true duplicates (not just similar names)
    """
    import hashlib
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read in chunks for memory efficiency
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def is_duplicate_filename(filename):
    """
    Check if filename has Mac-style duplicate pattern
    Examples: IMG_0158 (1).jpeg, IMG_0158 (2).jpeg
    Returns True if it matches the pattern
    """
    import re
    # Match pattern: anything followed by space, parentheses with number, then extension
    pattern = r'.+ \(\d+\)\.[a-zA-Z]+$'
    return bool(re.match(pattern, filename))

def get_original_filename(filename):
    """
    Get the original filename from a duplicate
    'IMG_0158 (2).jpeg' -> 'IMG_0158.jpeg'
    """
    import re
    # Remove ' (n)' pattern
    pattern = r' \(\d+\)(\.[a-zA-Z]+)$'
    return re.sub(pattern, r'\1', filename)

def detect_and_remove_duplicates(photo_files, temp_folder):
    """
    Detect true duplicates by comparing file hashes
    Delete duplicate copies (keep original)
    Returns list of unique photo files
    """
    print(f"  🔍 Checking for duplicates...")

    # Build hash map: hash -> [file_paths]
    hash_to_files = {}
    for photo_path in photo_files:
        file_hash = get_file_hash(photo_path)
        if file_hash not in hash_to_files:
            hash_to_files[file_hash] = []
        hash_to_files[file_hash].append(photo_path)

    # Process duplicates
    unique_files = []
    deleted_count = 0

    for file_hash, files in hash_to_files.items():
        if len(files) == 1:
            # No duplicates
            unique_files.append(files[0])
        else:
            # Multiple files with same hash - true duplicates!
            print(f"  🔄 Found {len(files)} copies of same photo:")

            # Keep the original (no duplicate pattern in name)
            # Delete the (1), (2), (3) versions
            original = None
            duplicates = []

            for file_path in files:
                if is_duplicate_filename(file_path.name):
                    duplicates.append(file_path)
                else:
                    original = file_path

            # If no "original" found, keep the first one
            if original is None:
                original = files[0]
                duplicates = files[1:]

            unique_files.append(original)
            print(f"      ✅ Keep: {original.name}")

            # Delete duplicates
            for dup in duplicates:
                print(f"      🗑️  Delete: {dup.name}")
                dup.unlink()
                deleted_count += 1

    if deleted_count > 0:
        print(f"  ✨ Deleted {deleted_count} true duplicate(s)")
    else:
        print(f"  ✅ No duplicates found")

    return unique_files

def process_plant_folder(temp_folder):
    """Process all photos in a plant's temp folder"""
    plant_id = temp_folder.name.replace('_temp', '')

    print(f"\n{'='*60}")
    print(f"📸 Processing: {plant_id}")
    print(f"{'='*60}")

    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.heic', '.JPG', '.JPEG', '.PNG', '.HEIC'}
    all_files = [f for f in temp_folder.iterdir() if f.suffix in image_extensions]

    if not all_files:
        print(f"  ⚠️  No photos found in {temp_folder}")
        return 0

    print(f"  📁 Found {len(all_files)} file(s)")

    # Detect and remove true duplicates (by hash comparison)
    all_photos = detect_and_remove_duplicates(all_files, temp_folder)

    print(f"  📁 Found {len(all_photos)} photos")

    # Extract dates and organize
    photos_with_dates = []
    for photo_path in all_photos:
        date_obj, source = get_photo_date(photo_path)
        photos_with_dates.append((photo_path, date_obj, source))
        print(f"  📅 {photo_path.name}: {date_obj.strftime('%Y-%m-%d %H:%M:%S')} ({source})")

    # Sort photos intelligently
    sorted_photos = sort_photos_by_date(photos_with_dates)

    # Group by date
    photos_by_date = defaultdict(list)
    for photo_path, date_obj, source in sorted_photos:
        date_str = date_obj.strftime('%Y%m%d')
        photos_by_date[date_str].append((photo_path, date_obj, source))

    print(f"\n  📊 Photos span {len(photos_by_date)} unique dates")

    # Create destination folder
    dest_folder = PHOTO_BASE_PATH / plant_id
    dest_folder.mkdir(parents=True, exist_ok=True)

    # Process each date
    processed_count = 0
    for date_str in sorted(photos_by_date.keys()):
        photos = photos_by_date[date_str]
        print(f"\n  📆 {date_str} ({len(photos)} photos)")

        # Start numbering at 02 (probe is always 01)
        photo_num = 2

        for photo_path, date_obj, source in photos:
            # Generate new filename
            new_filename = f"{plant_id}-{date_str}-{photo_num:02d}.jpeg"
            output_path = dest_folder / new_filename

            # Skip if already exists
            if output_path.exists():
                print(f"    ⏭️  {new_filename} (already exists)")
                photo_num += 1
                continue

            # Compress and save
            success = compress_and_save(photo_path, output_path)
            if success:
                file_size_mb = output_path.stat().st_size / (1024 * 1024)
                print(f"    ✅ {new_filename} ({file_size_mb:.2f} MB)")
                processed_count += 1

            photo_num += 1

    print(f"\n  💾 Processed {processed_count} photos → {dest_folder}")
    return processed_count

def main():
    """Process all temp folders"""
    print("🌿 EXIF Batch Photo Processor")
    print("=" * 60)
    print(f"📍 Reading from: {TEMP_BASE_PATH}")
    print(f"📍 Writing to: {PHOTO_BASE_PATH}")
    print(f"🗜️  Compression: {COMPRESSION_QUALITY}% quality")
    print(f"🔍 Duplicate detection: INTELLIGENT (by file hash)")
    print(f"🗑️  Auto-delete: True duplicates only")

    # Verify we're reading from Desktop
    if "Desktop" not in str(TEMP_BASE_PATH):
        print("\n⚠️  WARNING: Temp path is not on Desktop!")
        print(f"   Current: {TEMP_BASE_PATH}")
        print(f"   Expected: ~/Desktop/garden_photos_temp")
        response = input("\n   Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("❌ Cancelled")
            return

    # Check if temp base path exists
    if not TEMP_BASE_PATH.exists():
        print(f"\n❌ Temp folder not found: {TEMP_BASE_PATH}")
        print("\n💡 Setup Instructions:")
        print("   1. ⏸️  PAUSE Google Drive sync first!")
        print(f"   2. Create folder: {TEMP_BASE_PATH}")
        print("   3. Inside it, create folders like: basil_001_temp, strawberry_001_temp")
        print("   4. Drop historical photos into each temp folder")
        print("   5. Run this script again")
        print("   6. When done, delete ~/Desktop/garden_photos_temp")
        print("   7. ▶️  RESUME Google Drive sync")
        return

    # Find all temp folders
    temp_folders = [f for f in TEMP_BASE_PATH.iterdir() if f.is_dir() and f.name.endswith('_temp')]

    if not temp_folders:
        print(f"\n❌ No temp folders found in {TEMP_BASE_PATH}")
        print("\n💡 Instructions:")
        print("   1. Create folders like: basil_001_temp, strawberry_001_temp")
        print(f"   2. Inside: {TEMP_BASE_PATH}")
        print("   3. Drop historical photos into each temp folder")
        print("   4. Run this script again")
        return

    print(f"\n📁 Found {len(temp_folders)} temp folder(s):")
    for folder in temp_folders:
        photo_count = len([f for f in folder.iterdir() if f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.heic'}])
        print(f"   • {folder.name} ({photo_count} photos)")

    # Warning reminder
    print("\n⚠️  IMPORTANT: Make sure Google Drive sync is PAUSED!")

    # Confirm processing
    response = input("\n❓ Process all folders? (y/n): ")
    if response.lower() != 'y':
        print("❌ Cancelled")
        return

    # Process each folder
    total_processed = 0
    for temp_folder in sorted(temp_folders):
        count = process_plant_folder(temp_folder)
        total_processed += count

    # Summary
    print("\n" + "=" * 60)
    print(f"✨ Complete! Processed {total_processed} photos from {len(temp_folders)} plant(s)")
    print("\n💡 Next steps:")
    print("   1. Review photos in Google Drive folders")
    print(f"   2. Delete temp folder: rm -rf {TEMP_BASE_PATH}")
    print("   3. ▶️  RESUME Google Drive sync (uploads final compressed photos)")
    print("   4. Run update_placeholders.py to update JSON files")
    print("   5. View photos in journal!")

if __name__ == '__main__':
    main()