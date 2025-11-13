# Garden Journal Web Forms Requirements

**VERSION: 1.0**
**Last Updated: 2025-11-13**
**Status: Requirements Complete - Ready for Implementation**

---

## Overview

Local web application with HTML forms for adding plants, daily journal entries, and moving plants. Uses Flask backend to interface with existing `data_manager.py` functions.

---

## Technical Decisions

- **Framework:** Flask (Python web framework)
- **Port:** localhost:5000
- **Browser:** Chrome (primary testing)
- **Photo Source:** `/Users/jodisilverman/Library/CloudStorage/GoogleDrive-jodimsilverman@gmail.com/My Drive/GardenPhotos/`
- **Photo Workflow:** Export from iCloud Photos → Google Drive folder → Select in form → Compress & rename → Copy to `photos/` folder
- **Markdown Support:** All multi-line text areas support markdown bullets (dash-space for bullets, three-space-dash for indented)

---

## Photo Workflow

### User's Process:
1. Take photos with iPhone throughout the day
2. Photos sync to iCloud Photos automatically
3. Open Photos app on MacBook, go to "Garden" album
4. **Drag photos from Photos app to Google Drive folder** (auto-converts HEIC → JPEG!)
5. In web form: Browse to Google Drive folder, select photos
6. Form handles: compression (600×450px @ 85-90% quality), renaming (`plant_id_YYYYMMDD_HHMM_seq.jpg`), copying to repo `photos/` folder
7. Original photos remain in Google Drive folder

### Technical Requirements:
- Form can read from Google Drive CloudStorage path (tested ✓)
- JavaScript Canvas API for client-side image compression
- Auto-suggest filenames based on plant_id + EXIF date/time
- Target size: 600×450px (2.0" × 1.5" @ 300 DPI for print)
- Quality: 85-90% JPEG compression
- Extract EXIF metadata (date/time) from JPEGs
- No limit on number of photos per observation

---

## Form 1: Landing Page (forms/index.html)

### Purpose
Main navigation hub for the web application.

### Elements

**Header:**
- Title: "🌿 Garden Journal"

**Navigation Links:**
- Add New Plant
- Add Daily Entry
- Move Plant
- View Generated Journal (links to `output/` folder)

**Quick Stats Section:**
- Total active plants: X
- Last journal entry: [date]

---

## Form 2: Add Plant (forms/add_plant.html)

### Purpose
Add a new plant to the garden with initial location and summary.

### Form Fields

**Plant Information:**
- **Plant Type** (text input, required) - e.g., "basil", "tomato", "strawberry"
- **Common Name** (text input, required) - e.g., "Basil - Left"
- **Variety** (text input, optional) - e.g., "Sweet Basil"
- **Purchased/Sowed Date** (date picker, required) - converts to YYYYMMDD
- **Source** (text input, optional) - e.g., "Lowe's", "Seeds"

**Location & Container:**
- **Current Location** (text input or dropdown, required) - Panel 1-18, Picnic Table, Indoors, etc.
- **Container Name** (text input, required) - e.g., "Basil Pot - Left", "Raised Bed"
- **Container Type** (text input, required) - e.g., "Round Pot", "Window Planter"
- **Container Size** (text input, optional) - e.g., "8 inch, 0.94 gal"
- **Stake Number** (number input, optional) - If in shared staked container
- **Position** (text input, optional) - e.g., "left section", "edges"

**Soil & Care:**
- **Soil Mix** (text input, required) - e.g., "Potting Mix", "Topsoil/Sand"

**Initial Summary:**
- **Plant Summary** (textarea, optional) - Initial assessment/notes

**Form Buttons:**
- [Add Plant]
- [Cancel]

**Backend Action:**
- Calls `data_manager.add_plant()`
- Generates new plant_id automatically
- Creates initial location_history entry
- Shows success modal with plant details

---

## Form 3: Move Plant (forms/move_plant.html)

### Purpose
Record when a plant moves to a new location.

### Form Fields

- **Select Plant** (dropdown, required) - Shows all active plants: "Basil - Left (basil_001)", etc.
- **New Location** (text input or dropdown, required) - Panel 1-18, Picnic Table, Indoors, Garage, etc.
- **Reason for Move** (text input, required) - e.g., "Better sunlight", "Cold protection"
- **Date of Move** (date picker, required) - defaults to today

**Form Buttons:**
- [Move Plant]
- [Cancel]

**Backend Action:**
- Calls `data_manager.move_plant()`
- Adds entry to location_history
- Updates current_location
- Shows success modal

---

## Form 4: Daily Entry (forms/add_entry.html)

### Purpose
Add complete daily journal entry with all 6 sections.

---

### Basic Information

- **Date** (date picker, required) - defaults to today, converts to YYYYMMDD
- **Time of Entry** (time picker, required) - when filling out form, converts to HHMM

---

### Section 1: Summary of Activities

**Field:**
- **Activities** (textarea, markdown support)
  - Use `- ` for bullets
  - Use `   - ` (3 spaces + dash) for indented bullets
  - Converts to HTML `<ul>` lists on save

