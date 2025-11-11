#!/usr/bin/env python3
"""
Garden Journal Documentation Setup Script

This script creates all the initial documentation and structure files
for the garden journal project.

Usage:
    python setup_docs.py
"""

import os
from pathlib import Path


def create_directory_structure():
    """Create all necessary directories"""
    directories = [
        'docs',
        'src',
        'data',
        'photos',
        'output',
        'templates',
        'scripts'
    ]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}/")

    # Create __init__.py in src
    Path('src/__init__.py').touch()
    print(f"✓ Created file: src/__init__.py")


def create_readme():
    """Create README.md"""
    content = '''# 🌿 Jodi's Garden Journal

A local-first garden journaling system that tracks plants, their locations, growth stages, photos, and daily observations.

## Features

- 🌱 **Plant Tracking** - Complete history of each plant from purchase through all location moves
- 📍 **Location History** - Track when plants move between locations (picnic table, panels, raised bed)
- 📷 **Photo Management** - Consistent naming convention with automatic organization
- 🌤️ **Weather Logging** - Track temperature, conditions, and environmental factors
- 📝 **Daily Observations** - Activities, observations, and Q&A from your gardening research
- 📄 **Beautiful HTML Output** - Generate print-ready HTML pages (print to PDF)
- 💾 **Local Storage** - All data in a single JSON file, no database required

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Your Garden

```bash
# Create initial data file
python scripts/init_garden.py

# Add your first plant
python scripts/add_plant.py
```

### 3. Daily Usage

```bash
# Add a daily journal entry
python scripts/add_entry.py

# Generate all HTML pages
python scripts/generate_all.py

# View your journal
open output/Garden_00_Front_Page.html
```

## Project Structure

```
garden-journal/
├── README.md                           # This file
├── data/
│   ├── garden_data.json                # Your garden data
│   └── garden_data.example.json        # Example structure
├── photos/                             # All photos (flat structure)
│   ├── basil_001_20251029_0745_1.jpg
│   └── ...
├── output/                             # Generated HTML files
│   ├── Garden_00_Front_Page.html
│   ├── Garden_01_Layout.html
│   ├── Garden_02_Plant_by_Plant_Summary.html
│   └── Garden_03_Daily_20251111.html
├── templates/                          # HTML templates
│   ├── base_template.html
│   ├── front_page_template.html
│   └── daily_journal_template.html
├── src/                                # Core Python modules
│   ├── schema.py                       # Data validation
│   ├── data_manager.py                 # JSON read/write
│   ├── html_generator.py               # Generate HTML
│   └── photo_manager.py                # Photo utilities
├── scripts/                            # Executable scripts
│   ├── init_garden.py
│   ├── add_plant.py
│   ├── add_entry.py
│   ├── generate_all.py
│   └── rename_photos.py
└── docs/                               # Documentation
    ├── data-structure.md               # JSON schema details
    ├── photo-naming.md                 # Photo conventions
    ├── workflow.md                     # Daily usage guide
    └── setup.md                        # Setup instructions
```

## Documentation

- **[Data Structure](docs/data-structure.md)** - Complete JSON schema and examples
- **[Photo Naming](docs/photo-naming.md)** - Photo organization and naming conventions
- **[Workflow Guide](docs/workflow.md)** - Daily usage and best practices
- **[Setup Instructions](docs/setup.md)** - First-time setup and configuration

## Core Concepts

### Plants are Primary

Each plant has a unique ID (e.g., `basil_001`) and tracks:
- Complete location history (from purchase through all moves)
- Current location and container details
- Growth stages and care history
- All associated photos

### Photo Naming Convention

Photos use a consistent naming format:

```
{plant_id}_{YYYYMMDD}_{HHMM}_{seq}.jpg
```

Example: `basil_001_20251105_0745_1.jpg`

See [docs/photo-naming.md](docs/photo-naming.md) for details.

### Daily Journal Structure

Each day can include:
- Weather conditions
- Activities performed
- General observations
- Questions & answers from research
- Individual plant observations with photos

## Example Usage

### Adding a New Plant

```bash
python scripts/add_plant.py
```

```
Plant ID: basil_001
Common Name: Basil - Left
Variety: Sweet Basil
Purchase Date (YYYYMMDD): 20251008
Location: Picnic Table
Container: 8" white round pot, 0.94 gal
Soil Mix: Miracle-Gro Moisture Control
```

### Creating a Daily Entry

```bash
python scripts/add_entry.py
```

The script will prompt you for:
- Date and time
- Weather (optional)
- Activities
- Observations
- Q&A pairs (optional)
- Plant-specific observations

### Generating HTML Pages

```bash
# Generate everything
python scripts/generate_all.py

# Generate only daily journals
python scripts/generate_all.py --daily-only

# Generate only static pages
python scripts/generate_all.py --static-only
```

## HTML Output

The system generates:

1. **Garden_00_Front_Page.html** - Title page and table of contents
2. **Garden_01_Layout.html** - Panel/container layout table
3. **Garden_02_Plant_by_Plant_Summary.html** - Complete plant reference
4. **Garden_03_Daily_YYYYMMDD.html** - Individual daily journals

All pages use consistent styling and can be printed to PDF.

## Why This Approach?

- ✅ **Fully local** - No internet required, no accounts
- ✅ **Simple backups** - Just copy the folder
- ✅ **Future-proof** - Plain JSON and HTML
- ✅ **Version control friendly** - Can use Git
- ✅ **No vendor lock-in** - Your data, your format
- ✅ **Printable** - HTML to PDF anytime
- ✅ **Extensible** - Easy to add features

## Contributing

This is a personal project, but feel free to fork and adapt for your own garden!

## License

MIT License - See LICENSE file for details

---

**Happy Gardening! 🌱**
'''

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Created file: README.md")


