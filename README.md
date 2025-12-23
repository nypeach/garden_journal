===============================================
# 🌿 Master Garden Dashboard
_Last Updated: December 22, 2025 7:39 PM_
===============================================

A simple, self-hosted Flask web application for managing your personal garden. Track your plants, products, and garden data through an intuitive dashboard interface with dynamic categorization and detailed plant histories.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Overview

Master Garden Dashboard is a personal garden management system designed for gardeners who code. It provides a clean, organized way to track plant origins, monitor growth stages, log journal entries with environmental data, and maintain a complete history of your garden.

Built with simplicity in mind, the dashboard uses file-based JSON storage (no database required) and displays your plants in an intuitive, category-organized layout. Whether you're managing herbs, vegetables, flowers, or fruit plants, everything is accessible through a beautiful web interface.

## Features

### ✅ Completed (Phase 1, 2, 3 & 5 - Complete!)
- **Dynamic plant dashboard** with real-time data from JSON files
- **Category-based organization** with custom emoji navigation
- **Plant journal modal** - Click any plant to view complete journal history
- **Comprehensive journal entries** - Date/time, conditions, probe readings, observations, actions, photos
- **Digital & analog probe data** - pH, EC, moisture, fertility, temperature tracking
- **Photo prep tool** - Drag & drop upload, compression, renaming, organization
- **Probe reading identification** - User-selectable checkboxes to mark probe screenshots
- **HEIC support** - Direct upload from iPhone Photos app
- **EXIF orientation correction** - Photos display right-side up automatically
- **Smart message system** - Global weather + plant-specific messages with intelligent reset
- **Date persistence** - Process multiple plants on same date without re-entering
- **Google Drive integration** - Photos served from organized subfolders
- **ChatGPT workflow** - Automated filename generation with probe reading markers
- **Placeholder photo upload** - Click or drag to backfill photos in past entries
- **Photo lightbox** - Single-click to view full-size with caption footer
- **Auto-JSON updates** - Placeholder uploads automatically update plant files
- **Plant ID validation** - Autocomplete dropdown with existing plants
- **Photo display in journals** - Compressed images with captions
- **Responsive modal overlay** - ESC key and backdrop click to close
- **Unified CSS styling** - Single stylesheet for dashboard and journal
- **Flexible data structure** supporting unlimited plants
- **Easy data management** through JSON files
- **Fast and lightweight** - no database overhead
- **Self-hosted** - complete control over your data

### 🚧 In Development (Phase 4)
- **New Journal Entry Workflow** - Add journal entries directly from dashboard through Photo Prep
- **JSON Input Form** - Paste ChatGPT journal JSON and save to plant files
- **Update Plant Data** - Edit plant metadata (stage, state, timeline)

## Project Structure

```
garden_journal/
├── chatgpt/
│   ├── master_garden_ai_guide.md
│   ├── master_garden_ai_prompt.md
│   ├── master_garden_dashboard.html    # Sample static files
│   ├── strawberry_left_journal.html
│   └── master_garden_ai_prompt_generator.py
├── data/
│   ├── plants/
│   │   ├── strawberry_001.json
│   │   ├── basil_001.json
│   │   └── ...
│   ├── containers.json      # Container inventory
│   ├── dashboard_order.json # Dashboard category ordering
│   ├── meta.json            # Garden metadata
│   └── products.json        # Product catalog
├── docs/
│   ├── schema.md                # Data schema documentation
│   ├── photo_requirements.md    # Photo handling system requirements
│   └── ...
├── static/
│   ├── images/              # Plant photos
│   │   └── plants/          # Organized by plant
│   ├── style.css            # Unified CSS styling
│   └── modal.js             # Modal interaction JavaScript
├── templates/
│   ├── dashboard.html       # Master garden dashboard
│   └── journal.html         # Plant journal template
├── .gitignore               # Git ignore rules
├── LICENSE                  # Project license
├── PROMPT.md                # AI conversation continuity
├── README.md                # This file
├── app.py                   # Flask server
├── data_manager.py          # JSON operations
└── requirements.txt         # Python dependencies
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### From Source

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/garden_journal.git
   cd garden_journal
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python3 app.py
   ```

4. **Open your browser**
   ```
   http://localhost:3000
   ```

## Usage

