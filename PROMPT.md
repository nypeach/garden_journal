# Garden Journal Project - Current Status

**Last Updated:** November 11, 2025 @ 5:45 PM EST
**Current Version:** 13
**GitHub Repo:** garden-journal

---

## 🎯 Project Goal

Build a local-first garden journaling system to track plants, their complete location history, growth stages, photos, and detailed daily observations. Replace ChatGPT-based tracking with a proper Python/HTML system that gives full control over data, timestamps, and organization.

---

## ✅ COMPLETED

### 1. Project Structure Created

**Repository:** `garden-journal` (synced to GitHub)

**Directory structure:**
```
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
├── photos/ (excluded from git due to size)
├── output/
├── templates/
│   ├── base.css
│   ├── daily_journal_template.html
│   └── sample_daily_journal.html
├── scripts/
│   └── compress_photos.py
├── html_examples/ (reference files from ChatGPT)
├── chatGPT_conversations/ (PDFs of chat history)
├── setup_docs.py
└── setup_templates_V13.py
```

### 2. Documentation (VERSION 13)

**Files created:**
- `README.md` - Project overview, quick start guide, features
- `docs/data-structure.md` - Complete JSON schema with all V13 enhancements
- `docs/photo-naming.md` - Photo naming conventions and best practices
- `src/schema.py` - Python validation functions and dataclasses
- `data/garden_data.example.json` - Working example with V13 structure
- `PROMPT.md` - This file - handoff documentation

### 3. Data Schema (VERSION 13)

**Core design:**
- **Plants are primary entities** with unique IDs (basil_001, tomato_001, etc.)
- **Locations are separate from containers** - plants can move (Picnic Table → Panel 14 → Panel 1)
- **Complete location history** - Track every move with dates and reasons
- **Shared containers supported:**
  - **With stakes:** Pepper Box (3 peppers at stakes 1-3), Raised Bed (4 stakes)
  - **With positions:** Garlic Box (garlic in sections, scallions at edges), Arugula/Cilantro Box

**VERSION 13 major features:**
1. Multiple observations per plant per day (with timestamps)
2. Photo metadata (before/after tags, captions, timestamps)
3. Detailed action tracking (amounts: "1½ cups", products: "Captain Jack's Neem Oil", methods)
4. Soil moisture descriptions ("bone dry", "lightly moist", "dry 1 inch down", etc.)
5. Temporary location tracking (brought indoors, covered overnight, etc.)
6. Position field for shared containers ("left section", "edges", "center")
7. Upcoming actions array (plan future tasks)
8. Product/brand tracking in care history
9. Container naming system for grouping plants
10. Stake number support for staked containers

### 4. Photo System

**Naming convention:** `{plant_id}_{YYYYMMDD}_{HHMM}_{seq}.jpg`

**Examples:**
- `basil_001_20251111_1400_1.jpg` - Basil #1, Nov 11 2025, 2:00 PM, photo 1
- `tomato_001_20251111_1445_1.jpg` - Tomato, Nov 11 2025, 2:45 PM, photo 1

**Storage:** Single flat `photos/` directory (no date subfolders)

**Format:** .jpg (JPEG) for smaller file sizes vs .png

**Metadata:** Photos can have tags (before_pruning, after_watering, etc.) and captions

### 5. HTML Templates (VERSION 13)

