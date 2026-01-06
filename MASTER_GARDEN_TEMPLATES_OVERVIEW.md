===============================================
# 🌿 Master Garden Dashboard - Template Files Overview
_Last Updated: December 30, 2025_
===============================================

## Core Dashboard & Journal

### dashboard.html - Master Garden Dashboard

**Purpose:** Main landing page displaying all plants organized by category

**Data Sources:**
- `data/dashboard_order.json` - Defines category order and which plants appear in each section
- `data/plants/{plant_id}.json` - Individual plant files for tile data (plant name, current_stage, current_state, origin_history, timeline, whats_been_logged)
- `data/meta.json` - Garden name and metadata

**Layout:**

**Chip-row navigation at top:**

*Plant Category Links:*
- When clicked, scrolls to the corresponding section of plant tiles
- Each tile displays:
  - Plant name with emoji
  - Current stage (pill indicator)
  - Origin/history bullet list
  - What's been logged summary
  - Current state description
  - Timeline with projected dates
  - **📓 View Journal** link
- When **📓 View Journal** is clicked, opens journal.html in modal overlay (see journal.html section below)

*Tool Links:*
- **📸 Open Photo Tool** - Opens photo_prep.html (see Photo Prep Tool section below)
- **🔧 Open Correction Tool** - Opens assist_corrections.html (see Assist Corrections Tool section below)
- **📝 Journal Update** - Opens journal_update.html (see Journal Update Tool section below)
- **🚀 Channel Start** - Opens channel_start.html (see Channel Start Tool section below)
- **📋 Actions** - Fetches the latest `actions` field from the most recent journal entry for each plant, generates markdown list (format: `- plant_id: action text` with blank line between each entry, no backticks), copies to clipboard, shows ✓ Actions feedback for 2 seconds

---

### journal.html - Individual Plant Journal View

**Purpose:** Detailed journal view for a single plant, opened from dashboard tiles in a modal overlay

**Data Source:**
- Single `data/plants/{plant_id}.json` file

**Displays:**
- Plant header with current state/stage
- All journal entries in reverse chronological order (newest first)
- Each entry showing:
  - Date and time
  - Weather conditions
  - Digital probe readings (pH, moisture, EC, NPK, temperature)
  - Analog probe reading (if present)
  - Observations
  - Actions taken
  - Next steps
  - Q&A summary (if present)
  - Follow-ups (if present)
  - Photos with captions

**Features:**
- **Photo lightbox:** Click any photo to view full-size with caption overlay
- **Placeholder photo upload:** Click placeholder tiles (📷 Click or Drop Photo Here) to upload a single photo for past entries
  - Automatically determines filename from context (plant_id, date, photo index)
  - Compresses and saves to Google Drive
  - Updates plant JSON with new photo entry

**Buttons:**
- **🌿 Back to Dashboard** - Returns to dashboard.html

---

## ChatGPT Integration Tools

### channel_start.html - Channel Start Tool

**Purpose:** Bootstrap new ChatGPT plant channels with initialization messages

**Data Sources:**
- `data/plants/{plant_id}.json` - Selected plant data
- `chatgpt/master_garden_01_ai_prompt.md` - AI prompt template
- `chatgpt/master_garden_02_ai_guide.md` - AI guide template
- `chatgpt/master_garden_04_ai_after_json.md` - Post-JSON instructions
- `chatgpt/master_garden_05_ai_one_time_correction.md` - One-time patch content

**Form Fields:**
- **Plant ID** dropdown - Select plant from your garden (autocomplete)

**Buttons:**

- **🚀 Start Channel**
  - Combines: AI prompt template + AI guide + plant JSON + post-JSON instructions
  - Replaces variables: `{id}`, `{plant}` with actual plant data
  - Outputs complete initialization message ready to paste into new ChatGPT chat
  - Shows output with **Copy** button

- **🔧 One-Time Patch**
  - Returns one-time correction message from template file
  - Used for applying corrections to existing channels
  - Shows output with **Copy** button

- **✏️ Rename Chat**
  - Generates chat rename string in format: `🌿 MG: {plant_id}`
  - Shows output with **Copy** button

**After generating output:**
- **Copy** button - Copies output message to clipboard, shows ✓ feedback for 2 seconds

---

### journal_update.html - Journal Update Tool

**Purpose:** Paste ChatGPT-generated journal entries or plant main data fragments to update plant JSON files

**Data Source:**
- `data/plants/{plant_id}.json` - Target plant to update

