===============================================
# 🌿 Master Garden Dashboard
_Last Updated: December 10, 2025 3:05 PM_
===============================================

A simple, self-hosted Flask web application for managing your personal garden. Track your plants, products, and garden data through an intuitive dashboard interface.

## 📋 Features

### ✅ Phase 1: Foundation Setup
- [x] Repo structure
- [ ] Flask webserver
- [ ] Data manager for JSON operations
- [ ] Base CSS styling

### Phase 2: Dynamic Master Dashboard
- [ ] Load all plant data from JSON files
- [ ] Display plants as interactive tiles
- [ ] Show basic plant info (name, status, current stage)
- [ ] Apply unified CSS styling across dashboard

### Phase 3: Plant Detail Modal
- [ ] Click plant tile to open modal overlay
- [ ] Display plant main data (origin, location, container, soil)
- [ ] Display journal entries in chronological order
- [ ] Show probe readings, observations, and actions
- [ ] Modal close functionality

### Phase 4: GPT Integration Forms
- [ ] **Update Plant Data Form**
  - Dropdown to select plant
  - Input for new journal entry (prepends to journal array)
  - Input for fragment update (updates specific main data fields)
  - Input for complete main data (replaces all main data fields)
  - Save functionality with feedback
- [ ] **Add Containers Form**
  - Form with container_name and common_name fields
  - Save to data/containers.json
  - Duplicate validation
- [ ] **Add Products Form**
  - Form with product_name and common_name fields
  - Save to data/products.json
  - Duplicate validation

### Phase 5: Photo Management System
- [ ] **Photo Upload Interface**
  - "Manage Photos" button in journal entries
  - List all photo placeholders with captions and tags
  - File upload button for each placeholder
  - Drag-and-drop zone support
  - Upload status indicators
- [ ] **Photo Processing**
  - Image compression using PIL/Pillow
  - Organized storage in static/images/plants/
  - JSON filename updates
- [ ] **Photo Display**
  - Replace placeholders with actual images
  - Thumbnail tiles in journal view
  - Click to view full size (lightbox/modal)
  - Display captions and tags

## 📁 Project Structure

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
│   ├── containers.json  # Container inventory
│   └── products.json    # Product catalog
├── docs/
│   ├── schema.md        # Data schema documentation
│   └── ...
├── static/
│   ├── images/          # Plant photos (optional)
│   │   └── ...
│   └── style.css        # Unified CSS styling
├── templates/
│   ├── add_plant.html   # Add plant form
│   ├── add_product.html # Add product form
│   ├── dashboard.html   # Master garden dashboard
│   └── ...
├── .gitignore           # Git ignore rules
├── LICENSE              # Project license
├── PROMPT.md            # AI conversation continuity
├── README.md            # This file
├── data_manager.py      # JSON operations
├── requirements.txt     # Python dependencies
└── webserver.py         # Flask server
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

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
   python webserver.py
   ```

4. **Open your browser**
   ```
   http://127.0.0.1:5000
   ```

## 🎯 Usage

### Viewing Your Garden
Navigate to the home page to see your master dashboard with all plants displayed.

### Adding Plants
Click the "Add Plant" button on the dashboard to open the form, fill in the details, and submit.

### Managing Data
All data is stored as JSON files in the `data/plants/` directory. You can manually edit these files or use the web interface.

## 🗺️ Development Roadmap

This project is being developed in phases. Check the Features section above to see current progress.

**Current Phase:** Phase 1 - Foundation Setup

**Completed:**
- ✅ Repository structure defined
- ✅ Documentation created

**Next Steps:**
- Set up Flask webserver
- Create data_manager.py
- Implement base CSS

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

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
   python webserver.py
   ```

4. **Open your browser**
   ```
   http://127.0.0.1:5000
   ```

## 🎯 Usage

### Viewing Your Garden
Navigate to the home page to see your master dashboard with all plants displayed.

### Adding Plants
Click the "Add Plant" button on the dashboard to open the form, fill in the details, and submit.

### Managing Data
All data is stored as JSON files in the `data/plants/` directory. You can manually edit these files or use the web interface.

## 🛠️ Development

### Data Structure
See `docs/schema.md` for detailed information about the JSON data schema.

### Adding New Features
1. Create new routes in `webserver.py`
2. Add corresponding HTML templates in `templates/`
3. Update `data_manager.py` for data operations
4. Styling automatically applies via `static/style.css`

## 📝 License

This project is licensed under the terms specified in the LICENSE file.

## 🤝 Contributing

This is a personal project, but feel free to fork and adapt it for your own garden management needs!

## 💡 About PROMPT.md

The `PROMPT.md` file maintains conversation context for AI assistants. If development spans multiple sessions, this file helps new AI instances understand the project's current state and continue seamlessly.

---

**Built with ❤️ for gardeners who code**