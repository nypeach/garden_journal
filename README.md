# 🌿 Jodi's Garden Journal

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
