# Garden Journal Project - Current Status

**Last Updated:** November 15, 2025 @ 7:45 AM EST
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
│   ├── add_entry.html             # Daily entry form (Phases 1-3 complete)
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
- `docs/webform.md` - Complete web forms requirements (VERSION 1.0)
- `src/schema.py` - Python validation functions and dataclasses (V13.1)
- `data/garden_data.example.json` - Working example with V13.1 structure (cleaned)
- `data/garden_data.json` - Actual garden data (cleaned, test plants removed)
- `PROMPT.md` - This file - handoff documentation

### 3. JSON Schema (VERSION 13.1)

**Features:**
- Plant-centric design with unique IDs (PLANT001, PLANT002, etc.)
- Complete location history tracking (moves between locations)
- Shared containers with stake OR position systems
- Soil mix tracking (type, brand, amendments)
- Plant status tracking (active/died/harvested/removed) with dates and reasons
- Growth stages tracking (current, next, date achieved)
- Daily entries with multiple plant observations per day
- Photo metadata (before/after tags, captions)
- Action tracking with amounts and product brands
- Questions and answers section
- Upcoming actions with target dates

**See:** `docs/data-structure.md` for complete schema details

### 4. Photo Naming Convention

**Format:** `plantID_YYYYMMDD_HHMM_sequence.jpg`

**Examples:**
- `PLANT001_20251015_0830_01.jpg` - First photo of PLANT001 on Oct 15 at 8:30 AM
- `PLANT001_20251015_0830_02.jpg` - Second photo same time
- `PLANT002_20251016_1445_01.jpg` - First photo of PLANT002 on Oct 16 at 2:45 PM

**See:** `docs/photo-naming.md` for complete details

### 5. HTML Templates (VERSION 13.1)

**Created with Jinja2:**
- `templates/front_page_template.html` - Entry point with clickable tiles
- `templates/layout_template.html` - Plant layout by location
- `templates/plant_summary_template.html` - Plant-by-plant status
- `templates/daily_journal_template.html` - Daily entries chronological

