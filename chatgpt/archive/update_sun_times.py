#!/usr/bin/env python3
"""
Update full_sun_start and full_shade_start times for all plants based on their panel location.
"""
import json
import os
from pathlib import Path

# Sun timing data by panel
SUN_TIMES = {
    "Panel 1": {"start": "9:05 AM", "end": "3:30 PM"},
    "Panel 2": {"start": "9:05 AM", "end": "3:30 PM"},
    "Panel 3": {"start": "9:00 AM", "end": "3:30 PM"},
    "Panel 4": {"start": "9:00 AM", "end": "3:30 PM"},
    "Panel 5": {"start": "8:30 AM", "end": "3:30 PM"},
    "Panel 6": {"start": "8:30 AM", "end": "3:30 PM"},
    "Panel 7": {"start": "9:10 AM", "end": "3:30 PM"},
    "Panel 8": {"start": "9:45 AM", "end": "3:30 PM"},
    "Panel 9": {"start": "10:20 AM", "end": "3:30 PM"},
    "Panel 10": {"start": "10:43 AM", "end": "3:30 PM"},
    "Panel 11": {"start": "10:43 AM", "end": "3:30 PM"},
    "Panel 12": {"start": "10:43 AM", "end": "3:30 PM"},
    "Panel 13": {"start": "10:43 AM", "end": "3:30 PM"},
    "Panel 14": {"start": "10:48 AM", "end": "3:30 PM"},
    "Panel 15": {"start": "10:48 AM", "end": "3:30 PM"},
    "Panel 16": {"start": "11:15 AM", "end": "4:15 PM"},
    "Panel 17": {"start": "11:15 AM", "end": "4:15 PM"},
    "Panel 18": {"start": "11:15 AM", "end": "4:15 PM"},
    "Panel 16-18": {"start": "11:15 AM", "end": "4:15 PM"},  # Combined panel location
    "Firepit": {"start": "9:30 AM", "end": "4:15 PM"},  # Firepit mums
    "Firepit mum #1": {"start": "9:30 AM", "end": "4:15 PM"},
    "Firepit mum #2": {"start": "9:30 AM", "end": "4:15 PM"},
}

def update_plant_sun_times(plant_file):
    """Update sun times for a single plant file."""
    with open(plant_file, 'r') as f:
        plant_data = json.load(f)

    garden_location = plant_data.get('garden_location', '')

    if garden_location in SUN_TIMES:
        sun_times = SUN_TIMES[garden_location]
        old_start = plant_data.get('full_sun_start')
        old_end = plant_data.get('full_shade_start')

        plant_data['full_sun_start'] = f"{sun_times['start']} EST"
        plant_data['full_shade_start'] = f"{sun_times['end']} EST"

        # Write back to file
        with open(plant_file, 'w') as f:
            json.dump(plant_data, f, indent=2)

        print(f"✓ Updated {plant_data['id']}: {garden_location}")
        print(f"  Sun: {old_start} → {sun_times['start']} EST")
        print(f"  Shade: {old_end} → {sun_times['end']} EST")
        return True
    else:
        print(f"⚠ Skipped {plant_data['id']}: Location '{garden_location}' not found in sun times data")
        return False

def main():
    plants_dir = Path(__file__).parent / 'data' / 'plants'

    # Get all JSON files except those in inactive folder
    plant_files = [f for f in plants_dir.glob('*.json')]

    print(f"Found {len(plant_files)} plant files to process\n")

    updated_count = 0
    skipped_count = 0

    for plant_file in sorted(plant_files):
        if update_plant_sun_times(plant_file):
            updated_count += 1
        else:
            skipped_count += 1
        print()

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Updated: {updated_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Total: {len(plant_files)}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
