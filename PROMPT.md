===============================================
# 🌿 Master Garden AI Assistant Prompt
_Last Updated: January 5 8:45 PM_
===============================================

## Purpose

This file maintains context for AI assistants working on the **Garden Journal** project. If development spans multiple sessions or reaches token limits, this file helps new AI instances understand:

- The project's current state and progress
- What has been completed
- What is currently being worked on
- What comes next in the development roadmap
- Key conventions and practices to follow
- **How the user prefers to work**

**Read this file first** before beginning any work on the project to ensure continuity and consistency.

---

## 🚨 Critical Instructions

### How This User Works - MUST READ

**The user has strong preferences for workflow and will correct you if you deviate:**

1. **NO assumptions without confirmation**
   - When you identify something that needs fixing, describe it and WAIT for confirmation
   - Don't implement changes and then ask if they're correct
   - Don't move forward with "I'll do X" - ask first "Should I do X?"

2. **Token consciousness**
   - User is always aware of token limits
   - Don't add unnecessary explanations or context the user already knows
   - If user says "I already did this locally" - don't repeat instructions
   - Keep responses concise unless detail is specifically requested

3. **Incremental changes**
   - Make ONE change at a time when debugging
   - Wait for user to test before proceeding
   - Don't bundle multiple fixes together unless explicitly asked

4. **File handling**
   - When user uploads files, they expect you to read and understand them fully
   - Check uploaded files against project knowledge to spot differences
   - Don't recreate entire files unless necessary - provide find/replace when possible
   - **CRITICAL:** When user provides file in parts, reconstruct EXACTLY as provided with ONLY requested changes

5. **Testing cycle**
   - User will say "Testing now!!!" when ready to test
   - Stand by for results - don't assume success
   - When bugs appear, investigate carefully before proposing fixes

6. **Commit discipline**
   - User will ask for commit messages when ready
   - Always provide full `git add -A && git commit -m "..." && git push` format
   - Commit messages should be comprehensive but concise

7. **Historical context matters**
   - This tool has been working perfectly for over a month
   - If something breaks during a session, it's from TODAY's changes
   - Always check what changed today vs what was working before
   - Don't make up explanations - investigate actual differences

8. **"Does this make sense?" means the user wants confirmation you understand**
   - Respond with your understanding and ask clarifying questions if needed
   - Don't just say "yes" - demonstrate comprehension

9. **When asked "tell me what you see" - ONLY answer that question and STOP**
   - Do NOT proceed with any work until explicitly told to
   - Wait for confirmation with "yes, proceed" or similar

10. **Separation of Concerns - PRIME DIRECTIVE**
    - NEVER use inline styles in HTML templates
    - ALL styling goes in `static/style.css`
    - Use existing CSS classes or create new ones as needed
    - If you violate this, you're creating technical debt and bugs

11. **Work incrementally on complex features**
    - Break down multi-step features into individual steps
    - Wait for user confirmation after each step
    - This prevents overwhelming the user and allows for course correction

### File Creation Protocol

**CRITICAL:** When creating or updating files (markdown, JSON, or any code), ALWAYS use a **code artifact** with appropriate language tag (application/vnd.ant.code with language="markdown", "json", etc.), NOT a document artifact. The code artifact must appear in the sidebar as a persistent artifact. The user needs to copy raw code, not a rendered preview. If the content appears as formatted/styled text instead of a code block in the sidebar, regenerate it as a code artifact.

### Accessing Project Files

**IMPORTANT:** In Claude Projects, repository files are NOT accessible via traditional file system paths like `/mnt/user-data/uploads`. Instead, use the `project_knowledge_search` tool to access synced repository content.

**How to access files:**
```
<invoke name="project_knowledge_search">
<parameter name="query">data plants JSON arugula basil</parameter>
</invoke>
```

**What this returns:**
- File contents from the synced repository
- Multiple relevant files and sections
- Actual data you can work with

**Don't panic if:**
- Files don't appear in `/mnt/user-data/uploads`
- Traditional file system commands show empty directories
- The project seems "not synced"

**The files ARE there** - just access them via `project_knowledge_search` instead of file system paths.

---

## 📁 Project Overview

**Repository:** garden_journal
**Type:** Self-hosted Flask web application
**Purpose:** Personal garden management dashboard with plant tracking, journal entries, and photo management

### Tech Stack
- **Backend:** Python Flask
- **Frontend:** HTML, CSS (unified), Jinja2 templates
- **Data Storage:** JSON files (file-based, no database)
- **Image Processing:** PIL/Pillow (for photo compression)
- **Photo Storage:** Google Drive (local mount path)

