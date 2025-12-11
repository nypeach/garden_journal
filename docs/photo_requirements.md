===============================================
# 🌿 Master Garden Photo Handling Requirements
_Last Updated: December 11, 2025 5:20 PM_
===============================================

## Overview

This document outlines the complete photo handling system for the Master Garden Dashboard. The system enables efficient photo management, compression, organization, and integration with ChatGPT plant channels for automated journal entry generation.

---

## 🎯 Problem Statement

### Current Workflow Gap
- User takes high-quality iPhone photos (large file sizes)
- User uploads photos to ChatGPT plant channels for analysis
- ChatGPT generates journal entries with photo metadata (captions, tags)
- ChatGPT cannot determine actual filenames during upload
- User cannot link physical photo files to their captions/tags without manual work

### Solution
Create an integrated photo management system that:
1. Standardizes photo naming conventions
2. Compresses images to reduce file size while maintaining quality
3. Organizes photos by plant in Google Drive
4. Provides ChatGPT with exact filenames for accurate journal entries
5. Displays photos in journal with lightbox capability
6. Allows backfilling of placeholder photos from past entries

---

## 📁 File Structure & Paths

### Google Drive Photo Storage
**Base Path:**
```
/Users/jodisilverman/Library/CloudStorage/GoogleDrive-jodimsilverman@gmail.com/My Drive/Garden Photos/
```

**Organized Subfolder Structure:**
```
Garden Photos/
├── basil_001/
│   ├── basil_001-20251211-01.jpeg
│   ├── basil_001-20251211-02.jpeg
│   └── basil_001-20251211-03.jpeg
├── strawberry_001/
│   ├── strawberry_001-20251209-01.jpeg
│   └── strawberry_001-20251209-02.jpeg
├── lavender_004/
└── ...
```

**Naming Convention:**
```
{plant_id}-{YYYYMMDD}-{##}.jpeg

Examples:
- basil_001-20251211-01.jpeg
- strawberry_001-20251209-15.jpeg
- lavender_004-20251130-03.jpeg
```

### Flask Photo Serving
**Route Pattern:**
```python
@app.route('/photos/<plant_id>/<filename>')
```

**Template Usage:**
```html
<img src="/photos/{{ plant_id }}/{{ photo.file_name }}">
```

---

## 🔧 Version 1: Photo Prep Tool

### Purpose
Prepare photos before sending to ChatGPT plant channels by renaming, compressing, organizing, and generating a formatted message with filenames.

### User Interface

**Route:** `/tools/photo-prep` or `/photo-prep`

**Form Fields:**
1. **File Upload** (required)
   - Multiple file selection allowed
   - Accepts: JPEG, PNG, HEIC
   - Supports 1-20+ photos

2. **Plant ID** (required)
   - Text input
   - Format: `plant_type_###` (e.g., `basil_001`, `strawberry_002`)
   - Used for subfolder creation and filename prefix

3. **Date** (required)
   - Date picker
   - Default: Today's date
   - Format: MM/DD/YYYY (displayed), YYYYMMDD (in filename)

4. **Starting Photo Number** (optional)
   - Number input
   - Default: 01 (if blank)
   - Allows continuation of photo sequences within same day
   - Zero-padded to 2 digits

5. **Context** (required)
   - Dropdown: "Initial" or "Follow-Up"
   - Informs message structure

6. **Message** (required)
   - Textarea (multi-line)
   - User provides weather conditions, observations, questions
   - Will be prepended to filename list in output

7. **Process Button**
   - Triggers photo processing workflow

### Processing Workflow

**Step 1: Validation**
- Verify plant_id is not empty
- Verify at least one photo uploaded
- Verify date is valid
- Calculate starting number (use 01 if blank)

**Step 2: Create Subfolder**
- Check if `{base_path}/{plant_id}/` exists
- Create subfolder if it doesn't exist

**Step 3: Process Each Photo**
For each uploaded photo (in order):

a. **Generate New Filename**
   - Pattern: `{plant_id}-{YYYYMMDD}-{##}.jpeg`
   - Number increments with each photo
   - Example: `basil_001-20251211-01.jpeg`

