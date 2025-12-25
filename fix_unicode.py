#!/usr/bin/env python3
"""
Script to replace unicode/special characters with escaped sequences in JSON files.
"""
import json
import os
import glob

def escape_unicode_in_value(value):
    """Recursively escape unicode characters in JSON values."""
    if isinstance(value, str):
        # Encode to ASCII with backslashreplace to get escaped sequences
        return value.encode('ascii', 'backslashreplace').decode('ascii')
    elif isinstance(value, dict):
        return {k: escape_unicode_in_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [escape_unicode_in_value(item) for item in value]
    else:
        return value

def process_json_file(filepath):
    """Process a single JSON file to escape unicode characters."""
    print(f"Processing {filepath}...")

    try:
        # Read the JSON file
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Escape unicode characters
        escaped_data = escape_unicode_in_value(data)

        # Write back to file with proper formatting
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(escaped_data, f, indent=2, ensure_ascii=True)

        print(f"  ✓ Successfully processed {filepath}")
        return True
    except Exception as e:
        print(f"  ✗ Error processing {filepath}: {e}")
        return False

def main():
    """Main function to process all plant JSON files."""
    # Get all JSON files in data/plants
    json_files = glob.glob('data/plants/*.json')

    if not json_files:
        print("No JSON files found in data/plants/")
        return

    print(f"Found {len(json_files)} JSON files to process\n")

    success_count = 0
    for filepath in sorted(json_files):
        if process_json_file(filepath):
            success_count += 1

    print(f"\n{'='*60}")
    print(f"Processed {success_count}/{len(json_files)} files successfully")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