**Form Fields:**
- **Plant ID** dropdown - Select plant from your garden (autocomplete, persists between updates)
- **Journal Entry JSON** textarea - Paste JSON from ChatGPT (auto-cleans trailing commas, wraps fragments in `{}`if needed, strips leading whitespace from each line)

**Buttons:**

- **📝 Update Journal Entry**
  - Validates required fields: date, time, conditions, digital_probe, observations
  - Adds new journal entry to beginning of journal array (newest first)
  - Saves plant JSON
  - Shows success message with entry date/time and total entry count

- **🔧 Update Plant Main Data**
  - Accepts JSON fragments (fields like: container, soil_mix, origin_history, whats_been_logged, current_stage, current_state, timeline)
  - Auto-wraps fragments in `{}`, strips indentation
  - Updates ONLY the fields present in the fragment
  - Leaves other plant data untouched
  - Saves plant JSON
  - Shows success message with updated field names

**After successful update:**
- **← Try Again** button - Returns to form with Plant ID preserved, ready for another update
- Plant ID persists in dropdown for convenience

**Error Handling:**
- Displays specific error messages for: missing Plant ID, missing JSON input, invalid JSON format, plant not found, missing required fields

---

### photo_prep.html - Photo Prep Tool

**Purpose:** Compress, rename, and organize photos for ChatGPT plant channels

**Data Sources:**
- `data/plants/{plant_id}.json` - For auto-fetching last photo number in Follow-Up mode and validating plant exists
- Weather API (`/api/weather/current`) - National Weather Service forecast for Loxahatchee, FL
- localStorage - For weather caching (date-validated) and global message persistence

**Form Fields:**
- **Context** dropdown - Initial (first check-in) or Follow-Up (same-day update)
- **Date** - Date picker (defaults to today)
- **Plant ID** - Text input with autocomplete (validates against plant list)
- **Starting Photo #** - Number input (auto-fills in Follow-Up mode when plant selected)
- **Time Override** - Text input (optional, replaces current time throughout output)
- **Photo Upload Zone** - Drag & drop or click to select 1-20+ photos
  - Shows thumbnail previews
  - Each photo has probe reading checkbox (adds "← (probe reading)" indicator to output)
- **Include watering assessment prompt** - Checkbox (unchecked by default, adds smart watering prompt with time context)
- **Include questions section** - Checkbox (adds Q&A update section in Follow-Up output)
- **Add latest journal entry** - Checkbox (unchecked by default, appends latest journal entry JSON to output)
- **Global Message (Weather)** - Textarea (Initial context only)
  - Auto-fills with cached weather if from today
  - **🌤️ Refresh Weather** button - Fetches fresh forecast from NWS, updates cache
- **Plant-Specific Message** - Textarea (observations for this specific plant, persists across form changes)

**Buttons:**

- **📤 Process Photos**
  - Validates: Plant ID exists, photos provided (Initial only), date provided, plant-specific message (Follow-Up only)
  - Compresses photos to JPEG at 85% quality
  - Auto-rotates based on EXIF orientation
  - Renames to format: `{plant_id}-{YYYYMMDD}-{##}.jpeg`
  - Saves to Google Drive: `/Garden Photos/{plant_id}/`
  - Generates formatted output based on context:
    - **Initial:** Weather + plant message + photo list + optional watering prompt + final instructions
    - **Follow-Up:** Time + plant message + JSON check reminder + conditional sections (photos, follow-up, Q&A) + optional latest journal entry
  - Shows success page with output message

**After successful processing:**
- **🌱 Process Another Plant** - Reloads form, preserves: global message (weather), date
- **🔄 Start Fresh** - Reloads form, clears everything except weather cache
- **Copy** button (on output) - Copies formatted message to clipboard, shows ✓ feedback for 2 seconds

**Features:**
- **Auto-fetch starting photo number:** In Follow-Up mode, when Plant ID changes, automatically fetches last photo number from today's journal entry and increments
- **Smart validation:**
  - Follow-Up checks for existing journal entry on selected date
  - Alerts if Plant-Specific Message blank in Follow-Up
  - Auto-fetches photo number if blank or set to 1
- **Field persistence:**
  - Plant-Specific Message survives date/plant changes
  - Plant ID survives date changes
- **Weather caching:**
  - Stores weather in localStorage with date validation
  - Only uses cache if from today
  - Manual refresh always fetches fresh data
- **Smart watering prompt:**
  - Detects if form date is today vs yesterday
  - Today: "Should I water at 6:00 AM tomorrow morning?"
  - Yesterday: "Should I water right now the following day?"
  - Uses time override in prompt if provided

**Output Formats:**