**Files created:**
- `templates/base.css` - Shared styles, green color scheme (#216e3a)
- `templates/daily_journal_template.html` - Jinja2 template for daily pages
- `templates/sample_daily_journal.html` - Working sample with Nov 11, 2025 real data

**Template features:**
- Time badges showing observation times (green rounded badges)
- Photo captions below images
- Soil moisture display
- Nested action lists with amounts/products
- Upcoming Actions section
- Container grouping (staked and position-based)
- Plant-specific Q&A with headers
- Shared container support (Arugula/Cilantro example included)
- **No print CSS** - removed for Print Friendly & PDF plugin use

**Sample includes:**
- Multiple basil and strawberry observations
- Tomato with 7 before/after photos showing pruning
- Shared Arugula/Cilantro container (positions)
- Raised Bed with 3 zucchini at different stakes
- Real Nov 11 activities and observations

### 6. Setup Scripts

**Created:**
- `setup_docs.py` - Generates all documentation files and project structure
- `setup_templates_V13.py` - Generates CSS and HTML templates (VERSION 13)
- `scripts/compress_photos.py` - Batch compress photos maintaining quality

---

## 📋 DESIGN DECISIONS

### Location vs Container vs Panel

- **Locations:** Physical places (Picnic Table, Panel 1, Panel 2, ... Panel 18, Indoors, Garage)
- **Panels:** Numbered positions along fence (1-18), gate between 11-12
- **Containers:** What plants live in (pots, window planters, raised bed)
- **Container names:** Friendly names for grouping (Basil Pot - Left, Pepper Box, Raised Bed)

**Example:** Basil - Left lives in "Basil Pot - Left" container, which has been at these locations:
1. Picnic Table (Oct 8)
2. Panel 14 (Oct 15)
3. Panel 1 (Oct 20 - current)

### Sun Exposure Pattern

- Panels 1-3: Full sun starting 7:00 AM
- Panels 4-15: Full sun by 10:00-10:45 AM
- Panels 16-18: Full sun by 11:00 AM
- All panels: Shade begins ~3:50 PM

### Container Types

**Individual containers:** Each plant has its own pot
- Basil Pot - Left, Basil Pot - Right
- Strawberry Pot - Left, Strawberry Pot - Right

**Shared containers with stakes:**
- Pepper Box (Panel 7): 3 stakes for 3 pepper plants
- Raised Bed (Panels 16-18): 4 stakes for tomato + zucchinis

**Shared containers with positions:**
- Garlic & Scallion Box (Panel 8): Garlic varieties in sections, scallions at edges
- Arugula & Cilantro Box (Panel 11): Arugula left side, cilantro right side
- Broccoli & Chives Box (Panel 13): Broccoli center, chives at edges
- 5-Herb Box (Panel 12): 5 herbs in different sections

### Daily Journal Structure

**Sections (in order):**
1. Summary of Activities (what you did)
2. Weather / Sun Conditions (temp, conditions, sunrise/sunset)
3. General Observations (garden-wide notes)
4. Questions & Answers (general garden topics)
5. Upcoming Actions (planned future tasks)
6. Plant by Plant (individual plant observations with photos)

**All sections always display** with empty state message if no data ("No activities recorded for this date")

### Styling Guidelines

- **Colors:** Green #216e3a, muted #5f6b6b, rule/borders #e6e8eb
- **Fonts:** System fonts (Apple, Segoe UI, Roboto, etc.)
- **Headers:**
  - h1 (Daily Journal): 28px
  - h2.major-section (Plant by Plant): 24px
  - h2 (other sections): 18px
  - h3 (Raised Bed, container headers): 18px
  - Stake titles: 16px
- **Photos:** 2.0in × 1.5in, 0.15in gap, max 4 per observation, indented 20px
- **Q&A blocks:** Indented 20px with left border
- **Time badges:** Green rounded badges showing observation time
- **No print CSS:** User will use Print Friendly & PDF browser plugin

---

## 🌱 MY CURRENT GARDEN (as of Nov 11, 2025)

### Plants Being Tracked:

**Basil (2):**
- basil_001 "Basil - Left" - Panel 1 (moved from Picnic Table → Panel 14 → Panel 1)
- basil_002 "Basil - Right" - Panel 2

**Strawberries (2):**
- strawberry_001 "Strawberry - Left" - Panel 3 (recently transplanted)
- strawberry_002 "Strawberry - Right" - Panel 4 (has fungal leaf spot, treated Nov 11)

**Lavender (2):**
- lavender_001 "Lavender - Left" - Panel 5 (seeds planted Nov 9, not germinated)
- lavender_002 "Lavender - Right" - Panel 6 (seeds planted Nov 9)

**Peppers (3) - Panel 7 Pepper Box (not planted yet):**
- pepper_001 "Scotch Bonnet" - Stake 1
- pepper_002 "Orange Cali Wonder" - Stake 2
- pepper_003 "Jalapeño" - Stake 3

**Garlic & Scallions - Panel 8 Garlic Box:**
- garlic_001 "Siberian Hardneck" - Left section
- garlic_002 "Music Hardneck" - Center section
- garlic_003 "Chesnok Red" - Right section
- scallions_001 "Scallions" - Edges (not planted yet)

**Shallots & Chamomile - Panel 10:**
- shallots_001 "Shallots" - Planted Nov 9
- chamomile_001 "Chamomile" - Not planted yet

**Arugula & Cilantro - Panel 11 shared box:**
- arugula_001 "Arugula" - Left side (reseeded Nov 5, recovering well)
- cilantro_001 "Cilantro" - Right side

**5-Herb Box - Panel 12:**
- thai_basil_001, cilantro_002, parsley_001, thyme_001, oregano_001

**Broccoli & Chives - Panel 13:**
- broccoli_001 "Broccoli" - Center section (pale but healthy)
- chives_001 "Chives" - Edges (failed germination, needs reseeding)

**Raised Bed - Panels 16-18 (4 stakes):**
- tomato_001 "Cherry Tomato" - Stake 1 (FRUITING! First fruits Nov 11)
- zucchini_001 "Zucchini + Green Beans" - Stake 2 (direct-sown, green beans sown recently)
- zucchini_002 "Zucchini" - Stake 3 (direct-sown, largest, got neem Nov 11)
- zucchini_003 "Zucchini" - Stake 4 (transplanted, recovering)

### Key Events Nov 11, 2025:

- **Cold night** (<40°F): Brought basil and strawberries indoors for protection
- **Tomato milestone:** First fruits forming! Pruned all diseased lower branches, added mulch
- **Strawberry Right:** Fungal leaf spot - removed worst leaves, added topsoil, neem planned for Nov 12
- **Zucchini Stake 3:** First neem oil treatment for chew marks (beetles/caterpillars)
- **Lavender:** Day 2 since seeding, first watering (2 tbsp each pot)
- **Garlic:** Deep watered with hose (16 oz) after dry cold night
- **Multiple plants:** Watered after dry overnight period

---

## 🚧 WHAT NEEDS TO BE DONE NEXT

### IMMEDIATE PRIORITIES:

### 1. Create Remaining HTML Templates

Need to create templates matching the approved HTML examples:

**a) Front Page Template** (`templates/front_page_template.html`)
- Reference: `html_examples/Garden_00_Front Page.html` (approved design)
- Title: "🪴 Jodi's Garden Journal"
- Subtitle: "Beginning October 2025"
- Description and sections list

