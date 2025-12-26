#!/usr/bin/env python3
"""
Script to fix improperly escaped unicode characters in JSON files.
Converts \\xNN format back to proper \\uNNNN JSON unicode escapes.
"""
import json
import os
import glob
import re

def fix_escaped_unicode(text):
    """Convert \\xNN and \\uNNNN patterns to proper unicode characters."""
    if not isinstance(text, str):
        return text

    # Replace \\xNN hex escapes (like \\xb0 for degree symbol)
    def replace_hex(match):
        hex_value = match.group(1)
        return chr(int(hex_value, 16))

    text = re.sub(r'\\x([0-9a-fA-F]{2})', replace_hex, text)

    # Replace \\uNNNN unicode escapes (like \\u2013 for en dash)
    def replace_unicode(match):
        hex_value = match.group(1)
        return chr(int(hex_value, 16))

    text = re.sub(r'\\u([0-9a-fA-F]{4})', replace_unicode, text)

    return text

def fix_value(value):
    """Recursively fix unicode in JSON values."""
    if isinstance(value, str):
        return fix_escaped_unicode(value)
    elif isinstance(value, dict):
        return {k: fix_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [fix_value(item) for item in value]
    else:
        return value

def process_json_file(filepath):
    """Process a single JSON file to fix unicode characters."""
    print(f"Processing {filepath}...")

    try:
        # Read the JSON file
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Fix unicode characters
        fixed_data = fix_value(data)

        # Write back to file with proper formatting
        # ensure_ascii=False allows unicode characters to be written directly
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(fixed_data, f, indent=2, ensure_ascii=False)

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
