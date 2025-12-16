===============================================
# 🌿 Phase 5: Admin Dashboard - MVP Requirements
_Last Updated: December 16, 2025 4:29 AM_
===============================================

## 📋 Overview

Simple, focused admin dashboard for managing IF/THEN correction rules with search and filter capabilities.

**MVP Scope:**
- Single JSON file for all IF/THEN rules (`data/if-then-corrections.json`)
- Single search/filter page matching existing site style
- Basic view/search functionality
- Export to markdown for guide updates

___

## 🗒️ Notes

Every copy/paste output should have the following paragraph appended.

Acknowledge the correction with one brief sentence confirming you will follow this approach going forward, then immediately continue the workflow as my professional horticulturist or extension agent.
___

## 🎯 MVP Deliverables

### 1. JSON Data File

**File Location:** `data/if-then-corrections.json`

**JSON Schema:**
```json
{
  "schema_version": "1.0",
  "last_updated": "2025-12-15",
  "corrections": [
    {
      "id": "DW-ASSESSMENT-001",
      "title": "No Expert Assessment Provided",
      "category": "Daily Workflow",
      "sub_category": "Assessment order & depth",
      "severity": "critical",
      "status": "active",
      "frequency": "common",
      "count": 0,
      "date_added": "2025-12-15",
      "trigger_if": "The assistant gives me Plant Daily Journal Entry Data JSON before providing an Expert Assessment",
      "response_then": "Stop — give me your Expert Assessment FIRST (natural, conversational), then immediately re-send the Daily Journal Entry JSON.",
      "tags": ["assessment", "json", "workflow_order"],
      "scope": "Plant Channels",
      "applies_when": ["New Day"],
      "anti_patterns": [
        "Providing JSON code block before any assessment text",
        "Jumping straight to structured output"
      ],
      "notes": "This is the most common workflow violation",
      "related_rules": ["DW-ASSESSMENT-002", "DW-WORKFLOW-003"]
    }
  ]
}
```

**Field Definitions:**
- `count` (integer, default: 0): Number of times the THEN response has been copied. Auto-increments when user clicks the copy button. Used to surface most frequently used corrections.

**Categories & Subcategories** (from your images):

1. **Daily Workflow**
   - Assessment order & depth
   - Voice / tone
   - Workflow gating / unnecessary confirmation
   - Code block / formatting violations
   - Missing required inputs

2. **Daily Journal Entry JSON**
   - Schema / field names
   - Validity / formatting
   - Partial JSON outputs
   - Wrong field updates (changed unrelated fields)

3. **Photos & Evidence Handling**
   - Filename / order preservation
   - Probe screenshot vs plant photo classification
   - Caption accuracy
   - Hallucinated / external content

4. **Probe Readings**
   - Multiple screenshots logic (averaging/outliers/timestamps)
   - Required probe summary format compliance
   - Interpretation errors

5. **Follow-Ups**
   - Offer to log follow-up
   - Same-day vs new-day handling
   - Silent logging / logging without asking
   - Initial-message commentary incorrectly logged as follow_up

6. **Plant Main Data**
   - Review not performed
   - Lock-in / sequencing errors
   - Skipped attributes
   - Timeline / what_i_should_see
     - missing lifecycle coverage
     - missing intermediates
     - wrong dates
     - no consolidated proposal before confirmation
   - Premature Plant Main Data JSON

7. **Corrections Handling**
   - Acknowledged but not applied
   - Didn't resume from correct step
   - Saved-to-memory when it shouldn't

___

### 2. HTML Search Page

**File:** `templates/if-then-search.html`

**Layout:**
- Sticky header (matching dashboard.html style)
- Title: "🔍 IF/THEN Corrections Database"
- Subtitle: "Search and manage correction rules for the Master Garden Reset Channel"
- Nav chip: "← Back to Dashboard"

**Top 5 Most Used Section:**
- Card displaying "🔥 Top 5 Most Used Corrections"
- Shows 5 corrections with highest `count` value
- Each displays:
  - Title
  - Severity pill
  - Copy button (copies THEN text and increments count)
  - Usage count badge: "Used X times"
- Always visible above search section
- Updates in real-time when copy button clicked

**Search Section:**
- Text search bar (searches: id, title, trigger_if, response_then, tags, notes)
- Filter dropdowns:
  - Category (all 7 categories)
  - Sub-category (cascades from selected category)
  - Severity (critical, high, medium, low)
  - Status (active, deprecated, draft, needs_testing)
  - Scope (Master Channel, Plant Channels, Both)
- "Clear Filters" button
- Search results count: "Showing X of Y rules"

**Results Display:**
- Table with columns:
  - ID (clickable to expand detail)
  - Title
  - Category
  - Severity (colored pill badge)
  - Status (colored pill badge)
  - Count (usage badge: "X uses")
  - Actions (📋 Copy THEN button, 👁️ View Detail button)

**Copy Button Behavior:**
- Button icon: 📋 Copy
- On click:
  1. Copies `response_then` text to clipboard
  2. Sends POST to `/api/if-then-corrections/<id>/increment-count`
  3. Increments `count` field in JSON file
  4. Shows toast notification: "✅ Copied! (Used X times)"
  5. Updates count badge in UI
  6. Refreshes Top 5 section if needed

**Detail Card** (expandable when clicking row):
- Full IF condition
- Full THEN action
- All metadata (frequency, scope, applies_when)
- Anti-patterns list
- Related rules (clickable links to other rules)
- Notes section
- Tags
- "Export to Markdown" button (exports this single rule)

___

### 3. Flask Routes

**File:** `app.py`

**New Routes:**