### Key Files
- `app.py` - Flask server with all routes
- `data_manager.py` - JSON read/write operations
- `static/style.css` - Single unified CSS file for all pages
- `static/modal.js` - Modal interaction JavaScript
- `templates/dashboard.html` - Master garden dashboard template
- `templates/journal.html` - Dynamic plant journal template
- `templates/photo_prep.html` - Photo preparation tool
- `templates/journal_update.html` - Journal entry submission
- `templates/channel_start.html` - ChatGPT channel initialization
- `templates/assist_corrections.html` - Correction management tool
- `data/` - JSON data files (plants, containers, products, dashboard_order, assist_corrections, watering_estimates.csv)
- `docs/schema.md` - Complete data schema documentation
- `docs/photo_requirements.md` - Photo handling system requirements and workflow
- `MASTER_GARDEN_TEMPLATES_OVERVIEW.md` - Complete functional reference for all templates (what each does, button actions, data flow)
- `PROMPT.md` - This file (AI assistant continuity)

---

## 🎯 Current Development Status

**Current Phase:** Photo Prep Tool Enhancements - December 30, 2025

### ✅ Completed Today (Dec 30, 2025)

**Morning Session - Photo Prep Overhaul:**
1. **Form Restructuring**
   - Moved Context to top (first field)
   - Consolidated Date, Plant ID, Starting Photo #, Time Override into single row
   - Relocated photo upload zone after checkboxes
   - Added Time Override field for backdating follow-up actions

2. **Follow-Up Template (New Format)**
   - Cleaner "{time} Same Day Follow-up" format
   - Upfront check for JSON in context
   - Conditional photos section (only if photos uploaded)
   - Conditional q_and_a_summary section (Questions checkbox)
   - Proper single blank line spacing between sections
   - Time override used throughout when provided
   - Removed redundant validation lines (commented out)

3. **Smart Watering Prompt**
   - Detects if form date is today vs yesterday
   - Today: "Should I water at 6:00 AM tomorrow morning?"
   - Yesterday: "Should I water right now the following day?"
   - Uses time override in prompt

4. **Auto-Fetch Features**
   - Auto-populate starting photo number when Plant ID selected in Follow-Up
   - Triggers on Plant ID change, Context change, Date change
   - Silent failure with placeholder text

5. **Smart Validation (Follow-Up only)**
   - Auto-fetch starting photo if blank or 1
   - Alert + focus if Plant-Specific Message blank
   - Server-side journal entry validation
   - Removed duplicate client-side validation

6. **Smart Field Persistence**
   - Plant-Specific Message persists through date/plant changes
   - Plant ID persists through date changes
   - Prevents accidental data loss

7. **Assist Corrections Tool Enhancement**
   - Added "📋 Copy Prompt" button
   - Generates ChatGPT prompt with:
     - List of highest numerical ID for each parent category
     - Complete markdown template
   - Copies to clipboard with visual feedback
   - Helps ensure correct ID sequencing for new corrections

8. **Bug Fixes (Morning)**
   - Fixed dashboard.html timeline display (stage → what_i_should_see)
   - Fixed pepper_003.json schema compliance
   - Restored missing assist_corrections routes
   - Fixed probe checkbox behavior (was filtering photos, now just adds indicator)
   - Fixed "Here are the photo names:" missing in Initial output
   - Fixed final instructions missing for Initial context
   - Fixed weather text concatenation (NWS line breaks using `<br>` tags)
   - Fixed instructions line missing in Follow-Up ("Do NOT reconstruct...")
   - Fixed probe indicators missing in Follow-Up output
   - Fixed assist_corrections create route to use user-provided ID
   - Fixed Initial context instructions (separated watering from final instructions)
   - Fixed Follow-Up context instructions (photo-specific validation only when photos present)

**Afternoon Session - Critical Fixes:**

9. **Journal Update Fragment Handling (MAJOR FIX)**
   - **Problem:** Plant Main Data fragment update was broken - added validation logic that prevented simple fragment updates
   - **Root Cause:** Code was changed from simple key-value replacement to field-specific validation
   - **Solution:** Restored original Dec 23 logic:
     - Parse JSON fragment (auto-wrapped in `{}`)
     - Strip leading whitespace from each line (handles indented fragments from ChatGPT)
     - Loop through key-value pairs
     - Update ONLY those fields in plant object
     - Save plant
   - **Key insight:** Fragments have 2-space indentation for copy/paste readability - must strip before parsing
   - This was working perfectly for over a month before being accidentally changed