**Example input:**
```
- Watered all plants
- Pruned tomato
   - Removed diseased leaves
   - Cut back lower branches
- Added mulch to raised bed
```

---

### Section 2: Weather / Sun Conditions

**Fields:**
- **Temperature High** (number input, °F, optional)
- **Temperature Low** (number input, °F, optional)
- **Current Conditions** (text input, optional) - e.g., "Sunny", "Partly cloudy"
- **Sunrise Time** (time picker, optional)
- **Sunset Time** (time picker, optional)
- **Humidity** (text input, optional)
- **Wind** (text input, optional)
- **Notes** (textarea, optional)

---

### Section 3: General Observations

**Field:**
- **Observations** (textarea, markdown support)
  - Garden-wide notes
  - Same markdown bullet support as Activities

---

### Section 4: Questions & Answers (General)

**Repeatable Section** - Can add multiple Q&A pairs

Each Q&A pair:
- **Question** (text input)
- **Answer** (textarea)

**Button:**
- [+ Add Another Q&A]

---

### Section 5: Upcoming Actions

**Repeatable Section** - Can add multiple actions

Each action:
- **Description** (text input, required) - e.g., "Fertilize tomatoes"
- **Target Date** (date picker, optional)
- **Target Timeframe** (text input, optional) - e.g., "in 3 days", "next week"

**Button:**
- [+ Add Another Action]

---

### Section 6: Plant by Plant Observations

**Repeatable Section** - Can add multiple plant observations per entry

Each plant observation includes:

#### Plant Selection & Timing
- **Select Plant** (dropdown, required) - All active plants
- **Time of Observation** (time picker, required) - When you checked this plant (HHMM)

#### Plant Summary (Inline Editing)
- **Current Summary** (textarea, pre-loaded from plant data, editable)
  - Auto-loads when plant selected
  - Whatever is in the box when submitted = what gets saved to plant record
  - No buttons needed - just edit and submit

#### Container & Location Info
- **Container** (text input, auto-filled from plant data, editable)
- **Soil Mix** (text input, auto-filled from plant data, editable)

#### Soil Conditions
- **Soil Moisture** (text input, optional) - Free text: "4 (Green – ideal)", "bone dry", "lightly moist"
- **Soil pH** (text input, optional) - Free text: "Between 6-7", "6.5", "7-8 (slightly alkaline)"
- **Soil Fertility** (text input, optional) - Free text: "Yellow (Low)", "Red (Medium)", "Green (High)"

#### Growth Tracking
- **Current Stage** (text input, optional) - e.g., "Vegetative", "Flowering"
- **Next Stage** (text input, optional) - e.g., "Fruit development"

#### Observations & Actions
- **Observations** (textarea, required) - What you observed
- **Actions Taken** (textarea, markdown support, optional) - What you did
- **Notes** (textarea, optional) - Additional notes

#### Plant-Specific Q&A (Optional)
**Repeatable** - Can add multiple Q&A pairs per plant

Each Q&A pair:
- **Question** (text input)
- **Answer** (textarea)

**Button:**
- [+ Add Another Q&A]

#### Photos

**Photo Selection:**
- [Browse Photos from Google Drive folder]
- Shows thumbnails of selected photos
- Can select multiple photos

**For each selected photo:**
- **Auto-suggested Filename** (display/editable) - `plant_id_YYYYMMDD_HHMM_seq.jpg` based on EXIF
- **Caption** (text input, optional)
- **Tags** (text input, optional) - e.g., "before_pruning", "closeup"
- [Remove Photo] button

**Photo Processing:**
- Extract EXIF metadata (date/time) from JPEG
- Compress to 600×450px @ 85-90% quality
- Rename according to convention
- Copy to `photos/` folder
- Leave original in Google Drive folder

**Button:**
- [+ Add Another Plant Observation]

---

### Form Submission Buttons

- **[Save Entry & Generate Journal]** - Saves to JSON and triggers HTML generator
- **[Cancel]**

---

## Success Modal (All Forms)

After successful form submission, display modal alert:

```
┌──────────────────────────────────────────┐
│  ✓ [Action] Successful!                  │
├──────────────────────────────────────────┤
│  [Summary of what was added/changed]     │
│  • Item 1                                │
│  • Item 2                                │
│  • Item 3                                │
│                                          │
│  [View Journal] [Add Another] [OK]       │
└──────────────────────────────────────────┘
```

**Buttons:**
- **View Journal** - Opens generated HTML page for that entry
- **Add Another** - Clears form to add more (for daily entry/plant)
- **OK** - Closes modal, stays on form

**Examples:**

### Daily Entry Success:
```
✓ Daily Entry Added Successfully!

Date: November 13, 2025
Plants Observed: 3
 • Basil - Left
 • Strawberry - Right
 • Tomato
Photos Added: 5

[View Journal] [Add Another Entry] [OK]
```

### Add Plant Success:
```
✓ Plant Added Successfully!

Plant: Basil - Center (basil_003)
Location: Panel 5
Container: Basil Pot - Center

[View Plant Summary] [Add Another Plant] [OK]
```

### Move Plant Success:
```
✓ Plant Moved Successfully!

Plant: Basil - Left (basil_001)
From: Panel 1
To: Panel 14
Reason: Better afternoon sun

[View Plant Summary] [OK]
```

