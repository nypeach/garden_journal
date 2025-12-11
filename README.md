===============================================
# 🌿 Master Garden Dashboard
_Last Updated: December 10, 2025 9:07 PM_
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

### ✅ Completed (Phase 1 & 2)
- **Dynamic plant dashboard** with real-time data from JSON files
- **Category-based organization** with custom emoji navigation
- **Responsive design** with unified CSS styling
- **Flexible data structure** supporting unlimited plants
- **Easy data management** through JSON files
- **Fast and lightweight** - no database overhead
- **Self-hosted** - complete control over your data

### 🚧 In Development
- **Plant detail modals** with complete journal history
- **Data entry forms** for adding/updating plants
- **Photo management system** with compression and tagging
- **ChatGPT integration** for plant-specific horticultural guidance

## Project Structure

```
garden_journal/
├── chatgpt/
│   ├── master_garden_ai_guide.md
│   ├── master_garden_ai_prompt.md
│   └── master_garden_ai_prompt_generator.py
├── data/
│   ├── plants/
│   │   ├── plant1.json
│   │   ├── plant2.json
│   │   └── ...
│   ├── containers.json      # Container inventory
│   ├── dashboard_order.json # Dashboard category ordering
│   ├── meta.json            # Garden metadata
│   └── products.json        # Product catalog
├── docs/
│   ├── schema.md            # Data schema documentation
│   └── ...
├── static/
│   ├── images/              # Plant photos (optional)
│   │   └── ...
│   └── style.css            # Unified CSS styling
├── templates/
│   ├── dashboard.html       # Master garden dashboard
│   └── ...
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

### Managing Plant Data

All data is stored as JSON files in the `data/` directory:

**Individual plant files:** `data/plants/*.json`
```json
{
  "id": "basil_001",
  "status": "Active",
  "plant": "Basil (Left)",
  "current_stage": "Clustered Regrowth Phase",
  "timeline": [...],
  "journal": [...]
}
```

**Category ordering:** `data/dashboard_order.json`
```json
{
  "categories": [
    {
      "name": "Herbs & Greens",
      "emoji": "🌿",
      "plants": ["basil_001", "cilantro_001", ...]
    }
  ]
}
```

You can manually edit these files or use the web interface once forms are built (Phase 4).

### Adding New Plants

1. Create a new JSON file in `data/plants/` following the schema in `docs/schema.md`
2. Add the plant ID to the appropriate category in `data/dashboard_order.json`
3. Refresh the dashboard

## Configuration

### Dashboard Ordering

Edit `data/dashboard_order.json` to customize category grouping, display order, and navigation emojis:

```json
{
  "categories": [
    {
      "parent_order": 1,
      "parent": "Vegetables",
      "name": "Tomatoes",
      "emoji": "🍅",
      "anchor": "tomatoes",
      "plants": ["tomato_001", "tomato_002"]
    }
  ]
}
```

### Garden Metadata

Configure garden-wide settings in `data/meta.json`:

```json
{
  "metadata": {
    "garden_name": "My Garden",
    "location": "City, State",
    "garden_type": "Container Garden"
  }
}
```

### Server Configuration

The Flask server runs on port 3000 by default. To change this, edit `app.py`:

```python
app.run(host='0.0.0.0', port=YOUR_PORT, debug=True)
```

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

### Phase 3: Plant Detail Modal
- [ ] Create modal overlay component
- [ ] Display plant main data and origin history
- [ ] Show journal entries with probe readings
- [ ] Modal interaction controls (close, keyboard support)

### Phase 4: GPT Integration Forms
- [ ] Update Plant Data Form
- [ ] Add Containers Form
- [ ] Add Products Form

### Phase 5: Photo Management System
- [ ] Photo upload interface
- [ ] Image compression using PIL/Pillow
- [ ] Photo display in journal with lightbox

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