**b) Section 1 - Layout Template** (`templates/layout_template.html`)
- Table format with leaf emoji (🍃)
- Columns: Panel, Plant, Container, Soil Mix, Notes
- Italic note: "Fence panels are numbered 1 → 18 (gate between 11 & 12). Raised bed spans Panels 16–18."
- Lists all current plant locations

**c) Section 2 - Plant Summary Template** (`templates/plant_summary_template.html`)
- Reference: `html_examples/Garden_02_Plant_by_Plant_Summary.html` (user manually fixed, approved)
- Ordered by panel 1-18, then stakes 1-4
- Each plant separate with container, soil, notes, growth expectations
- Divider lines between panels
- Text-only (no photos) - static reference document

**d) Section 3 Cover Page Template** (`templates/section3_cover_template.html`)
- Static title page explaining daily journal structure
- Describes the 6 sections and photo format

### 2. Build HTML Generator (`src/html_generator.py`)

**Must implement:**
- Read `garden_data.json`
- Use Jinja2 to render all templates
- **Container grouping logic:** Implement `group_plants_by_container()` function from `schema.py`
  - Group by location + container_name
  - Detect stakes vs positions
  - Sort appropriately for display
- Generate output files with proper naming:
  - `Garden_00_Front_Page.html`
  - `Garden_01_Layout.html`
  - `Garden_02_Plant_by_Plant_Summary.html`
  - `Garden_03_Daily_YYYYMMDD.html` (one per date)
- Copy `base.css` to `output/styles.css`
- Handle photo paths (../photos/filename.jpg)
- Format dates and times for display

### 3. Build Data Manager (`src/data_manager.py`)

