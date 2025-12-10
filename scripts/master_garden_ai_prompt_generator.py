#!/usr/bin/env python3
"""
Generate Plant Channel markdown files for all plants in the garden journal.

This script reads JSON files from data/plants/ and generates corresponding
markdown files in data/plants/prompt/ with the Master Garden Assistant Guide.

The script dynamically loads:
- Master Garden AI Guide from master_garden_ai_guide.md
- Custom prompt intro from master_garden_ai_prompt_new.md
- Plant data from all JSON files in data/plants/

Usage:
    python3 generate_plant_channels.py
"""

import json
from pathlib import Path
import sys


def load_master_guide(script_dir: Path) -> str:
    """Load the Master Garden AI Guide from the docs directory."""
    guide_path = script_dir.parent / "docs" / "master_garden_ai_guide.md"

    try:
        with open(guide_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: Could not find {guide_path}")
        print(f"   Please ensure master_garden_ai_guide.md exists in docs/")
        sys.exit(1)
    except IOError as e:
        print(f"❌ Error reading {guide_path}: {e}")
        sys.exit(1)


def load_prompt_template(script_dir: Path) -> str:
    """Load the custom prompt intro template from the docs directory."""
    prompt_path = script_dir.parent / "docs" / "master_garden_ai_prompt.md"

    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: Could not find {prompt_path}")
        print(f"   Please ensure master_garden_ai_prompt.md exists in docs/")
        sys.exit(1)
    except IOError as e:
        print(f"❌ Error reading {prompt_path}: {e}")
        sys.exit(1)


def load_plant_data(json_file: Path) -> tuple[str, str]:
    """
    Load plant ID and name from a JSON file.

    Returns:
        tuple: (plant_id, plant_name)
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        plant_id = data.get("id")
        plant_name = data.get("plant")

        if not plant_id:
            print(f"⚠️  Warning: {json_file.name} is missing 'id' attribute")
            return None, None

        if not plant_name:
            print(f"⚠️  Warning: {json_file.name} is missing 'plant' attribute")
            return None, None

        return plant_id, plant_name

    except json.JSONDecodeError as e:
        print(f"⚠️  Warning: Could not parse {json_file.name}: {e}")
        return None, None
    except IOError as e:
        print(f"⚠️  Warning: Could not read {json_file.name}: {e}")
        return None, None


def create_plant_channel_intro(prompt_template: str, plant_id: str, plant_name: str) -> str:
    """
    Create the intro section by replacing placeholders in the template.

    Args:
        prompt_template: Template string with {plant_id} and {plant_name} placeholders
        plant_id: The plant's ID value
        plant_name: The plant's name value

    Returns:
        Formatted intro string with values substituted
    """
    intro = prompt_template.replace("{plant_id}", plant_id)
    intro = intro.replace("{plant_name}", plant_name)
    return intro


def generate_plant_channel_markdown(prompt_template: str, master_guide: str,
                                   plant_id: str, plant_name: str) -> str:
    """Generate complete markdown content for a plant channel."""
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

    # Find all JSON files in the plants directory
    print(f"\n🔍 Scanning for plant JSON files in {plants_dir}...")
    json_files = sorted(plants_dir.glob("*.json"))

    if not json_files:
        print(f"❌ No JSON files found in {plants_dir}")
        sys.exit(1)

    print(f"✓ Found {len(json_files)} JSON files")

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