10. **Separation of Concerns - CSS Cleanup**
    - **Violation found:** Inline styles on checkboxes in photo_prep.html
    - **Fix:** Removed ALL inline styles from checkbox labels
    - **Solution:** Use existing `.radio-label` class from style.css
    - **Prime Directive restored:** All styling in CSS, none in HTML

11. **Photo Prep Enhancement - Latest Journal Entry**
    - Added "Add latest journal entry" checkbox (unchecked by default)
    - When checked, appends latest journal entry JSON to output (both Initial and Follow-Up contexts)
    - Format:
      ```
      Here is the last journal entry so you have it in context:

      ```json
      {latest journal entry}
      ```
      ```
    - Helps ChatGPT maintain continuity without reconstructing data

12. **Dashboard Enhancement - Actions Summary**
    - Added "📋 Actions" button to chip-row navigation
    - Fetches latest `actions` field from most recent journal entry for each plant
    - Generates markdown list (no backticks, blank line between entries)
    - Copies to clipboard with ✓ feedback
    - Quick way to see all current action items across entire garden

13. **Documentation - Template Overview**
    - Created `MASTER_GARDEN_TEMPLATES_OVERVIEW.md` in root directory
    - Complete functional reference for all templates
    - Documents what each button does, data sources, output formats
    - Perfect for onboarding new AI assistants or explaining to ChatGPT
    - Separate from README (high-level) and schema docs (low-level)

**Evening Session - Watering Guide Feature:**

14. **Photo Prep Enhancement - Watering Guide**
    - Added "💦 Watering Guide" button next to Refresh Weather
    - Parses Global Message (Weather) for:
      - Weather condition (maps Mostly Sunny→Sunny, Mostly Cloudy→Cloudy, Mostly Clear→Sunny)
      - High temperature
      - Overnight low temperature
      - Precipitation percentage (or 0% if none)
      - Moisture readings for each plant (format: "plant_id: value, plant_id: value")
    - Loads `data/watering_estimates.csv`
    - For each plant with moisture reading:
      - Matches by: plant_id, condition, precip range, moisture range, high temp range
      - Extracts watering instruction from appropriate column
      - Checks if overnight low triggers "Bring Inside/Cover" threshold
    - Generates markdown output:
      ```
      WEATHER
      {weather text only - moisture readings removed}

      6 AM WATERING INSTRUCTIONS
      - plant_id: watering instruction

      ‼️ BRING INSIDE / COVER BEFORE 6 PM (only if needed)
      - plant_id
      ```
    - Copies to clipboard with ✓ Copied! visual feedback (2 seconds)
    - New API route: `/api/watering-guide` (POST)

15. **Template Data Attributes Fix**
    - Removed Jinja2 template syntax from JavaScript (was causing IDE errors)
    - Moved template data to HTML data attributes on success card
    - JavaScript reads from `dataset` instead of inline template variables
    - Cleaner separation of concerns, no more IDE complaints

### 🐛 Known Issues
- Inline styles still present in photo_prep.html (weather buttons section) - needs cleanup

### 📋 Next Up

**PRIORITY 1: Remove All Inline Styles (Prime Directive Violation)**
- **Problem:** photo_prep.html still has inline styles in several places (weather button section, checkbox container)
- **Solution:** Create appropriate CSS classes in style.css, remove all inline `style=` attributes
- **Goal:** Complete separation of concerns - zero inline styles anywhere
- **Importance:** HIGH - this is a Prime Directive violation and creates technical debt

**PRIORITY 2: Add Third Context State to Photo Prep Tool**
- **Problem:** Photo Prep currently has Initial and Follow-Up contexts hardcoded in app.py
- **Need:** Add third context state (TBD) and make prompts easily editable without code changes
- **Solution:** Similar to channel_start tool:
  - Create markdown template files for each context (e.g., `photo_prep_initial.md`, `photo_prep_followup.md`, `photo_prep_[new].md`)
  - Support variable substitution from plant JSON (e.g., `{id}`, `{plant}`, `{garden_location}`)
  - Load templates from files instead of hardcoded strings in app.py
  - Make it easy for user to edit prompts by editing markdown files
- **Benefits:**
  - User can edit prompts without coming to AI assistant
  - Easy to add new context states
  - Cleaner code separation
  - Consistent with channel_start pattern