**Functions needed:**
- `load_data()` - Read garden_data.json with validation
- `save_data()` - Write garden_data.json with backup
- `add_plant()` - Add new plant with initial location
- `move_plant()` - Add location history entry, update current_location
- `add_daily_entry()` - Add complete daily entry
- `add_plant_observation()` - Add observation to existing daily entry
- `get_plant_by_id()` - Retrieve plant data
- `get_entry_by_date()` - Retrieve daily entry
- Validation using schema.py functions

### 4. Build Interactive Scripts

**a) `scripts/add_plant.py`**
- Interactive CLI to add new plants
- Prompts for: plant type, common name, variety, purchase date, location, container details, stake/position
- Auto-generates plant_id
- Validates all inputs
- Updates garden_data.json

**b) `scripts/move_plant.py`**
- Select plant from list
- Enter new location, reason for move
- Updates location_history and current_location

**c) `scripts/add_entry.py`**
- Interactive form for daily entries
- Sections: date/time, weather, activities, observations, general Q&A, upcoming actions
- Then loop: add plant observations (select plant, enter details, specify photos)
- Support multiple observations per plant (morning, afternoon checks)

**d) `scripts/generate_all.py`**
- Generate all HTML pages
- Options: --static-only, --daily-only, --date YYYYMMDD
- Progress indicators
- Validation before generating

**e) `scripts/rename_photos.py`**
- Batch rename photos to proper convention
- Prompts for plant_id, date, time
- Automatically numbers sequence
- Moves to photos/ folder

### 5. Import Historical Data

**Source:** `html_examples/Garden_Log_Oct8–Nov9.html` (ChatGPT generated, has errors)

**Tasks:**
- Parse HTML table data
- Validate dates and plant names
- Create plant records for all plants
- Build location history from movement notes
- Create daily entries for Oct 8 - Nov 9
- **Important:** ChatGPT makes mistakes with times/dates - verify everything
- Match to actual photos from chatGPT_conversations/ PDFs

### 6. Create Initial garden_data.json

- Start with structure from garden_data.example.json
- Add all real plants with accurate data
- Import validated historical entries
- Current data through Nov 11, 2025

---

## 📐 TECHNICAL SPECIFICATIONS

### Date/Time Formats

- **Dates:** YYYYMMDD (e.g., "20251111")
- **Times:** HHMM in 24-hour military time (e.g., "1400" for 2:00 PM)
- **Display:** Functions in schema.py convert to readable format

### Plant ID Format

- **Pattern:** `{planttype}_{###}` with 3-digit numbers
- **Examples:** basil_001, tomato_001, strawberry_002
- **Validation:** `validate_plant_id()` in schema.py

### Photo Filename Format

- **Pattern:** `{plant_id}_{YYYYMMDD}_{HHMM}_{seq}.jpg`
- **Example:** basil_001_20251111_1400_1.jpg
- **Validation:** `validate_photo_filename()` in schema.py

### Container Grouping Rules

**When generating HTML Plant by Plant section:**

1. Group plant observations by: `location + container_name`
2. **If multiple plants with same container_name AND have stakes:**
   - Display container header once (e.g., "Raised Bed — Panels 16–18")
   - List plants by stake number underneath
   - Indent stakes 20px
3. **If multiple plants with same container_name but NO stakes:**
   - Display container header once (e.g., "Panel 11 — Arugula & Cilantro Box")
   - List each plant with position shown
   - Indent plants 20px
4. **If single plant in container:**
   - Display: "Panel X — Container Name"
   - No grouping header needed

### Action Types (Validation)

Valid values: `watering`, `pruning`, `treatment`, `feeding`, `mulching`, `transplanting`, `seeding`, `thinning`, `staking`, `covering`, `observation`, `moving`, `soil_amendment`, `pest_control`

### Plant Status Values

Valid values: `active`, `removed`, `died`, `harvested`

---

## 🎨 APPROVED DESIGN

### Color Scheme

- Primary green: `#216e3a`
- Muted text: `#5f6b6b`
- Borders/rules: `#e6e8eb`
- Background: `#fff`
- Text: `#111`

### Typography

- **Fonts:** -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji"
- **H1 (Daily Journal):** 28px
- **H2.major-section (Plant by Plant):** 24px - larger than other sections
- **H2 (Summary, Weather, etc.):** 18px
- **H3 (Raised Bed, container headers):** 18px, bold
- **Panel titles:** 18px, bold
- **Stake titles:** 16px, bold