```python
@app.route('/if-then-search')
def if_then_search():
    """IF/THEN corrections search page"""
    corrections = load_if_then_corrections()
    top_5 = get_top_5_corrections(corrections)
    return render_template('if_then_search.html',
                         corrections=corrections,
                         top_5=top_5,
                         categories=get_categories())

@app.route('/api/if-then-corrections')
def api_if_then_corrections():
    """API endpoint for filtered corrections"""
    category = request.args.get('category')
    sub_category = request.args.get('sub_category')
    severity = request.args.get('severity')
    status = request.args.get('status')
    scope = request.args.get('scope')
    search_query = request.args.get('q')

    corrections = filter_corrections(
        category=category,
        sub_category=sub_category,
        severity=severity,
        status=status,
        scope=scope,
        search_query=search_query
    )
    return jsonify(corrections)

@app.route('/api/if-then-corrections/<correction_id>/increment-count', methods=['POST'])
def increment_correction_count(correction_id):
    """Increment the count for a correction when THEN is copied"""
    success = increment_count(correction_id)
    if success:
        correction = get_correction_by_id(correction_id)
        return jsonify({
            'success': True,
            'count': correction['count'],
            'message': f"Copied! (Used {correction['count']} times)"
        })
    return jsonify({'success': False, 'message': 'Error updating count'}), 400
```

___

### 4. Data Manager Functions

**File:** `data_manager.py`

**New Functions:**

```python
def load_if_then_corrections():
    """Load all IF/THEN corrections from JSON file"""
    # Load data/if-then-corrections.json
    # Return list of correction dicts

def filter_corrections(**filters):
    """Filter corrections based on provided criteria"""
    # Apply filters
    # Return filtered list

def get_categories():
    """Get list of all categories and subcategories"""
    # Return category structure for dropdowns

def get_top_5_corrections(corrections):
    """Get top 5 corrections by count"""
    # Sort by count descending
    # Return top 5

def increment_count(correction_id):
    """Increment the count for a correction"""
    # Load JSON file
    # Find correction by ID
    # Increment count field
    # Save JSON file
    # Return True if successful

def get_correction_by_id(correction_id):
    """Get single correction by ID"""
    # Load JSON file
    # Find and return correction dict

def export_correction_to_markdown(correction_id):
    """Export single correction as markdown"""
    # Format as markdown IF/THEN block
    # Return markdown string
```

___

### 5. CSS Updates

**File:** `static/style.css`

**New Styles:**
- `.top-5-card` - card for top 5 most used corrections
- `.top-5-item` - individual correction in top 5 list
- `.copy-button` - copy THEN button styling
- `.usage-badge` - count display badge
- `.toast-notification` - success message on copy
- `.search-container` - search bar styling
- `.filter-row` - filter dropdown row
- `.results-table` - corrections table styling
- `.severity-pill` - colored badges for severity levels
- `.status-pill` - colored badges for status
- `.detail-card` - expanded detail view
- `.tag-list` - tag display styling

___

## 📝 Implementation Steps

1. **Convert IF/THEN statements to JSON**
   - Parse existing markdown IF/THEN blocks
   - Map to JSON schema
   - Assign IDs, categories, subcategories
   - Add all metadata fields

2. **Create HTML search page**
   - Match existing dashboard.html structure
   - Use same header/nav pattern
   - Table for results display
   - Expandable detail cards

3. **Add Flask routes**
   - Main search page route
   - API endpoint for filtering

4. **Add data_manager functions**
   - Load JSON
   - Filter/search logic
   - Export functions

5. **Style with existing CSS**
   - Reuse nav-link, pill, card classes
   - Add minimal new styles for table

___

## 🎨 Visual Reference

**Severity Pills:**
- 🔴 Critical (red)
- 🟠 High (orange)
- 🟡 Medium (yellow)
- 🟢 Low (green)

**Status Pills:**
- ✅ Active (green)
- 📝 Draft (gray)
- ⚠️ Needs Testing (orange)
- ❌ Deprecated (red)

___

## 📤 Export Feature

**Export Single Rule to Markdown:**
```markdown
**[Title]**

   **IF**
   [trigger_if text]

   **THEN**
   [response_then text]

___
```

**Export All Active Rules to Markdown:**
- Groups by category
- Preserves existing guide structure
- Only includes status="active"
- Ready to paste into guide

___

## 🔮 Optional Future Enhancements

**Phase 5.1 - Nice to Have:**
- Edit/Create form for adding new rules
- Bulk actions (activate/deprecate multiple)
- Version history tracking
- Import from JSON file
- Advanced search (regex, fuzzy matching)
- Saved search presets
- Related rules visualization
- Usage statistics (how often rules are triggered)

**Phase 5.2 - Advanced:**
- Reset Notes editor
- Dashboard order drag-and-drop
- Containers/Products forms
- Add new plant wizard

___

## ✅ Acceptance Criteria

MVP is complete when:
- [ ] All existing IF/THEN statements converted to JSON with `count: 0`
- [ ] Top 5 most used corrections displayed at top of page
- [ ] Copy button copies THEN text to clipboard
- [ ] Copy button increments count in JSON file
- [ ] Count badge updates in UI after copy
- [ ] Toast notification shows on successful copy
- [ ] Search page displays all rules
- [ ] Text search works across all fields
- [ ] Filters work (category, severity, status, scope)
- [ ] Detail cards expand/collapse
- [ ] Export single rule to markdown works
- [ ] Page matches existing site styling
- [ ] Responsive on mobile

___

## 🚀 Next Steps After MVP

1. Get user feedback on search/filter functionality
2. Identify most-needed enhancements
3. Add edit/create forms if needed
4. Consider bulk operations
5. Add analytics (which rules are most common)