---

## Backend Integration

### Flask Routes

**Static Routes:**
- `GET /` → Render index.html (landing page)
- `GET /add-plant` → Render add_plant.html
- `GET /add-entry` → Render add_entry.html
- `GET /move-plant` → Render move_plant.html

**API Routes:**
- `POST /api/add-plant` → Process form, call `data_manager.add_plant()`, return success JSON
- `POST /api/add-entry` → Process form, call `data_manager.add_daily_entry()`, return success JSON
- `POST /api/move-plant` → Process form, call `data_manager.move_plant()`, return success JSON
- `GET /api/plants` → Return list of all active plants for dropdowns
- `GET /api/plant/<plant_id>` → Return plant data including current summary
- `POST /api/generate-html` → Trigger `html_generator.py` to rebuild pages

**Photo Routes:**
- `POST /api/upload-photos` → Handle photo upload, compression, renaming
- `GET /api/photos/browse` → List photos in Google Drive folder

---

## File Structure

```
garden-journal/
├── forms/
│   ├── index.html              # Landing page
│   ├── add_plant.html          # Add plant form
│   ├── add_entry.html          # Daily entry form (big one)
│   ├── move_plant.html         # Move plant form
│   └── static/
│       ├── forms.css           # Form styling
│       └── forms.js            # JavaScript for interactivity
├── src/
│   └── web_server.py           # Flask application
└── [existing structure...]
```

---

## Styling Guidelines

### Form Styling
- Match existing garden journal color scheme:
  - Primary green: `#216e3a`
  - Muted: `#5f6b6b`
  - Borders: `#e6e8eb`
- Clean, minimal design
- Responsive layout (works on laptop/desktop)
- Clear labels and helpful placeholders
- Focus states for accessibility

### Photo Display in Forms
- Thumbnail grid: 3-4 photos wide
- Each thumbnail: ~150px square
- Click to select/deselect
- Selected photos have green border
- Show filename below thumbnail

---

## Markdown Conversion

### Supported Formats

**Bullets:**
```
- Top level bullet
   - Indented bullet (3 spaces + dash)
```

**Converts to:**
```html
<ul>
  <li>Top level bullet
    <ul>
      <li>Indented bullet</li>
    </ul>
  </li>
</ul>
```

**Applied to these fields:**
- Summary of Activities
- General Observations
- Actions Taken (in plant observations)

---

## Validation Requirements

### Client-side (JavaScript)
- Required fields marked with *
- Date/time format validation
- Plant ID uniqueness check (for add plant)
- Photo filename validation

### Server-side (Python)
- All validation from `schema.py`
- Duplicate plant_id check
- Date/time format validation
- Photo filename format validation
- JSON structure validation

---

## Error Handling

### Form Validation Errors
- Show inline error messages below fields
- Highlight invalid fields in red
- Don't allow form submission until valid

### Server Errors
- Show error modal with friendly message
- Log detailed error to console/logs
- Offer "Try Again" option

### Photo Upload Errors
- File too large: "Photo file size too large. Please use photos under 10MB."
- Invalid format: "Please select JPEG images only."
- Compression failed: "Failed to process photo. Please try a different file."

---

## Future Enhancements (Not in v1.0)

- Drag-and-drop photo upload
- Batch add multiple plants
- Edit existing entries
- Delete entries/plants
- Search/filter plants
- Calendar view of entries
- Export to PDF directly from form

---

## Testing Checklist

Before marking Priority 4 complete:

### Photo Workflow
- [ ] Can browse Google Drive folder path
- [ ] Can select multiple photos
- [ ] EXIF data extracted correctly
- [ ] Filenames auto-suggested accurately
- [ ] Photos compressed to target size
- [ ] Photos renamed correctly
- [ ] Photos copied to `photos/` folder
- [ ] Originals remain in Google Drive

### Add Plant Form
- [ ] All fields save correctly
- [ ] Plant ID generated properly
- [ ] Location history created
- [ ] Success modal displays
- [ ] Links to plant summary work

### Move Plant Form
- [ ] Plant dropdown loads active plants
- [ ] Location history updated
- [ ] Current location updated
- [ ] Success modal displays

### Daily Entry Form
- [ ] All 6 sections save correctly
- [ ] Markdown bullets convert properly
- [ ] Multiple plant observations work
- [ ] Multiple Q&A pairs work
- [ ] Plant summary loads and saves
- [ ] Photos attach to correct plant
- [ ] Success modal displays
- [ ] HTML generator triggered
- [ ] Generated HTML displays correctly

### Backend
- [ ] Flask server runs on localhost:5000
- [ ] All routes respond correctly
- [ ] data_manager functions called properly
- [ ] Backups created automatically
- [ ] Error handling works
- [ ] Logging in place

---

## Notes

- All forms use existing `data_manager.py` functions - no need to rewrite data logic
- Photo compression happens client-side (JavaScript) before upload to reduce server load
- Markdown parsing happens server-side when saving to JSON
- HTML generation triggered automatically after daily entry submission
- User always uses Chrome browser on macOS