### Photo Display

- **Size:** 2.0in width × 1.5in height
- **Gap:** 0.15in between photos
- **Max per observation:** 4 photos
- **Indent:** 20px (aligns with bullet text)
- **Border:** 1px solid #e6e8eb, 10px border-radius
- **Captions:** 12px gray italic text below photo, centered, max-width 2.0in
- **Container:** Flexbox column for photo + caption

### Layout Details

- **Max width:** 880px
- **Margins:** 32px auto 60px, 20px side padding
- **Dividers:** 1px solid #e6e8eb, 22px top/bottom margin
- **Q&A indent:** 20px margin-left, 16px padding-left, 3px left border
- **Stakes indent:** 16px top/bottom, 20px left, 16px padding-bottom
- **Time badges:** Green background (#f0fdf4), green border (#bbf7d0), green text (#166534)

---

## 📦 DEPENDENCIES

### Python Packages Needed:

```
Jinja2>=3.1.0        # Template engine
Pillow>=10.0.0       # Image processing for compression script
```

Create `requirements.txt`:
```
Jinja2>=3.1.0
Pillow>=10.0.0
```

---

## 🔄 WORKFLOW (Future State)

### Daily Usage:

1. Take photos throughout the day
2. Transfer photos to computer, rename with script or manually
3. Run `python3 scripts/add_entry.py` - add daily observations
4. Run `python3 scripts/generate_all.py --daily-only --date 20251111`
5. Open `output/Garden_03_Daily_20251111.html` in browser
6. Use Print Friendly & PDF to save as PDF with custom page breaks

### Adding New Plant:

1. Run `python3 scripts/add_plant.py`
2. Follow prompts
3. Regenerate static pages: `python3 scripts/generate_all.py --static-only`

### Moving Plant:

1. Run `python3 scripts/move_plant.py`
2. Select plant, enter new location
3. Updates location_history automatically

---

## 🐛 KNOWN ISSUES / NOTES

1. **ChatGPT data has errors:** The Garden_Log_Oct8–Nov9.html file has some incorrect timestamps and data. Need to manually validate against actual photos and PDF conversations.

2. **Photo size:** Original photos too large for git (excluded in .gitignore). Need compression script before committing photos.

3. **Print CSS removed:** User prefers Print Friendly & PDF browser plugin for page break control instead of embedded CSS.

4. **Version tracking:** Always update VERSION number in file headers when making changes. Check line 3-4 of Python files for version number.

---

## 📱 TOOLS & BROWSER EXTENSIONS

### Recommended (User's Choices):

- **Print Friendly & PDF** - Chrome extension for PDF creation with custom page breaks
- **ImageOptim** (Mac) or **Squoosh** (web) - Free photo compression maintaining quality
- **Compression script** - Python script created at `scripts/compress_photos.py`

---

## 🎯 IMMEDIATE NEXT ACTIONS

**Priority 1: HTML Generator**
Build `src/html_generator.py` so we can generate actual journal pages from data. This is the critical path to having a working system.

**Priority 2: Remaining Templates**
Create Front Page, Layout (Section 1), Plant Summary (Section 2), and Section 3 Cover templates.

**Priority 3: Data Manager**
Build `src/data_manager.py` for JSON read/write operations.

**Priority 4: Scripts**
Create add_entry.py, add_plant.py, generate_all.py for daily usage.

**Priority 5: Import Data**
Validate and import historical data from ChatGPT conversations (Oct 8 - Nov 9).

---

## 💡 CONTEXT FOR AI ASSISTANT

- User is Jodi, tracking a container garden in Miami, Florida
- Started garden Oct 8, 2025
- Currently has 18 fence panels numbered 1-18 with gate between 11-12
- Takes multiple photos daily, wants detailed tracking
- Previously used ChatGPT but it couldn't maintain accurate dates/times
- Values: accuracy, completeness, beautiful printable output
- Prefers: clean design, no excessive formatting, functional over flashy
- Technical level: Comfortable with Python, command line, GitHub
- Always use `python3` commands (not `python`)

---

**Continue from here. Ready to build the HTML generator to start creating actual journal pages.**