### Viewing Your Garden

Navigate to `http://localhost:3000` to see your master dashboard with all plants displayed and organized by categories (Fruit, Vegetables, Herbs & Greens, etc.).

### Viewing Plant Journals

Click the "📓 View Journal" link on any plant card to open a modal overlay showing:
- Complete journal history (newest to oldest)
- Digital probe readings (pH, EC, moisture, fertility, temperature)
- Analog probe readings (fertility, moisture, pH descriptions)
- Observations and actions taken
- Follow-up notes with timestamps
- Photo placeholders and actual images with captions

### Closing the Journal

- Press **ESC** key
- Click outside the modal (on the dark backdrop)

## Configuration

### Changing the Port

The application runs on port 3000 by default. To change this, edit `app.py`:

```python
app.run(host='0.0.0.0', port=YOUR_PORT, debug=True)
```

### Adding Plants

Add new plant JSON files to the `data/plants/` directory following the schema in `docs/schema.md`. Update `data/dashboard_order.json` to include the new plant in your desired category.

## Roadmap

### ✅ Phase 1: Foundation Setup (COMPLETE)
- [x] Flask webserver (`app.py`)
- [x] Data manager for JSON operations (`data_manager.py`)
- [x] Base CSS styling (`style.css`)

### ✅ Phase 2: Dynamic Master Dashboard (COMPLETE)
- [x] Load all plant data from JSON files
- [x] Display plants as interactive tiles
- [x] Category grouping with `dashboard_order.json`
- [x] Navigation chips with emojis

### ✅ Phase 3: Plant Detail Modal (COMPLETE)
- [x] Create modal overlay component
- [x] Display plant journal with current state and stage
- [x] Show complete journal entries with all data fields
- [x] Display probe readings (digital and analog)
- [x] Show observations, actions, follow-ups
- [x] Display photo grid with captions
- [x] Modal interaction controls (ESC, backdrop click)
- [x] Dynamic journal route (`/journal/<plant_id>`)

### Phase 4: GPT Integration Forms
- [ ] Update Plant Data Form (journal entries, fragments, complete data)
- [ ] Add Containers Form
- [ ] Add Products Form

### ✅ Phase 5: Photo Management System (COMPLETE)
- [x] **Photo Prep Tool** - Web form for batch photo processing
  - [x] Upload multiple photos (drag & drop or click)
  - [x] Automated renaming with plant_id-date-number pattern
  - [x] Image compression (PIL/Pillow, 85% quality)
  - [x] HEIC format support via pillow-heif
  - [x] EXIF orientation correction (photos display right-side up)
  - [x] Organized subfolder structure by plant
  - [x] Generate ChatGPT message with filename list
  - [x] Probe reading warning for -01 photos
  - [x] Smart message system (global weather + plant-specific)
  - [x] Intelligent reset buttons (process another plant vs start fresh)
- [x] **Google Drive Integration**
  - [x] Serve photos from Google Drive folder
  - [x] Photos organized in plant-specific subfolders
  - [x] Sync across devices
  - [x] Update journal template to use photo route
- [x] **Placeholder Photo Upload**
  - [x] Click or drag & drop to upload photo
  - [x] Automatic naming and organization
  - [x] JSON auto-update with filename
  - [x] EXIF orientation correction
  - [x] Immediate display update
- [x] **Photo Lightbox Modal**
  - [x] Single-click to view full-size
  - [x] Caption footer attached to image (matches journal style)
  - [x] Proper aspect ratio for portrait and landscape
  - [x] Close with ESC or backdrop click

## Contributing

This is a personal project, but contributions are welcome! Feel free to:
- Fork the repository
- Submit issues for bugs or feature requests
- Create pull requests with improvements

### Development Guidelines
- Keep it simple and lean
- Follow the existing code structure
- Test thoroughly before submitting PRs
- Update documentation for new features

### Development Setup
```bash
git clone https://github.com/yourusername/garden_journal.git
cd garden_journal
pip install -r requirements.txt
python3 app.py
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **Flask** - Lightweight and powerful Python web framework
- **ChatGPT** - AI integration for plant-specific horticultural guidance
- **Open-source community** - For tools, libraries, and inspiration

---

**Built with ❤️ for gardeners who code**
**Added this message to make sure repo is syncing"