b. **Compress Image**
   - Use PIL/Pillow library
   - Target: Reduce file size while maintaining visual quality
   - Suggested settings:
     * JPEG quality: 85%
     * Optimize: True
     * Progressive: True
   - Maintain EXIF data if possible

c. **Save to Subfolder**
   - Write compressed image to: `{base_path}/{plant_id}/{new_filename}`
   - **MOVE files** (don't copy) - remove from temporary upload location

**Step 4: Generate Output**
Create formatted message in markdown code block:

```
{user's message text}

Here are the photo names:
1. {plant_id}-{YYYYMMDD}-01.jpeg
2. {plant_id}-{YYYYMMDD}-02.jpeg
3. {plant_id}-{YYYYMMDD}-03.jpeg
...
```

**Step 5: Display Output**
- Show output in copyable code block on page
- Provide success confirmation
- Show list of processed files
- Show destination folder path

### Example Usage

**Scenario 1: First Photos of the Day**
```
Files uploaded: 3 photos
Plant ID: basil_001
Date: 12/11/2025
Starting Photo #: [blank]
Context: Initial
Message: "Today 12/11/2025: Mostly Sunny with a high of 77°F dropping to 52°F overnight."

Result:
- Creates: /Garden Photos/basil_001/
- Renames & compresses:
  * basil_001-20251211-01.jpeg
  * basil_001-20251211-02.jpeg
  * basil_001-20251211-03.jpeg
```

**Scenario 2: Follow-Up Photos Same Day**
```
Files uploaded: 2 photos
Plant ID: basil_001
Date: 12/11/2025
Starting Photo #: 4
Context: Follow-Up
Message: "I added more soil and watered lightly."

Result:
- Uses existing: /Garden Photos/basil_001/
- Renames & compresses:
  * basil_001-20251211-04.jpeg
  * basil_001-20251211-05.jpeg
```

### Output Message Format

```markdown
Today 12/11/2025: Mostly Sunny with a high of 77°F dropping to 52°F overnight. Tonight: Mostly Clear. Tomorrow: Sunny with a high of 72°F.

I added soil back into the pot where the probe left a gap. I took a zoom of one of the leaves. Do you think I need to chop it off? Is it leaf spot?

Here are the photo names:
1. basil_001-20251211-01.jpeg
2. basil_001-20251211-02.jpeg
3. basil_001-20251211-03.jpeg
4. basil_001-20251211-04.jpeg
5. basil_001-20251211-05.jpeg
```

User copies this entire block and pastes into ChatGPT plant channel along with the photos.

---

## 🖼️ Version 2: Placeholder Upload & Lightbox

### Feature 1: Placeholder Photo Upload

**Purpose:**
Backfill photos for past journal entries that only have placeholders.

**Implementation:**

1. **Photo Placeholder Button**
   - When journal displays: `"file_name": "<<put filename here>>"`
   - Entire placeholder box becomes clickable upload button
   - Styled to look like interactive element (hover effect)
   - Text: "📷 Click to Upload Photo"

2. **Upload Behavior**
   - Click placeholder → Opens file picker
   - User selects single photo
   - System automatically:
     * Extracts plant_id from current journal
     * Extracts date from journal entry
     * Determines next available photo number for that date
     * Compresses image
     * Renames: `{plant_id}-{YYYYMMDD}-{##}.jpeg`
     * Moves to: `{base_path}/{plant_id}/`
     * Updates JSON file with actual filename
     * Refreshes display to show actual photo

3. **User Experience**
   - No form needed - all context is known
   - One click, one file selection, done
   - Immediate visual feedback (placeholder → actual photo)

### Feature 2: Photo Lightbox Modal

**Purpose:**
View full-size photos in journal without leaving the page.

**Implementation:**

1. **Thumbnail Display**
   - Current size: 180px thumbnails
   - Could reduce to 120-140px since expandable
   - Add visual indicator (magnifying glass icon on hover?)

2. **Lightbox Modal**
   - Click any photo thumbnail → Opens modal
   - Modal displays full-size image
   - Shows caption below image
   - Dark backdrop (like journal modal)
   - Close options:
     * ESC key
     * Click backdrop
     * X button in corner
   - Navigation (if multiple photos in entry):
     * Left/right arrows
     * Keyboard arrows

3. **Styling**
   - Reuse existing modal styles from journal modal
   - Center image, scale to fit viewport
   - Maintain aspect ratio
   - Smooth transitions

---

## 🔬 Image Compression Specifications

### Compression Goals
- **Reduce file size** from typical 3-5MB iPhone photos to ~200-500KB
- **Maintain visual quality** - No visible degradation in journal display
- **Preserve metadata** - Keep EXIF data where possible

### Compression Settings (PIL/Pillow)

```python
from PIL import Image

# Recommended settings:
image.save(
    output_path,
    'JPEG',
    quality=85,        # 85% quality (sweet spot for size/quality)
    optimize=True,     # Enable optimization
    progressive=True   # Progressive JPEG (better web loading)
)
```

### Quality Levels for Testing
- **90%** - Minimal compression, larger files (~800KB-1MB)
- **85%** - Recommended balance (~300-600KB)
- **80%** - More aggressive, still good quality (~200-400KB)
- **75%** - Maximum compression before visible quality loss

### File Format Support
- **Input:** JPEG, PNG, HEIC (if supported by PIL)
- **Output:** Always JPEG (best compression for photos)
- PNG photos will be converted to JPEG during compression

---

## 🧪 Testing Strategy

### Test Folder Setup
**Create test directory:**
```
/Users/jodisilverman/Library/CloudStorage/GoogleDrive-jodimsilverman@gmail.com/My Drive/Garden Photos TEST/
```

**During Development:**
- Use TEST folder for all photo processing
- Copy sample photos to test with (don't move originals)
- Test various compression levels
- Verify file sizes and visual quality
- Test subfolder creation
- Test file naming with various scenarios

**Before Production:**
- Switch path to production: `Garden Photos/`
- Test with 1-2 real photos first
- Verify Google Drive sync works correctly
- Confirm photos display in journal

### Test Scenarios

**Photo Prep Tool:**
1. ✓ Single photo upload
2. ✓ Multiple photos (5, 10, 20)
3. ✓ Default starting number (01)
4. ✓ Custom starting number (06, 15)
5. ✓ New plant_id (creates subfolder)
6. ✓ Existing plant_id (uses existing subfolder)
7. ✓ Backdated entry (past date)
8. ✓ Various photo formats (JPEG, PNG)
9. ✓ Large iPhone photos (3-5MB originals)
10. ✓ Output message format verification

**Placeholder Upload:**
1. ✓ Click placeholder → file picker opens
2. ✓ Upload replaces placeholder
3. ✓ Filename generated correctly
4. ✓ JSON updated automatically
5. ✓ Photo displays immediately

**Lightbox:**
1. ✓ Click thumbnail → modal opens
2. ✓ Full-size image displays
3. ✓ ESC key closes modal
4. ✓ Backdrop click closes modal
5. ✓ Caption displays correctly

---

## 🔗 Integration with ChatGPT Workflow

### Complete Workflow

**Step 1: Morning Photo Session**
- Take photos with iPhone
- Photos sync to Google Photos or local storage
- Photos are large (3-5MB each)

**Step 2: Photo Prep Tool**
- Open Flask app: `http://localhost:3000/photo-prep`
- Upload photos
- Fill in plant_id, date, message
- Click "Process"
- Copy generated message

**Step 3: ChatGPT Plant Channel**
- Open specific plant channel in ChatGPT
- Upload photos (in same order as prep tool)
- Paste message with filename list
- ChatGPT has complete context:
  * Weather conditions
  * Your observations
  * Exact filenames for each photo
  * Historical context from channel

**Step 4: ChatGPT Response**
- ChatGPT analyzes photos
- Provides care recommendations
- Generates JSON journal entry with:
  * Probe reading data
  * Observations
  * Actions
  * Next steps
  * Photos array with correct filenames, captions, tags

**Step 5: Save to Local System**
- Copy JSON from ChatGPT
- Prepend to plant's JSON file
- Photos already in correct location
- Journal displays photos automatically

### JSON Photo Array Structure

ChatGPT generates:
```json
"photos": [
  {
    "file_name": "basil_001-20251211-01.jpeg",
    "caption": "Top-down view showing healthy new growth and even canopy distribution.",
    "tags": "basil, top-view, healthy-growth, canopy"
  },
  {
    "file_name": "basil_001-20251211-02.jpeg",
    "caption": "Close-up of leaf showing suspected leaf spot damage on older foliage.",
    "tags": "basil, leaf-spot, close-up, damage, diagnostic"
  }
]
```

Flask serves photos from:
```
/photos/basil_001/basil_001-20251211-01.jpeg
```

---

## 🎨 UI/UX Considerations

### Photo Prep Tool Styling
- Match existing dashboard aesthetic
- Use unified `style.css`
- Form layout similar to dashboard cards
- Clear visual hierarchy
- Progress indicators during processing
- Success/error messages
- Copyable code block with syntax highlighting

### Placeholder Upload Button
- Clear visual indicator it's clickable
- Hover effects
- Dashed border (like current placeholder)
- Icon + text: "📷 Click to Upload Photo"
- Loading state while processing
- Smooth transition to actual photo

### Lightbox Modal
- Reuse existing modal styles
- Dark backdrop with slight blur
- Image centered and scaled
- Caption readable below image
- Smooth open/close animations
- Keyboard navigation support

---

## 📊 Success Metrics

### Functionality
- ✓ Photos renamed with consistent convention
- ✓ Files compressed to target size (~200-500KB)
- ✓ Photos organized in plant-specific subfolders
- ✓ ChatGPT receives accurate filename list
- ✓ Journal displays photos correctly
- ✓ Placeholder upload works seamlessly
- ✓ Lightbox modal enhances viewing experience

### User Experience
- ✓ Minimal clicks required
- ✓ No manual file renaming
- ✓ No manual photo organization
- ✓ Automated JSON population
- ✓ Photos accessible on phone via Google Drive
- ✓ Fast page load (compressed images)

### Technical
- ✓ Google Drive sync works correctly
- ✓ No duplicate files
- ✓ Flask serves photos efficiently
- ✓ JSON structure maintained
- ✓ No repo bloat (photos stay in Google Drive)

---

## 🚀 Implementation Phases

### Phase 5A: Photo Prep Tool (PRIORITY)
1. Create `/photo-prep` route and template
2. Implement file upload handling
3. Add PIL/Pillow image compression
4. Create subfolder organization logic
5. Generate formatted output message
6. Style form with unified CSS
7. Test compression levels
8. Test with various photo counts

### Phase 5B: Flask Photo Serving
1. Create `/photos/<plant_id>/<filename>` route
2. Update journal template to use new route
3. Test photo display in journal
4. Handle missing file errors gracefully

### Phase 5C: Placeholder Upload (Version 2)
1. Make placeholder clickable
2. Add file upload handler
3. Implement auto-naming logic
4. Update JSON file programmatically
5. Refresh journal display

### Phase 5D: Lightbox Modal (Version 2)
1. Create lightbox modal component
2. Make thumbnails clickable
3. Add navigation controls
4. Style with unified CSS
5. Add keyboard support

---

## 📝 Notes & Future Considerations

### Current Limitations
- User must manually paste JSON from ChatGPT
- No automated JSON updates (yet)
- No batch photo editing
- No photo deletion interface

### Future Enhancements
- Drag-and-drop photo upload
- Batch processing multiple plants
- Photo editing (crop, rotate, filters)
- Automatic EXIF data extraction
- Date/time from photo metadata
- Integration with ChatGPT API (if/when available)
- Photo search by tags
- Photo comparison (before/after views)

### Dependencies
- Flask
- PIL/Pillow (image processing)
- Jinja2 (templating)
- Standard library: os, pathlib, datetime

---

**End of Requirements Document**