def create_data_structure_doc():
    """Create docs/data-structure.md"""
    content = '''# Garden Journal Data Structure

## Overview

The garden journal uses a single JSON file (`data/garden_data.json`) to store all garden data. This document describes the complete schema.

## File Location

```
data/garden_data.json
```

## Root Structure

```json
{
  "metadata": { },
  "plants": [ ],
  "locations": { },
  "daily_entries": [ ]
}
```

---

## Metadata

Information about the garden itself.

```json
{
  "metadata": {
    "garden_name": "Jodi's Garden Journal",
    "start_date": "2025-10-08",
    "location": "Miami, Florida",
    "garden_type": "Container/Fence Panel Garden",
    "last_updated": "2025-11-11"
  }
}
```

### Fields

- `garden_name` (string) - Display name for your garden
- `start_date` (string) - Date garden started (YYYYMMDD)
- `location` (string) - Geographic location
- `garden_type` (string) - Type of garden setup
- `last_updated` (string) - Last modification date

---

## Plants Array

Each plant in your garden. **Plants are the primary entity** - locations are tracked as history.

### Plant Object Structure

```json
{
  "plant_id": "basil_001",
  "common_name": "Basil - Left",
  "variety": "Sweet Basil",
  "purchase_date": "20251008",
  "source": "Local Nursery",
  "status": "active",

  "location_history": [
    {
      "date": "20251008",
      "location": "Picnic Table",
      "container": "8\\" white round pot, 0.94 gal",
      "soil_mix": "Miracle-Gro Moisture Control",
      "reason": "Initial purchase, observation period"
    }
  ],

  "current_location": {
    "location": "Panel 1",
    "container": "8\\" white round pot, 0.94 gal",
    "soil_mix": "Miracle-Gro Moisture Control"
  }
}
```

For complete field definitions, see the full documentation in the repository.

---

## Daily Entries Array

Records of daily observations and activities.

See `data/garden_data.example.json` for a complete working example.

---

## See Also

- [Photo Naming Convention](photo-naming.md)
- [Daily Workflow](workflow.md)
- [Setup Instructions](setup.md)
'''

    with open('docs/data-structure.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Created file: docs/data-structure.md")


def create_photo_naming_doc():
    """Create docs/photo-naming.md"""
    content = '''# Photo Naming Convention

## Overview

All garden photos use a consistent naming format that embeds metadata directly in the filename.

---

## Format

```
{plant_id}_{YYYYMMDD}_{HHMM}_{seq}.jpg
```

### Components

1. **plant_id** - The plant's unique identifier (matches `plant_id` in JSON)
2. **YYYYMMDD** - Full date (year, month, day)
3. **HHMM** - Time in 24-hour military format
4. **seq** - Photo sequence number (1, 2, 3, 4, ...)

---

## Examples

```
basil_001_20251105_0745_1.jpg
tomato_001_20251105_1430_1.jpg
strawberry_001_20251107_0830_2.jpg
```

---

## Storage Structure

All photos in one flat directory:

```
photos/
├── basil_001_20251029_0745_1.jpg
├── basil_001_20251029_0745_2.jpg
├── tomato_001_20251029_0745_1.jpg
└── ...
```

---

## Military Time Reference

| 12-Hour | 24-Hour |
|---------|---------|
| 7:45 AM | 0745 |
| 12:00 PM | 1200 |
| 2:30 PM | 1430 |
| 5:00 PM | 1700 |

---

## See Also

- [Data Structure](data-structure.md)
- [Workflow Guide](workflow.md)
'''

    with open('docs/photo-naming.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Created file: docs/photo-naming.md")


def create_schema_py():
    """Create src/schema.py"""
    content = '''"""
Garden Journal Data Schema
Defines the structure for garden_data.json and provides validation functions.
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict


def validate_plant_id(plant_id: str) -> bool:
    """Validate plant_id format: {planttype}_{number}"""
    pattern = r'^[a-z_]+_\\d{3}$'
    return bool(re.match(pattern, plant_id))


def validate_date(date_str: str) -> bool:
    """Validate date format: YYYYMMDD"""
    if not re.match(r'^\\d{8}$', date_str):
        return False

    try:
        year = int(date_str[:4])
        month = int(date_str[4:6])
        day = int(date_str[6:8])

        if not (1900 <= year <= 2100):
            return False
        if not (1 <= month <= 12):
            return False
        if not (1 <= day <= 31):
            return False

        return True
    except ValueError:
        return False


def validate_time(time_str: str) -> bool:
    """Validate time format: HHMM (military/24-hour time)"""
    if not re.match(r'^\\d{4}$', time_str):
        return False

    try:
        hour = int(time_str[:2])
        minute = int(time_str[2:])
        return 0 <= hour <= 23 and 0 <= minute <= 59
    except ValueError:
        return False


def validate_photo_filename(filename: str) -> bool:
    """Validate photo filename format: {plant_id}_{YYYYMMDD}_{HHMM}_{seq}.jpg"""
    pattern = r'^[a-z_]+_\\d{3}_\\d{8}_\\d{4}_\\d+\\.jpg$'

    if not re.match(pattern, filename):
        return False

    parts = filename.replace('.jpg', '').split('_')
    if len(parts) < 5:
        return False

    plant_id = f"{parts[0]}_{parts[1]}"
    date = parts[2]
    time = parts[3]

    return (validate_plant_id(plant_id) and
            validate_date(date) and
            validate_time(time))


def format_date_display(date_str: str) -> str:
    """Format a date string (YYYYMMDD) for display"""
    if not validate_date(date_str):
        return date_str

    months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    year = int(date_str[:4])
    month = int(date_str[4:6])
    day = int(date_str[6:8])

    return f"{months[month-1]} {day}, {year}"


def format_time_display(time_str: str) -> str:
    """Format a time string (HHMM) for display in 12-hour format"""
    if not validate_time(time_str):
        return time_str

    hour = int(time_str[:2])
    minute = int(time_str[2:])

    period = "AM" if hour < 12 else "PM"
    display_hour = hour if hour <= 12 else hour - 12
    if display_hour == 0:
        display_hour = 12

    return f"{display_hour}:{minute:02d} {period}"


if __name__ == "__main__":
    # Test validation functions
    print("Testing validation functions...")

    assert validate_plant_id("basil_001") == True
    assert validate_plant_id("basil001") == False
    print("✓ Plant ID validation working")

    assert validate_date("20251105") == True
    assert validate_date("2025-11-05") == False
    print("✓ Date validation working")

    assert validate_time("0745") == True
    assert validate_time("2400") == False
    print("✓ Time validation working")

    assert validate_photo_filename("basil_001_20251105_0745_1.jpg") == True
    assert validate_photo_filename("basil_20251105_0745_1.jpg") == False
    print("✓ Photo filename validation working")

    print("\\n✅ All validation tests passed!")
'''

    with open('src/schema.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Created file: src/schema.py")


def create_example_json():
    """Create data/garden_data.example.json"""
    content = '''{
  "metadata": {
    "garden_name": "Example Garden Journal",
    "start_date": "20251001",
    "location": "Miami, Florida",
    "garden_type": "Container/Fence Panel Garden"
  },

  "plants": [
    {
      "plant_id": "basil_001",
      "common_name": "Basil - Left",
      "variety": "Sweet Basil",
      "purchase_date": "20251001",
      "source": "Local Nursery",
      "status": "active",

      "location_history": [
        {
          "date": "20251001",
          "location": "Picnic Table",
          "container": "8\\" white round pot, 0.94 gal",
          "soil_mix": "Miracle-Gro Moisture Control",
          "reason": "Initial purchase"
        }
      ],

      "current_location": {
        "location": "Picnic Table",
        "container": "8\\" white round pot, 0.94 gal",
        "soil_mix": "Miracle-Gro Moisture Control"
      },

      "care_history": [],
      "growth_stages": []
    }
  ],

  "locations": {
    "Picnic Table": {
      "type": "temporary_staging",
      "description": "Initial placement area"
    }
  },

  "daily_entries": []
}
'''

    with open('data/garden_data.example.json', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Created file: data/garden_data.example.json")


def create_gitignore():
    """Create .gitignore"""
    content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Garden Journal specific
data/garden_data.json
photos/*.jpg
output/*.html

# Keep example files
!data/garden_data.example.json

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
'''

    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Created file: .gitignore")


def main():
    """Main setup function"""
    print("🌿 Setting up Garden Journal Documentation...\n")

    try:
        # Create directory structure
        print("Creating directories...")
        create_directory_structure()
        print()

        # Create documentation files
        print("Creating documentation files...")
        create_readme()
        create_data_structure_doc()
        create_photo_naming_doc()
        print()

        # Create source files
        print("Creating source files...")
        create_schema_py()
        create_example_json()
        create_gitignore()
        print()

        print("✅ Setup complete!\n")
        print("📁 Your project structure:")
        print("""
garden-journal/
├── README.md
├── .gitignore
├── docs/
│   ├── data-structure.md
│   └── photo-naming.md
├── src/
│   ├── __init__.py
│   └── schema.py
├── data/
│   └── garden_data.example.json
├── photos/
├── output/
├── templates/
└── scripts/
""")
        print("🎯 Next steps:")
        print("  1. Review README.md for project overview")
        print("  2. Check docs/ for detailed documentation")
        print("  3. Run 'python src/schema.py' to test validation")
        print("\n🌱 Happy gardening!")

    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())