*Initial Context:*
```
{weather}

{plant_specific_message}

Here are the photo names:
1. filename.jpeg ← (probe reading)
2. filename.jpeg

[Watering prompt if checked]

Please provide:
Full Expert Assessment → Daily Journal Entry JSON → Plant Main Data Review (silently) → Result

If weather, probe readings, or photos are missing, ask me for them before beginning.

[Latest journal entry if checked]
```

*Follow-Up Context:*
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

---

### assist_corrections.html - Assist Corrections Tool

**Purpose:**
- **Primary:** Track how often corrections are needed (via `count` field) to identify where the ChatGPT guide needs improvement
- **Secondary:** Provide correct wording to get ChatGPT back on track in the interim

**Data Source:**
- `data/assist_corrections.json` - All correction entries with metadata (id, title, category, sub_category, trigger_if, response_then, anti_patterns, tags, include_footer, count, applies_when)

**Features:**

**Search & Browse:**
- **Search bar** - Filter corrections by keyword in title or trigger_if text
- **Category dropdown** - Filter by category (e.g., Daily Workflow, Plant Main Data, Probe Reading Devices)
- **Sub-category dropdown** - Filter by sub-category (populates based on selected category)
- **Top 5 Corrections** - Shows most-used corrections (by count) with quick links

**Correction Tiles:**
Each tile displays (collapsed by default):
- Title
- Category / Sub-category
- ID
- Usage count
- IF (trigger) text preview

When clicked/expanded, shows:
- Full IF (trigger) condition
- **Copy This THEN Message to ChatGPT:** label with THEN response text
- **Copy** button - Copies THEN message to clipboard (with optional footer), increments count, shows ✓ feedback
- **Edit** button - Switches to edit mode
- Anti-patterns list (what it looked like when wrong)
- Tags
- Checkbox: "Include 'Acknowledge the Correction...' footer when copying" (checked by default per correction's `include_footer` setting)

**Edit Mode:**
When **Edit** button clicked:
- THEN text becomes editable textarea
- **Copy** button remains active
- **Edit** button changes to **Save** button
- When **Save** clicked:
  - Updates `response_then` field in JSON
  - Exits edit mode
  - Updates displayed text

**Buttons:**

**Header Actions:**

- **📋 Copy Prompt**
  - Parses all correction IDs
  - Finds highest numerical ID for each prefix (e.g., DW-ASSESSMENT-003, PMD-TIMELINE-004)
  - Generates markdown with:
    - Comma-separated list of highest IDs per category
    - Complete blank markdown template for new correction
  - Copies to clipboard for pasting into ChatGPT
  - Shows "✓ Copied!" feedback for 2 seconds
  - **Purpose:** Ensures correct ID sequencing when creating new corrections via ChatGPT

- **+ Add New**
  - Toggles Add New Correction form
  - Form accepts markdown format (parses: ID, TITLE, CATEGORY, SUB-CATEGORY, IF, THEN, ANTI-PATTERNS, TAGS)
  - Checkbox: "Include 'Acknowledge the Correction...' footer when copying" (checked by default)
  - **Save Correction** button - Parses markdown, creates new correction object, adds to JSON, reloads page
  - **Cancel** button - Hides form

**Per-Correction Actions:**

- **Copy** button
  - Copies THEN message to clipboard
  - Optionally appends: "Acknowledge the correction with one brief sentence confirming you will follow this approach going forward, then immediately continue the workflow as my professional horticulturist or extension agent." (based on checkbox state)
  - Increments `count` field in JSON
  - Shows ✓ feedback for 2 seconds

- **Edit** / **Save** button
  - **Edit mode:** Makes THEN text editable
  - **Save mode:** Updates `response_then` in JSON, exits edit mode

**Usage Tracking:**
- Every time **Copy** button clicked, increments `count` field
- Allows tracking which corrections are needed most frequently
- Informs improvements to ChatGPT guide to reduce need for corrections

---

## Summary

The Master Garden Dashboard provides:
- **Central hub** (dashboard.html) for viewing all plants and accessing tools
- **Detailed plant journals** (journal.html) with full history and photo management
- **ChatGPT integration tools** for bootstrapping channels, updating data, and preparing photos
- **Correction management** to track and improve ChatGPT assistant performance

All tools follow separation of concerns:
- **Backend (app.py):** Data fetching, validation, file operations, API routes
- **Frontend (templates):** User interaction, form handling, display logic
- **Styling (static/style.css):** All visual styling (no inline styles)
- **Data (data/ folder):** JSON files for plants, corrections, configuration