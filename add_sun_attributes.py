#!/usr/bin/env python3
"""
Script to add full_sun_start and full_shade_start attributes to all plant JSON files
"""

import json
import os
from pathlib import Path

def add_sun_attributes(file_path):
    """Add sun timing attributes to a plant JSON file"""
    print(f"Processing: {file_path}")

    # Read the JSON file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if attributes already exist
    if 'full_sun_start' in data and 'full_shade_start' in data:
        print(f"  ⚠️  Attributes already exist, skipping")
        return False

    # Create new ordered dictionary with the attributes in the correct position
    new_data = {}
    for key, value in data.items():
        new_data[key] = value
        # After garden_location, add the new attributes
        if key == 'garden_location':
            new_data['full_sun_start'] = "9:00 AM"
            new_data['full_shade_start'] = "4:00 PM"

    # Write back to file with proper formatting
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)
        f.write('\n')  # Add trailing newline

    print(f"  ✓ Successfully added attributes")
    return True

def main():
    # Get the data/plants directory
    plants_dir = Path('/Users/jodisilverman/Repositories/garden_journal/data/plants')

    # Find all JSON files in plants directory and inactive subdirectory
    json_files = list(plants_dir.glob('*.json')) + list(plants_dir.glob('inactive/*.json'))

    print(f"Found {len(json_files)} plant JSON files\n")

    updated_count = 0
    skipped_count = 0

    for json_file in sorted(json_files):
        if add_sun_attributes(json_file):
            updated_count += 1
        else:
            skipped_count += 1

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Updated: {updated_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Total:   {len(json_files)}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
