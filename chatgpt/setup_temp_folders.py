#!/usr/bin/env python3
"""
Setup Temp Folders Script
==========================
Automatically creates temp folder structure on Desktop for batch photo processing.

Reads all plant IDs from data/plants/ directory and creates corresponding temp folders
in ~/Desktop/garden_photos_temp/

Perfect for preparing to process historical photos!

Usage:
    python3 setup_temp_folders.py

Or click "Run Python File" button in Cursor/VS Code
"""

from pathlib import Path

def main():
    """Create temp folder structure"""
    print("🌿 Garden Photos Temp Folder Setup")
    print("=" * 60)

    # Define paths (script is in chatgpt/, need to go up one level)
    data_dir = Path(__file__).parent.parent / 'data' / 'plants'
    temp_base = Path.home() / "Desktop" / "garden_photos_temp"

    # Check if data directory exists
    if not data_dir.exists():
        print(f"❌ Error: Plants directory not found: {data_dir}")
        return

    # Get all plant JSON files
    plant_files = list(data_dir.glob('*.json'))

    if not plant_files:
        print(f"❌ Error: No plant JSON files found in {data_dir}")
        return

    print(f"\n📁 Found {len(plant_files)} plants in data/plants/")

    # Extract plant IDs
    plant_ids = [f.stem for f in sorted(plant_files)]

    print(f"\n🌱 Plants:")
    for plant_id in plant_ids:
        print(f"   • {plant_id}")

    # Check if temp base already exists
    if temp_base.exists():
        print(f"\n⚠️  Temp folder already exists: {temp_base}")
        response = input("Delete and recreate? (y/n): ")
        if response.lower() == 'y':
            import shutil
            shutil.rmtree(temp_base)
            print(f"   🗑️  Deleted existing folder")
        else:
            print("❌ Cancelled")
            return

    # Create base temp folder
    temp_base.mkdir(parents=True, exist_ok=True)
    print(f"\n📂 Created: {temp_base}")

    # Create temp folder for each plant
    created_count = 0
    for plant_id in plant_ids:
        temp_folder = temp_base / f"{plant_id}_temp"
        temp_folder.mkdir(exist_ok=True)
        print(f"   ✅ {temp_folder.name}")
        created_count += 1

    # Summary
    print("\n" + "=" * 60)
    print(f"✨ Created {created_count} temp folders!")
    print(f"\n📍 Location: {temp_base}")
    print("\n💡 Next steps:")
    print("   1. ⏸️  PAUSE Google Drive sync")
    print("   2. Open Finder and navigate to Desktop/garden_photos_temp/")
    print("   3. Drop historical photos into appropriate plant folders")
    print("   4. Run: python3 chatgpt/batch_process_photos.py")
    print("   5. Delete ~/Desktop/garden_photos_temp when done")
    print("   6. ▶️  RESUME Google Drive sync")
    print("\n📖 Example:")
    print(f"   Drop basil photos into: {temp_base}/basil_001_temp/")
    print(f"   Drop strawberry photos into: {temp_base}/strawberry_001_temp/")

if __name__ == '__main__':
    main()