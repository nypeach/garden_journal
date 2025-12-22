#!/usr/bin/env python3
"""
Master Garden AI Prompt Generator
==================================
Generates individualized plant channel markdown files from master template.

Reads all plant JSON files from data/plants/ (including inactive subdirectory)
and creates a channel-specific markdown file for each one by combining:
1. The plant's ID and name
2. The master_garden_ai_prompt.md template
3. The master_garden_ai_guide.md guide

Output files go to docs/temp/ and are ready to copy/paste into ChatGPT.

Usage:
    python3 chatgpt/master_garden_ai_prompt_generator.py

Or click "Run Python File" button in Cursor/VS Code
"""

import json
import sys
from pathlib import Path


def load_master_guide(script_dir):
    """Load the Master Garden AI Guide markdown."""
    guide_path = script_dir / "master_garden_ai_guide.md"

    if not guide_path.exists():
        print(f"❌ Error: Master guide not found: {guide_path}")
        sys.exit(1)

    with open(guide_path, 'r', encoding='utf-8') as f:
        return f.read()


def load_prompt_template(script_dir):
    """Load the Master Garden AI Prompt template markdown."""
    template_path = script_dir / "master_garden_ai_prompt.md"

    if not template_path.exists():
        print(f"❌ Error: Prompt template not found: {template_path}")
        sys.exit(1)

    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def load_plant_data(json_file):
    """
    Load plant ID and name from JSON file.

    Returns:
        tuple: (plant_id, plant_name) or (None, None) if error
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

            plant_id = data.get('id')
            plant_name = data.get('plant')

            if not plant_id or not plant_name:
                print(f"⚠️  Skipping {json_file.name}: Missing 'id' or 'plant' field")
                return None, None

            return plant_id, plant_name

    except json.JSONDecodeError as e:
        print(f"✗ Error parsing {json_file.name}: {e}")
        return None, None
    except IOError as e:
        print(f"✗ Error reading {json_file.name}: {e}")
        return None, None


def create_plant_channel_intro(template, plant_id, plant_name):
    """
    Create the plant-specific introduction section.

    Replaces {{PLANT_ID}} and {{PLANT_NAME}} placeholders in template.
    """
    intro = template.replace("{{PLANT_ID}}", plant_id)
    intro = intro.replace("{{PLANT_NAME}}", plant_name)
    return intro


def generate_plant_channel_markdown(prompt_template, master_guide, plant_id, plant_name):
    """Generate the complete plant channel markdown file."""
    intro = create_plant_channel_intro(prompt_template, plant_id, plant_name)
    return intro + "\n" + master_guide


def main():
    """Main function to generate all plant channel markdown files."""

    # Define paths
    script_dir = Path(__file__).parent
    plants_dir = script_dir.parent / "data" / "plants"
    prompt_dir = script_dir.parent / "docs" / "temp"

    print("🌱 Plant Channel Markdown Generator")
    print("=" * 60)

    # Create prompt directory if it doesn't exist
    prompt_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Output directory ready: {prompt_dir}")

    # Load the master guide template
    print("\n📖 Loading Master Garden AI Guide...")
    master_guide = load_master_guide(script_dir)
    print(f"✓ Loaded master_garden_ai_guide.md ({len(master_guide)} characters)")

    # Load the prompt template
    print("\n📝 Loading prompt template...")
    prompt_template = load_prompt_template(script_dir)
    print(f"✓ Loaded master_garden_ai_prompt.md ({len(prompt_template)} characters)")

    # Find all JSON files in the main plants directory
    print(f"\n🔍 Scanning for plant JSON files in {plants_dir}...")
    json_files = sorted(plants_dir.glob("*.json"))

    # Also scan inactive subdirectory if it exists
    inactive_dir = plants_dir / 'inactive'
    if inactive_dir.exists() and inactive_dir.is_dir():
        json_files.extend(sorted(inactive_dir.glob("*.json")))

    if not json_files:
        print(f"❌ No JSON files found in {plants_dir}")
        sys.exit(1)

    print(f"✓ Found {len(json_files)} JSON files (including inactive)")

    # Process each JSON file
    print("\n🌿 Generating plant channel markdown files...")
    print("-" * 60)

    created_count = 0
    skipped_count = 0

    for json_file in json_files:
        # Load plant data from JSON
        plant_id, plant_name = load_plant_data(json_file)

        if not plant_id or not plant_name:
            skipped_count += 1
            continue

        # Generate output filename
        output_file = prompt_dir / f"{plant_id}_channel.md"

        try:
            # Generate markdown content
            markdown_content = generate_plant_channel_markdown(
                prompt_template, master_guide, plant_id, plant_name
            )

            # Write to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            created_count += 1
            print(f"✓ Created: {output_file.name} ({plant_name})")

        except IOError as e:
            print(f"✗ Error creating {output_file.name}: {e}")
            skipped_count += 1

    # Summary
    print("\n" + "=" * 60)
    print(f"✓ Successfully created: {created_count} files")
    if skipped_count > 0:
        print(f"⚠️  Skipped: {skipped_count} files (see warnings above)")
    print(f"📁 Output directory: {prompt_dir}")
    print("=" * 60)

    if created_count == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()