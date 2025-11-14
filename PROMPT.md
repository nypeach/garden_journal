# Garden Journal Project - Current Status

**Last Updated:** November 13, 2025 @ 9:58 PM EST
**Current Version:** 13.1
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
├── LICENSE
├── .gitignore
├── PROMPT.md
├── .claude/
├── chatGPT_conversations/ (PDFs of chat history)
├── data/
│   ├── garden_data.json            # Your actual garden data
│   ├── garden_data.example.json
│   ├── backups/                    # Timestamped backups (gitignored)
│   └── data.py (untracked - work in progress)
├── docs/
│   ├── data-structure.md
│   ├── photo-naming.md
│   └── webform.md                  # Web forms requirements (VERSION 1.0)
├── html_examples/ (reference files from ChatGPT)
├── output/ (gitignored - generated HTML files)
├── photos/ (gitignored - photo files)
├── scripts/
│   ├── compress_photos.py
│   └── test_data_manager.py       # Test suite for data_manager
├── src/
│   ├── __init__.py
│   ├── __pycache__/ (gitignored)
│   ├── data_manager.py            # JSON read/write operations
│   ├── html_generator.py
│   ├── schema.py
│   └── web_server.py              # Flask backend (VERSION 1.0)
├── forms/
│   ├── index.html                 # Landing page
│   ├── add_plant.html             # Add plant form
│   ├── move_plant.html            # Move plant form
│   └── static/
│       ├── base.css               # Shared CSS (moved from templates/)
│       └── forms.css              # Form-specific CSS
├── templates/
│   ├── daily_journal_template.html
│   ├── front_page_template.html
│   ├── layout_template.html
│   ├── plant_summary_template.html
│   └── samples/ (gitignored - sample files)
│       ├── sample_daily_journal.html
│       └── sample-*.jpg (sample photos)
├── setup_docs.py
├── setup_templates_20251112_347.py (old version)
└── setup_templates.py
```

### 2. Documentation (VERSION 13.1)

**Files created:**
- `README.md` - Project overview, quick start guide, features
- `docs/data-structure.md` - Complete JSON schema with all V13.1 enhancements
- `docs/photo-naming.md` - Photo naming conventions and best practices
- `docs/webform.md` - Complete web forms requirements (VERSION 1.0) **NEW!**
- `src/schema.py` - Python validation functions and dataclasses (V13.1)
- `data/garden_data.example.json` - Working example with V13 structure
- `PROMPT.md` - This file - handoff documentation

### 3. Data Schema (VERSION 13.1)

**Core design:**
- **Plants are primary entities** with unique IDs (basil_001, tomato_001, etc.)
- **Locations are separate from containers** - plants can move (Picnic Table → Panel 14 → Panel 1)
- **Complete location history** - Track every move with dates and reasons
- **Shared containers supported:**
  - **With stakes:** Pepper Box (3 peppers at stakes 1-3), Raised Bed (4 stakes)
  - **With positions:** Garlic Box (garlic in sections, scallions at edges), Arugula/Cilantro Box

**VERSION 13.1 NEW FEATURE:**
- **Plant summary field** - Evolving assessment of each plant that displays in Section 2. Can be kept, updated, or appended when adding daily observations.

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

**Photo Workflow (for web forms):**
1. Take photos with iPhone → sync to iCloud Photos
2. In Photos app on MacBook: drag photos from "Garden" album to Google Drive folder
3. Photos auto-convert from HEIC to JPEG when dragged out
4. In web form: browse Google Drive folder, select photos
5. Form compresses (600×450px), renames, and copies to `photos/` folder
6. Originals remain in Google Drive folder

**Google Drive Storage Path:** `/Users/jodisilverman/Library/CloudStorage/GoogleDrive-jodimsilverman@gmail.com/My Drive/GardenPhotos/`

### 5. HTML Templates (VERSION 13.1)

**Files created:**
- `templates/daily_journal_template.html` - Jinja2 template for daily pages
- `templates/front_page_template.html` - Front page with dynamic dates
- `templates/layout_template.html` - Current garden layout table
- `templates/plant_summary_template.html` - Plant summaries with summary field and Inactive Plants section
- `templates/samples/sample_daily_journal.html` - Working sample with Nov 11, 2025 real data

**Template features:**
- Time badges showing observation times (green rounded badges)
- Photo captions below images
- Soil moisture display
- Nested action lists with amounts/products
- Upcoming Actions section
- Container grouping (staked and position-based)
- Plant-specific Q&A with headers
- Shared container support (Arugula/Cilantro example included)
- Plant summary field display in Section 2
- Inactive Plants section at bottom of Section 2 (for died/harvested/removed plants)
- Dynamic date ranges on front page
- **No print CSS** - removed for Print Friendly & PDF plugin use
- **Title formatting:** All templates use colons (`:`) not em-dashes in titles/headings

**Sample includes:**
- Multiple basil and strawberry observations
- Tomato with 7 before/after photos showing pruning
- Shared Arugula/Cilantro container (positions)
- Raised Bed with 3 zucchini at different stakes
- Real Nov 11 activities and observations
- Photos moved to templates/samples/ folder

### 6. HTML Generator (VERSION 13)

**Created:** `src/html_generator.py`

**Features implemented:**
- Reads `garden_data.json` using Python's json module
- Uses Jinja2 to render all templates
- Container grouping logic for plant observations
- Generates all static pages (Front, Layout, Plant Summary)
- Generates daily journal pages from daily_entries
- Copies `base.css` from `forms/static/base.css` to `output/styles.css`
- Handles photo paths correctly (`../photos/filename.jpg`)
- Formats dates and times for display using schema.py functions
- Calculates `last_entry_date` from daily_entries automatically
- Command-line options: `--static-only`, `--daily-only`, `--date YYYYMMDD`

**Successfully tested and generates:**
- `Garden_00_Front_Page.html` ✅
- `Garden_01_Layout.html` ✅
- `Garden_02_Plant_by_Plant_Summary.html` ✅
- `Garden_03_Daily_YYYYMMDD.html` (ready to test with real data)

### 7. Data Manager (VERSION 1.0) ✅ COMPLETED

**Created:** `src/data_manager.py`

**Functions implemented:**
- `load_data()` / `save_data()` with timestamped backups to `data/backups/`
- `add_plant()` - Add new plant with initial location
- `update_plant_summary()` - Update plant summary field
- `move_plant()` - Add location history entry, update current_location
- `add_daily_entry()` - Add complete daily entry
- `add_plant_observation()` - Add observation to existing daily entry
- `get_plant_by_id()` / `get_entry_by_date()` / `get_all_plants()` / `get_all_entries()`

**Tested:** `scripts/test_data_manager.py` - Comprehensive test suite (7/8 tests passing)

### 8. Setup Scripts

**Created:**
- `setup_docs.py` - Generates all documentation files and project structure
- `setup_templates.py` - Generates CSS and HTML templates (VERSION 13.1)
- `scripts/compress_photos.py` - Batch compress photos maintaining quality
- `scripts/test_data_manager.py` - Test suite for data_manager.py

### 9. Web Forms & Flask Backend ⬅️ IN PROGRESS!

**Status:** 3 of 4 forms complete and tested - Ready for Daily Entry form

**Completed Files:**
- ✅ `src/web_server.py` - Flask backend (VERSION 1.0) - TESTED
- ✅ `forms/static/base.css` - Shared CSS - moved from templates/
- ✅ `forms/static/forms.css` - Form-specific styles
- ✅ `forms/index.html` - Landing page - TESTED
- ✅ `forms/move_plant.html` - Move plant form - TESTED
- ✅ `forms/add_plant.html` - Add plant form - TESTED

**Flask Backend Details (src/web_server.py):**
- Runs on `localhost:3000` (port 5000 blocked on macOS)
- Serves forms from `forms/` folder using Jinja2 templates
- Serves static files from `forms/static/`
- Serves generated HTML from `output/` folder
- Auto-regenerates static pages after Add Plant and Move Plant submissions

**Routes:**
- `GET /` - Landing page ✅
- `GET /add-plant` - Add plant form ✅
- `GET /add-entry` - Daily entry form (not yet built)
- `GET /move-plant` - Move plant form ✅
- `GET /output/<filename>` - Serve generated pages ✅
- `GET /api/plants` - Get all active plants ✅
- `GET /api/plant/<id>` - Get single plant ✅
- `POST /api/add-plant` - Add plant ✅ TESTED
- `POST /api/move-plant` - Move plant ✅ TESTED

**Landing Page (forms/index.html) - ✅ TESTED:**
- Server start/stop instructions
- Quick stats (total active plants, last entry date)
- Navigation cards to all forms
- Links to generated journal pages
- Matches base.css styling

**Move Plant Form (forms/move_plant.html) - ✅ TESTED:**
- Dropdown with all active plants
- Fields: new location, container type/name, stake, position, reason, date
- Auto-regenerates static pages after move
- Success modal with old → new location
- Working perfectly

**Add Plant Form (forms/add_plant.html) - ✅ TESTED:**
- 3 sections: Plant Info, Location & Container, Soil & Care
- Auto-generates unique plant_id (basil_001, basil_002, etc.)
- All fields: type, name, variety, purchased/sowed date, source, location, container details, stake, position, soil mix, initial summary
- Auto-regenerates static pages after adding
- Success modal shows plant details
- Buttons: View Plant Summary, Add Another Plant, OK
- Working perfectly

**CSS Architecture:**
- `forms/static/base.css` - Shared by forms AND generated HTML
- `forms/static/forms.css` - Form-specific additions only
- `html_generator.py` updated to copy from new location

**Forms Completed: 3 of 4**
1. ✅ Landing Page (index.html) - TESTED
2. ✅ Move Plant (move_plant.html) - TESTED
3. ✅ Add Plant (add_plant.html) - TESTED
4. 🚧 Daily Entry (add_entry.html) - PHASE 1 COMPLETE, PHASE 2 NEXT
   - ✅ Phase 1: Sections 1-5 complete and tested (Activities, Weather, Observations, Q&A, Upcoming Actions)
   - ⬅️ Phase 2: Section 6 Plant by Plant (next session)
   - Phase 3: Photo handling (after Phase 2)

**Daily Entry Form Requirements (Form 4):**
The comprehensive daily journal form with 6 sections:
- **Section 1:** Summary of Activities (markdown bullets)
- **Section 2:** Weather/Sun Conditions (temp high/low, conditions, sunrise/sunset, humidity, wind, notes)
- **Section 3:** General Observations (markdown bullets)
- **Section 4:** Questions & Answers - General (multiple Q&A pairs, repeatable)
- **Section 5:** Upcoming Actions (multiple items with optional target dates/timeframes)
- **Section 6:** Plant by Plant Observations (repeatable):
  - Select plant → auto-loads current summary for inline editing
  - Plant status dropdown (active/died/harvested/removed) - defaults to current status
  - If status changed from active: show "Reason for Status Change" field
  - Status change date = daily entry date
  - Container/soil info auto-filled from plant data, editable
  - Soil conditions: moisture, pH, fertility (all free text inputs)
  - Growth: current stage, next stage
  - Observations (textarea), Actions Taken (markdown bullets), Notes (textarea)
  - Plant-specific Q&A (multiple pairs, repeatable)
  - Photos: browse Google Drive → select multiple → extract EXIF → compress to 600×450px @ 85-90% → auto-suggest filename → add caption/tags → copy to `photos/` folder
  - No limit on photos per observation

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

### Plant Summary Field

**NEW IN VERSION 13.1**

Each plant now has a `summary` field containing an evolving assessment:
- Appears in Section 2 (Plant-by-Plant Summary) as "Notes"
- Updated manually when adding daily observations
- Can be kept unchanged, replaced, or appended to
- Contains high-level health status, care patterns, temperature thresholds
- Example: "Healthy, compact growth; recovered after pruning; ongoing harvest cycle. Cover or bring indoors ≤49°F."

### Plant Status Tracking

**NEW FOR WEB FORMS**

Each plant has a `status` field (active/died/harvested/removed). When status changes in Daily Entry form:
- New fields populated: `status_date` (YYYYMMDD), `status_reason` (text)
- Status date = the daily entry date where change occurred
- Inactive plants display in separate section at bottom of Plant Summary
- Format: "Lavender - Left (Died November 5, 2025: Water rot)"

### Sun Exposure Pattern

- Panels 1-3: Full sun starting 7:00 AM
- Panels 4-15: Full sun by 10:00-10:45 AM
- Panels 16-18: Full sun by 11:00 AM
- All panels: Shade begins ~3:50 PM

### Container Types

**Individual containers:** Each plant has its own pot
- Basil Pot - Left, Basil Pot - Right
- Strawberry Pot - Left, Strawberry Pot - Right
- Lavender Pot - Left, Lavender Pot - Right

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
  - Panel titles: 18px, bold
  - Stake titles: 16px, bold
- **Photos:** 2.0in × 1.5in, 0.15in gap, no limit per observation, indented 20px, 20px margin-top
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

### 1. ~~Create Remaining HTML Templates~~ ✅ COMPLETED

All templates created and tested.

### 2. ~~Build HTML Generator~~ ✅ COMPLETED

Successfully generates all 4 HTML page types.

### 3. ~~Build Data Manager~~ ✅ COMPLETED

All functions implemented and tested.

### 4. Build Web Forms ⬅️ IN PROGRESS!

**Status:** 3 of 4 forms complete - Daily Entry form is next

**Forms Completed:**
1. ✅ **Landing Page** (forms/index.html) - Navigation, stats, server instructions - TESTED
2. ✅ **Move Plant** (forms/move_plant.html) - Full functionality, auto-regenerates pages - TESTED
3. ✅ **Add Plant** (forms/add_plant.html) - Full functionality, auto-generates plant_id - TESTED
4. ⬅️ **Daily Entry** (forms/add_entry.html) - NEXT - The big form with all 6 sections

**Next: Build Daily Entry Form**

This is the most complex form with 6 sections:
- Basic info: date, time of entry
- Section 1: Summary of Activities (markdown bullets)
- Section 2: Weather/Sun Conditions (temp, conditions, sun times, humidity, wind, notes)
- Section 3: General Observations (markdown bullets)
- Section 4: Questions & Answers (general, multiple Q&A pairs)
- Section 5: Upcoming Actions (multiple items with target dates/timeframes)
- Section 6: Plant by Plant Observations (repeatable):
  - Select plant dropdown
  - Time of observation
  - Current plant summary (auto-loaded, editable textarea)
  - Plant status dropdown (active/died/harvested/removed)
  - Status change reason field (appears if status changed)
  - Container/soil auto-filled, editable
  - Soil readings: moisture, pH, fertility (free text)
  - Growth stages: current, next
  - Observations, actions (markdown), notes
  - Plant Q&A (multiple pairs)
  - Photo browser: select from Google Drive → compress → rename → copy to repo

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
- Add plant summaries for each plant
- Import validated historical entries
- Current data through Nov 11, 2025

---

## 📝 TECHNICAL SPECIFICATIONS

### Date/Time Formats

- **Dates:** YYYYMMDD (e.g., "20251111")
- **Times:** HHMM in 24-hour military time (e.g., "1400" for 2:00 PM)
- **Display:** Functions in schema.py convert to readable format
- **Date pickers in forms:** Use local timezone to ensure correct EST dates

### Plant ID Format

- **Pattern:** `{planttype}_{###}` with 3-digit numbers
- **Examples:** basil_001, tomato_001, strawberry_002
- **Auto-generated:** Forms use `schema.generate_plant_id()` function
- **Validation:** `validate_plant_id()` in schema.py

### Photo Filename Format

- **Pattern:** `{plant_id}_{YYYYMMDD}_{HHMM}_{seq}.jpg`
- **Example:** basil_001_20251111_1400_1.jpg
- **Auto-suggested:** Forms extract EXIF date/time and suggest filenames
- **Validation:** `validate_photo_filename()` in schema.py

### Container Grouping Rules

**When generating HTML Plant by Plant section:**

1. Group plant observations by: `location + container_name`
2. **If multiple plants with same container_name AND have stakes:**
   - Display container header once (e.g., "Raised Bed: Panels 16–18")
   - List plants by stake number underneath
   - Indent stakes 20px
3. **If multiple plants with same container_name but NO stakes:**
   - Display container header once (e.g., "Panel 11: Arugula & Cilantro Box")
   - List each plant with position shown
   - Indent plants 20px
4. **If single plant in container:**
   - Display: "Panel X: Container Name"
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
- **H2.major-section (Plant by Plant):** 24px
- **H2 (other sections):** 18px
- **H3 (Raised Bed, container headers):** 18px, bold
- **Panel titles:** 18px, bold
- **Stake titles:** 16px, bold

### Photo Display

- **Size:** 2.0in width × 1.5in height
- **Gap:** 0.15in between photos
- **No limit** on photos per observation
- **Indent:** 20px (aligns with bullet text)
- **Margin-top:** 20px (spacing above photo row)
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
Flask>=3.0.0         # Web framework for forms
```

Create `requirements.txt`:
```
Jinja2>=3.1.0
Pillow>=10.0.0
Flask>=3.0.0
```

---

## 📄 WORKFLOW (Current State with Web Forms)

### Daily Usage:

1. Take photos throughout the day with iPhone
2. Photos sync to iCloud Photos automatically
3. Open Photos app on MacBook, drag photos from "Garden" album to Google Drive folder
4. Start Flask server: `python3 src/web_server.py`
5. Open Chrome: `http://localhost:3000`
6. Click "📔 Daily Entry" to fill out daily journal form
7. Form sections: Activities, Weather, Observations, Q&A, Upcoming Actions, Plant by Plant
8. For each plant: select photos from Google Drive, form compresses/renames/copies to repo
9. Submit form - auto-saves to garden_data.json and generates HTML pages
10. Click "View Journal" to see generated daily page
11. Use Print Friendly & PDF Chrome extension to save as PDF

### Adding New Plant:

1. Open web application: `http://localhost:3000`
2. Click "➕ Add Plant" form
3. Fill in all fields (type, name, location, container, soil, initial summary)
4. Submit - auto-generates unique plant_id, updates garden_data.json
5. Pages auto-regenerate - plant immediately visible in Plant Summary

### Moving Plant:

1. Open "🔄 Move Plant" form
2. Select plant from dropdown
3. Enter new location, container details, reason
4. Submit - updates location_history and current_location
5. Pages auto-regenerate - plant shows at new location immediately

### Updating Plant Summary:

When filling out daily entry form:
- After selecting plant, current summary auto-loads in editable textarea
- Edit as needed (keep, update, or append)
- New summary saved to plant record on submit

### Changing Plant Status:

When filling out daily entry form:
- Plant status dropdown defaults to current status (active/died/harvested/removed)
- If changing from active to inactive: "Reason for Status Change" field appears
- Status change date = daily entry date
- Inactive plants appear in separate section at bottom of Plant Summary

---

## 🛠️ KNOWN ISSUES / NOTES

1. **ChatGPT data has errors:** The Garden_Log_Oct8–Nov9.html file has some incorrect timestamps and data. Need to manually validate against actual photos and PDF conversations.

2. **Photo compression:** Happens in Daily Entry form via JavaScript before upload - target 600×450px @ 85-90% quality.

3. **Print CSS removed:** User prefers Print Friendly & PDF browser plugin for page break control instead of embedded CSS.

4. **Version tracking:** Always update VERSION number in file headers when making changes. Check line 3-4 of Python files for version number.

5. **Sample files location:** Sample HTML and photos now in `templates/samples/` folder (gitignored)

6. **Soil tracking:** User tracks Soil Moisture, Soil pH, and Soil Fertility using JQ001-style soil meter. All three fields are free text inputs in forms.

7. **Port 3000:** Flask runs on port 3000 (port 5000 blocked on macOS).

8. **Auto-regeneration:** Add Plant and Move Plant forms automatically regenerate static HTML pages after submission so changes are immediately visible.

---

## 📱 TOOLS & BROWSER EXTENSIONS

### User's Choices:

- **Browser:** Chrome (primary)
- **Photo Export:** macOS Photos app drag-and-drop (auto-converts HEIC → JPEG)
- **Photo Storage:** Google Drive folder (100GB storage, 17GB used)
- **Print Friendly & PDF** - Chrome extension for PDF creation with custom page breaks
- **Soil Meter:** JQ001 or similar (measures Fertility/color, Moisture/numeric, pH/range)

---

## 🎯 IMMEDIATE NEXT ACTIONS

**Priority 1: ~~HTML Generator~~** ✅ COMPLETED

**Priority 2: ~~Remaining Templates~~** ✅ COMPLETED

**Priority 3: ~~Data Manager~~** ✅ COMPLETED

**Priority 4: Web Forms** ⬅️ IN PROGRESS!
- ✅ Landing Page - COMPLETE & TESTED
- ✅ Move Plant Form - COMPLETE & TESTED
- ✅ Add Plant Form - COMPLETE & TESTED
- ⬅️ Daily Entry Form - NEXT (the comprehensive form with all 6 sections)

**Priority 5: Import Data**
Validate and import historical data from ChatGPT conversations (Oct 8 - Nov 9).

**Priority 6: Create Initial garden_data.json**
Add all real plants and import historical entries.

---

## 💡 CONTEXT FOR AI ASSISTANT

- User is Jodi, tracking a container garden in Miami, Florida
- Started garden Oct 8, 2025
- Currently has 18 fence panels numbered 1-18 with gate between 11-12
- Takes multiple photos daily, wants detailed tracking
- Previously used ChatGPT but it couldn't maintain accurate dates/times
- Values: accuracy, completeness, beautiful printable output
- Prefers: clean design, no excessive formatting, functional over flashy
- **Wants a local web application** with HTML forms for data entry, not CLI scripts
- **Project uses array-based data structure** - plants stored as array/list, not dict
- **Backups are automatic** - every save operation creates timestamped backup in data/backups/
- **Photo workflow validated** - drag from Photos app → Google Drive folder → select in form → compress/rename → copy to repo
- Technical level: Comfortable with Python, command line, GitHub
- Always use `python3` commands (not `python`)
- **Commit message format:** User prefers commit messages generated in a copyable bash format like:
```
  git add -A && git commit -m "Title

  - Bullet point 1
  - Bullet point 2
  - Bullet point 3"
```
  Always provide commit messages in this exact format, ready to copy/paste into terminal.
- **IMPORTANT:** Only make changes that are explicitly requested - do not modify code, templates, or documentation beyond what is asked
- **IMPORTANT:** If you ask the user a question, WAIT for their answer before generating any code, artifacts, or making changes. Do not assume an answer.
- **CRITICAL WORKFLOW:** When building features, work incrementally and WAIT for user verification at each step:
  1. Build one component at a time
  2. Let user test and verify it works correctly
  3. WAIT for user confirmation before moving to next component
  4. If user finds issues, fix them before proceeding
  5. Do NOT move ahead to next feature until current one is confirmed working
  6. User will explicitly say "let's move on" or "next" when ready
- **Title Formatting:** In HTML templates, both `<title>` tags and `<h1>` headings should use colons (`:`) not em-dashes
- **IMPORTANT:** When the user asks you to update PROMPT.md or any other file, FIRST tell them in the chat what you changed (list the specific changes), THEN provide the updated file so they can verify the changes match what you said.

---

**Continue from here. Next priority: Build Daily Entry form (forms/add_entry.html) - the comprehensive daily journal form with all 6 sections and photo handling.**

**Continue from here. Next priority: Build Daily Entry form (forms/add_entry.html) - the comprehensive daily journal form with all 6 sections and photo handling.**

**Build Plan for Daily Entry Form (build incrementally in phases):**

**Phase 1: Basic Structure + Sections 1-5**
- Form foundation with date/time inputs
- Section 1: Summary of Activities (textarea with markdown support)
- Section 2: Weather/Sun Conditions (temp high/low, conditions, sunrise/sunset, humidity, wind, notes)
- Section 3: General Observations (textarea with markdown support)
- Section 4: Questions & Answers (repeatable Q&A pairs with [+ Add Another Q&A] button)
- Section 5: Upcoming Actions (repeatable items with description, target date/timeframe, [+ Add Another Action] button)
- Test and verify Sections 1-5 work before moving to Phase 2

**Phase 2: Section 6 - Plant by Plant Observations**
- Plant selection dropdown (loads from active plants)
- Time of observation input
- Current summary auto-load and inline editing (textarea, pre-filled, editable)
- Plant status dropdown (active/died/harvested/removed, defaults to current status)
- Status change reason field (only appears if status changed from active)
- Container/soil info (auto-filled from plant data, editable)
- Soil conditions: moisture, pH, fertility (all free text inputs)
- Growth stages: current stage, next stage
- Observations (textarea), Actions Taken (textarea with markdown), Notes (textarea)
- Plant-specific Q&A (repeatable pairs within each plant observation)
- [+ Add Another Plant Observation] button for multiple plants per entry
- Test and verify plant observations work before moving to Phase 3

**Phase 3: Photo Handling in Plant Observations**
- Browse button to select photos from Google Drive folder path
- Display selected photos as thumbnails
- Extract EXIF metadata (date/time) from JPEGs
- Auto-suggest filenames: {plant_id}_{YYYYMMDD}_{HHMM}_{seq}.jpg
- Client-side compression using Canvas API (target: 600×450px @ 85-90% quality)
- Caption and tags inputs for each photo
- Copy compressed/renamed photos to repo `photos/` folder
- Leave originals in Google Drive folder
- Test complete form end-to-end with photos

**After all 3 phases complete:**
- Add POST /api/add-entry endpoint to web_server.py
- Endpoint calls data_manager.add_daily_entry()
- Auto-regenerate ALL pages (Front, Layout, Plant Summary, Daily page for that date)
- Success modal with link to view generated daily journal page
- Full end-to-end testing of complete form

---