**PRIORITY 3: Regenerate Button (Previously ITEM 2)**
- **Problem:** User makes a mistake in form, submits, gets output, then realizes the error. Currently must start over.
- **Solution:** Add "🔄 Regenerate" button on success page that:
  1. Returns to form with all fields pre-populated
  2. Keeps filename list in readonly/disabled state (can't restore actual file uploads due to browser security)
  3. Allows fixing the mistake and resubmitting
- **Implementation Notes:**
  - Button appears on success page next to "Process Another Plant" and "Start Fresh"
  - Uses URL parameters or localStorage to pass form state back
  - Photo filenames shown as text list (read-only) since actual File objects can't be restored
  - User can change any other field and resubmit
  - Form should clearly indicate it's in "regenerate mode" with photos locked

---

## 🗺️ Development Phases

### Phase 1: Foundation Setup (COMPLETE ✅)
- [x] Repo structure
- [x] Flask webserver (`app.py`)
- [x] Data manager (`data_manager.py`)
- [x] Base CSS (`style.css`)
- [x] Requirements file

### Phase 2: Dynamic Master Dashboard (COMPLETE ✅)
- [x] Load plant data from JSON files
- [x] Display plants as tiles
- [x] Show basic plant info
- [x] Apply unified CSS
- [x] Category grouping (dashboard_order.json)
- [x] Navigation with emojis

### Phase 3: Plant Detail Modal (COMPLETE ✅)
- [x] Create modal overlay component
- [x] Click plant tile to open modal
- [x] Display plant main data (current_stage, current_state)
- [x] Display journal entries in chronological order
- [x] Show probe readings (digital and analog)
- [x] Show observations, actions, next steps, Q&A, follow-ups
- [x] Display photo placeholders and actual photos
- [x] Modal close functionality (ESC key, backdrop click)
- [x] Dynamic journal route (`/journal/<plant_id>`)
- [x] Unified CSS styling across dashboard and journal

### Phase 4: GPT Integration Forms (COMPLETE ✅)
- [x] Channel Start tool
- [x] Journal Update tool
- [x] Assist Corrections tool
- [x] Actions Summary button

### Phase 5: Photo Management System (COMPLETE ✅)
- [x] **Photo Prep Tool** - Compression, renaming, organization
- [x] **Google Drive Integration** - Photo serving from Google Drive
- [x] **Placeholder Upload** - Single photo upload for past entries
- [x] **Photo Lightbox** - Click to view full-size with caption
- [x] **Follow-Up Support** - Auto-fetch photo numbers, smart validation
- [x] **Weather Integration** - Manual refresh button, caching
- [x] **Smart Persistence** - Form field persistence across changes
- [x] **Assist Corrections Enhancement** - Copy Prompt for ChatGPT
- [x] **Latest Journal Entry** - Checkbox to append to output
- [x] **Actions Summary** - Dashboard button to copy all current actions
- [x] **Watering Guide** - CSV-based watering instruction generator

---

## 🔑 Key Project Conventions

### Naming Conventions
- Use `app.py` for the Flask server
- Keep Python utility files in root (e.g., `data_manager.py`)
- Use descriptive, snake_case for Python files
- Use kebab-case for HTML files

### Code Organization
- Flask routes in `app.py`
- Data operations in `data_manager.py`
- Templates use Jinja2 for dynamic content
- Single `style.css` for all pages (unified styling)
- Modal JavaScript in `static/modal.js`
- ChatGPT-related files in `chatgpt/` folder
- Photo prep prompt templates will go in `photo_prep/` folder (future)

### Data Structure
- Individual plant files: `data/plants/*.json`
- Shared data: `data/containers.json`, `data/products.json`, `data/meta.json`
- Dashboard ordering: `data/dashboard_order.json`
- Assist corrections: `data/assist_corrections.json`
- Watering estimates: `data/watering_estimates.csv`
- See `docs/schema.md` for complete data schema
- All dates: `M/D/YYYY` format (in JSON)
- All times: `H:MM AM/PM` format
- Photo filenames: `{plant_id}-{YYYYMMDD}-{##}.jpeg`

### Python Commands
- Always use `python3` instead of `python` for all commands
- Example: `python3 app.py` NOT `python app.py`

### File Artifacts
- Always create code artifacts for files the user will copy
- Use appropriate language tags (markdown, json, python, html, css, javascript)
- Never use document artifacts for code/configuration files

### Markdown File Headers
All markdown files must use this structure at the top:

```markdown
===============================================
# 🌿 Master Garden {Topic}
_Last Updated: {current date and time}_
===============================================
```

### Separation of Concerns - PRIME DIRECTIVE
**CRITICAL:** Never use inline styles in HTML templates
- ALL styling goes in `static/style.css`
- Use existing CSS classes or create new ones as needed
- Inline styles create technical debt and bugs
- If you find inline styles, remove them and use CSS classes
- **Current violation:** photo_prep.html still has inline styles that need cleanup

---

## 📝 Git Commit Guidelines

### Pre-Commit Review Process

**CRITICAL:** Before every commit, ALWAYS review and update:
1. **PROMPT.md** - Update status, phases, and timestamp
2. **README.md** - Update progress, features, and timestamp (if needed)

This ensures documentation stays in sync with code changes.

### When to Suggest a Commit

Suggest a commit when:
1. **Feature completion** - A complete feature or sub-task is finished and working
2. **Logical checkpoint** - A meaningful unit of work is complete
3. **File creation** - New files are created and ready to be tracked
4. **Documentation updates** - README, schema, or other docs are updated
5. **Bug fixes** - A bug is identified and fixed
6. **Refactoring** - Code is reorganized or improved without changing functionality

### When NOT to Commit

Don't suggest commits for:
- Incomplete features or broken code
- Work-in-progress that doesn't run
- Every single line change (too granular)
- Temporary or experimental code

### Commit Message Format

Follow the **Conventional Commits** standard:

```
<type>: <subject>

<body (optional)>
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style/formatting (no logic change)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

**Always provide as single copyable command:**

```bash
git add -A && git commit -m "type: Brief description

- Bullet point of what changed
- Another change
- Another change" && git push
```

---

## 💬 Communication Style

**Based on user preferences observed in this project:**

- **Be concise** - User is token-conscious
- **Ask before implementing** - Don't assume
- **One thing at a time** - Incremental changes
- **Wait for confirmation** - Especially when debugging
- **Historical awareness** - Check what changed today vs before
- **No unnecessary explanations** - User knows the project well
- **Demonstrate understanding** - When user asks "does this make sense?"
- **Find/replace over full files** - When possible
- **Investigate before explaining** - Don't make up reasons
- **When asked "what do you see?" - ONLY answer that and STOP**
- **NEVER use inline styles** - Separation of concerns is sacred
- **Work step-by-step on complex features** - Prevents overwhelming user

---

## 📚 Photo Prep Tool - Current State

### Form Layout (Top to Bottom)
1. **Context** (Initial / Follow-Up)
2. **Row:** Date | Plant ID | Starting Photo # | Time Override
3. **File Upload Zone** (drag & drop)
4. **Checkboxes:** Include watering | Include questions | Add latest journal entry
5. **Global Message (Weather)** with 💦 Watering Guide and 🌤️ Refresh Weather buttons
6. **Plant-Specific Message**
7. **Process Photos** button

### Watering Guide Feature
- **Input:** Weather text + moisture readings in Global Message (format: "plant_id: value, plant_id: value")
- **Processing:**
  - Parses condition (maps to Sunny/Partly Cloudy/Cloudy)
  - Extracts high temp, overnight low, precipitation %
  - Determines moisture range per plant (Dry 0-3, Normal 3-7, Wet 7-10)
  - Matches against `data/watering_estimates.csv` by: plant_id, condition, precip range, moisture range, temp range
  - Checks overnight low against "Bring Inside/Cover" thresholds
- **Output:** Markdown with weather, watering instructions per plant, optional bring inside alert
- **CSV Columns:** id, Bring Inside/Cover, Precip Range, Condition, 6AM Moisture, temp columns (60-65°F through 90+°F)

### Initial Context Output Format
```
{weather}

{plant_specific_message}

Here are the photo names:
1. filename.jpeg ← (probe reading)
2. filename.jpeg
3. filename.jpeg

[Watering prompt if checked]

Please provide:
Full Expert Assessment → Daily Journal Entry JSON → Plant Main Data Review (silently) → Result

If weather, probe readings, or photos are missing, ask me for them before beginning.

[Latest journal entry if checked]
```

### Follow-Up Context Output Format
```
{time} Same Day Follow-up

{plant_specific_message}

First, make sure you have today's most recent Daily Journal Entry JSON in context because I will have you update it after we discuss and I don't want you reconstructing or inventing a replacement JSON.

Then, respond naturally. Then re-issue today's most recent COMPLETE Daily Journal Entry JSON (above in this chat) and change nothing other than the following:

[Photos section if photos uploaded]
New photo(s) to append to existing `photos` array (generate a real caption + tags for each — no blanks):
1. filename.jpeg ← (probe reading)
2. filename.jpeg

New follow-up to append to existing `follow_up` array:
"[{time}] {replace with narrative summary}"

[Q&A section if Questions checkbox checked]
Update `q_and_a_summary` by APPENDING a short narrative summary of the new question(s) + answer(s) to the existing text (do not overwrite).

[Photo reminder if photos uploaded]
If photo filenames are listed but no photos were uploaded, reply only: "Please provide the photos referenced." and wait for them before responding further.

[Latest journal entry if checked]
```

**Commented out lines (kept for reference):**
```
Output valid JSON only (exact schema, no invented fields).
Do NOT change the Daily Journal Entry `time` (it remains the probe timestamp).
Do NOT reconstruct or invent a replacement JSON.
```

### Key Behaviors
- **Auto-fetch starting photo** when Plant ID changes in Follow-Up mode
- **Smart validation** for Follow-Up (plant message required, journal entry exists)
- **Field persistence** - Plant message and Plant ID survive form changes
- **Time override** - Replaces current time throughout output when provided
- **Weather caching** - localStorage with date validation
- **Manual refresh** - User controls when to fetch fresh weather
- **Conditional sections** - Photos and Q&A only show when applicable
- **Probe indicators** - Checkbox adds "← (probe reading)" to output, doesn't filter
- **Latest journal entry** - Checkbox appends JSON for context
- **Watering guide** - CSV-based instruction generator with bring inside alerts

---

## 📚 Journal Update Tool - Current State

### Fragment Handling (CRITICAL)
**Plant Main Data fragments:**
- Accepts indented JSON fragments (2-space indentation from ChatGPT)
- Auto-strips leading whitespace from each line
- Auto-wraps in `{}` if not present
- Removes trailing commas
- Parses and updates ONLY the fields present in fragment
- Simple key-value replacement - no field validation
- Works with ANY plant main data fields (container, soil_mix, origin_history, whats_been_logged, current_stage, current_state, timeline, etc.)

**This logic was working perfectly for over a month - do not change it!**

---

## 📚 Assist Corrections Tool - Current State

### Copy Prompt Feature
- **📋 Copy Prompt** button next to "+ Add New"
- Generates ChatGPT-ready prompt containing:
  - List of highest numerical ID for each parent category
  - Complete markdown template for new corrections
- Automatically parses all correction IDs
- Finds highest number per prefix (e.g., DW-ASSESSMENT-003, PMD-TIMELINE-004)
- Copies to clipboard with visual feedback (✓ Copied!)
- Ensures correct ID sequencing when creating new corrections

### Primary Purpose
- Track how often corrections are needed (via `count` field)
- Identify where ChatGPT guide needs improvement
- Secondary: Provide correct wording to get ChatGPT back on track

---

## 📚 Dashboard - Actions Summary

### Actions Button
- **📋 Actions** button in chip-row navigation
- Fetches latest `actions` field from most recent journal entry for each plant
- Generates markdown list:
  - Format: `- plant_id: action text`
  - Blank line between each entry
  - No backticks around plant_id
- Copies to clipboard with ✓ feedback
- Quick reference for all current garden action items

---

## 📚 Additional Resources

- **Data Schema:** See `docs/schema.md` for complete JSON structure
- **Photo System:** See `docs/photo_requirements.md` for photo workflow
- **Template Reference:** See `MASTER_GARDEN_TEMPLATES_OVERVIEW.md` for complete functional documentation
- **Assist Corrections:** See `data/assist_corrections.json` for IF/THEN statements
- **ChatGPT Integration:** See `chatgpt/` folder for plant channel templates
- **Watering Estimates:** See `data/watering_estimates.csv` for watering instruction lookup table
- **Project Structure:** See README.md for complete folder tree

---

## 🔄 Updating This File

When significant progress is made:
1. Update "Current Development Status" section
2. Check off completed tasks in "Development Phases"
3. Update the "Last Updated" timestamp at the top
4. Add new conventions or guidelines if discovered
5. Update "Next Up" section with upcoming work
6. Commit with clear documentation update message

---

**Remember:** This user values:
- Precision over speed
- Confirmation over assumption
- Investigation over explanation
- Incremental progress over big changes
- Token efficiency
- Historical context
- **EXACT file reconstruction when provided in parts**
- **Separation of concerns - NO inline styles**
- **Step-by-step on complex features**

When in doubt, **ask first, implement second**.