**Styling:**
- Clean green color scheme (#2d5016, #f0f4ed, #4a7c2c)
- No print CSS (using Print Friendly & PDF browser plugin)
- Responsive design
- Time badges for observations
- Photo captions and metadata display

**See:** `templates/` directory for all template files

### 6. HTML Generator (VERSION 1.0)

**Created:** `src/html_generator.py`

**Functions:**
- `generate_all_pages()` - Main function to regenerate all HTML
- `generate_front_page()` - Creates index.html with tiles
- `generate_layout_page()` - Creates layout.html sorted by location
- `generate_plant_summary()` - Creates plant_summary.html with current status
- `generate_daily_journal()` - Creates journal.html with all entries

**Features:**
- Automatic sorting and grouping
- Container grouping logic (stakes and positions)
- Photo display with captions
- Timezone-aware date formatting (EST)
- Error handling and validation

**Tested:** Successfully generates all pages

### 7. Data Manager (VERSION 1.1) ✅

**Created:** `src/data_manager.py`

**Functions implemented:**
- `load_data()` / `save_data()` with timestamped backups to `data/backups/`
- `add_plant()` - Add new plant with initial location (now includes container_size and soil_mix)
- `update_plant_summary()` - Update plant summary field
- `move_plant()` - Add location history entry, update current_location (now includes container_size and soil_mix)
- `add_daily_entry()` - Add complete daily entry
- `add_plant_observation()` - Add observation to existing daily entry
- `get_plant_by_id()` / `get_entry_by_date()` / `get_all_plants()` / `get_all_entries()`

**Tested:** `scripts/test_data_manager.py` - Comprehensive test suite

### 8. Setup Scripts

**Created:**
- `setup_docs.py` - Generates all documentation files and project structure
- `setup_templates.py` - Generates CSS and HTML templates (VERSION 13.1)
- `scripts/compress_photos.py` - Batch compress photos maintaining quality
- `scripts/test_data_manager.py` - Test suite for data_manager.py

### 9. Web Forms & Flask Backend ✅ ALL 4 FORMS COMPLETE!

**Flask Server (src/web_server.py VERSION 1.1):**
- Landing page route `/` serves forms/index.html
- API endpoints for plant data
- API endpoints for adding plants, moving plants, daily entries
- Auto-regenerates static HTML pages after each update
- New `/refresh-and-view` route for tiles (regenerates before displaying)

**Landing Page (forms/index.html) - ✅ COMPLETE:**
- Clean tile-based interface
- Four main tiles: Add Plant, Move Plant, Daily Entry, View Journal
- Clickable tiles open forms in new tabs
- "Refresh & View" buttons regenerate static pages before opening

**Add Plant Form (forms/add_plant.html) - ✅ COMPLETE & TESTED:**
- All fields: type, name, variety, purchased/sowed date, source, location, container details, stake, position, soil mix, container_size, initial summary
- Auto-regenerates static pages after adding
- Success modal shows plant details
- Buttons: View Plant Summary, Add Another Plant, OK
- Working perfectly

**Move Plant Form (forms/move_plant.html) - ✅ COMPLETE & TESTED:**
- Plant selection dropdown (loads from `/api/plants`)
- New location selection
- Container details: name, type, size, stake, position
- Soil mix tracking (type, brand, amendments)
- Reason for move field
- Auto-regenerates static pages after moving
- Success modal with confirmation
- Working perfectly

**Daily Entry Form (forms/add_entry.html) - ✅ ALL 3 PHASES COMPLETE & TESTED:**

**Phase 1 Complete - Sections 1-5:**
- ✅ Basic Information: date, time of entry (defaults to current EST date/time)
- ✅ Section 1: Summary of Activities (textarea with markdown bullets)
- ✅ Section 2: Weather/Sun Conditions (temp high/low, conditions, sunrise/sunset, humidity, wind, notes)
- ✅ Section 3: General Observations (textarea with markdown bullets)
- ✅ Section 4: Questions & Answers (repeatable Q&A pairs with [+ Add Another Q&A])
- ✅ Section 5: Upcoming Actions (repeatable with description, target date/timeframe, [+ Add Another Action])

**Phase 2 Complete - Section 6: Plant by Plant:**
- ✅ Plant selection dropdown (loads active plants from `/api/plants`)
- ✅ Time of observation input (defaults to current time)
- ✅ Plant summary textarea (auto-loads current summary when plant selected, fully editable)
- ✅ Plant status dropdown (active/died/harvested/removed) - defaults to plant's current status
- ✅ **Conditional "Reason for Status Change" field** - only appears when changing FROM active TO another status
- ✅ Container info fields auto-filled from `plant.current_location` (name, type, stake, position)
- ✅ Container size field (optional, manual entry)
- ✅ Soil conditions: moisture, pH, fertility (all free text inputs)
- ✅ Growth stages: current stage, next stage
- ✅ Observations, Actions Taken (markdown), Notes (textareas)
- ✅ Plant-specific Q&A (repeatable within each plant observation)
- ✅ [+ Add Another Plant Observation] button for multiple plants per entry
- ✅ Subtle styling (1px gray border, matches Q&A/Actions boxes)

**Phase 3 Complete - Photo Handling:**
- ✅ File input accepts multiple JPEG photos
- ✅ Validates file type (JPEG only)
- ✅ Warns if file > 10MB (suggests compression)
- ✅ Extracts EXIF date from file modification time
- ✅ Auto-generates filename: `plantID_YYYYMMDD_HHMM_seq.jpg`
- ✅ Client-side compression using Canvas API (600x450px, 90% quality)
- ✅ Photo preview with thumbnails
- ✅ Editable fields per photo: filename, caption, tags
- ✅ Shows before/after file sizes
- ✅ Upload functionality integrated

**Backend API (src/web_server.py):**
- ✅ POST `/api/add-plant` - Creates new plant, saves to JSON, regenerates pages
- ✅ POST `/api/move-plant` - Moves plant, updates location history, regenerates pages
- ✅ POST `/api/add-entry` - Built and tested with photo handling
- ✅ GET `/api/plants` - Returns all plants for dropdowns
- ✅ GET `/api/plants/active` - Returns only active plants
- ✅ GET `/refresh-and-view` - Regenerates pages before displaying

---

## 🚀 CURRENT STATUS

**Priority 5: Bug Fixes & Remaining Issues** ⬅️ **IN PROGRESS!**

### Task List:

**🚨 Issue 0: Template Syntax Error (BLOCKER)**
- Template: `plant_summary_template.html` line 36
- Problem: Stray `{% endif %}` tag inside `<ul>` doesn't match any opening `{% if %}`
- Impact: Blocks template rendering and testing
- Status: Identified, needs fix

**✅ ~~Issue 1: Tile buttons regenerate pages~~ - COMPLETE**
- Added `/refresh-and-view` route
- All tiles now regenerate before displaying

**✅ ~~Issue 2: Container_size saving~~ - COMPLETE**
- Updated `data_manager.add_plant()` to accept and save `container_size`
- Updated `data_manager.move_plant()` to accept and save `container_size` and `soil_mix`
- Fixed parameter order in `move_plant` (required before optional)
- Added fields to Move Plant form
- Updated API endpoints

**✅ ~~Issue 3: Container display format~~ - COMPLETE**
- Plant Summary template shows: "Container: type, size"
- Format: "Container: Round Pot (clear), 19.3 fl oz / 570 mL"
- Implemented in both stake and regular plant sections

**🆕 Issue 4: Fixed header on static pages**
- Header fixed at top (scrollable content below)
- Contains "🌿 Back to Home" link
- Link closes current tab and returns to Garden Journal tab

**🆕 Issue 5: Container name handling from daily entries**
- Need to handle `container_name` changes when entered in daily observations
- Update plant's `current_location.container_name` if different

**🆕 Issue 6: Journal routes and navigation**
- Create `/journal/current` link (all entries in chapter format)
- Create `/journal/current_2025` route linking to `/journal.html`

**🆕 Issue 7: Status change handling**
- When plant status changes in daily entry:
  - Generate status changes section in journal
  - Update plant summary appropriately
  - Track status_date and status_reason

---

## 🐛 KNOWN ISSUES

### Template Syntax Error (BLOCKER)
**File:** `templates/plant_summary_template.html`
**Line:** 36
**Problem:** Stray `{% endif %}` tag that doesn't match any opening `{% if %}`
```html
<li><strong>Notes:</strong> {{ plant.summary }}</li>
{% endif %}  <!-- ⬅️ THIS IS THE ERROR -->
</ul>
```
**Impact:** Prevents template from rendering
**Fix needed:** Remove or relocate this `{% endif %}` tag

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
7. When there are multiple tasks/issues to work through, create a visible task list and keep it updated throughout the conversation:
   - Use ✅ and ~~strikethrough~~ for completed items
   - Use ⬅️ arrow for current work in progress
   - Use 🆕 for newly identified items
   - Include brief details under each item as needed
   - Update the list after each task completion
   - This helps maintain context and prevents losing track of progress

   Example format:
```
   Task List:
   ✅ ~~Issue 1: Description~~ - COMPLETE
   ✅ ~~Issue 2: Description~~ - COMPLETE
   ⬅️ Issue 3: Description - Working on this now
   🆕 Issue 4: Description
   * Sub-detail 1
   * Sub-detail 2
```
- **Title Formatting:** In HTML templates, both `<title>` tags and `<h1>` headings should use colons (`:`) not em-dashes
- **IMPORTANT:** When the user asks you to update PROMPT.md or any other file, FIRST tell them in the chat what you changed (list the specific changes), THEN provide the updated file so they can verify the changes match what you said.

---

## 📋 NEXT PRIORITIES

1. **Fix template syntax error** in `plant_summary_template.html`
2. **Test Daily Entry form end-to-end** with photos
3. **Verify all data flows properly** through API endpoints
4. **Complete remaining issues** (4-7 from Task List)
5. **Import historical data** from ChatGPT conversations (Oct 8 - Nov 9)
6. **Create initial garden_data.json** with all real plants

---

## 🔄 Continue from here

**Where we are:** All 3 phases of Daily Entry form complete (basic fields, plant observations, photo handling). Data manager updated with container_size and soil_mix parameters. Template syntax error discovered blocking Plant Summary display.

**Next step:** Fix template syntax error in `plant_summary_template.html` line 36 (stray `{% endif %}` tag), then test full daily entry workflow with photos to verify all data saves correctly and pages regenerate properly.

**After that:** Complete Issues 4-7, then import historical October-November data from ChatGPT conversations.