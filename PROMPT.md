===============================================
# 🌿 Master Garden AI Assistant Prompt
_Last Updated: December 11, 2025 5:20 PM_
===============================================

## Purpose

This file maintains context for AI assistants working on the **Garden Journal** project. If development spans multiple sessions or reaches token limits, this file helps new AI instances understand:

- The project's current state and progress
- What has been completed
- What is currently being worked on
- What comes next in the development roadmap
- Key conventions and practices to follow

**Read this file first** before beginning any work on the project to ensure continuity and consistency.

---

## 🚨 Critical Instructions

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

### Key Files
- `app.py` - Flask server with dashboard and journal routes
- `data_manager.py` - JSON read/write operations
- `static/style.css` - Single unified CSS file for all pages
- `static/modal.js` - Modal interaction JavaScript
- `templates/dashboard.html` - Master garden dashboard template
- `templates/journal.html` - Dynamic plant journal template
- `data/` - JSON data files (plants, containers, products, dashboard_order)
- `docs/schema.md` - Complete data schema documentation
- `docs/photo_requirements.md` - Photo handling system requirements and workflow

---

## 🎯 Current Development Status

**Current Phase:** Phase 5 - Photo Management System 🚧 **IN PROGRESS**

### ✅ Completed
- Phase 1: Foundation Setup (complete)
- Phase 2: Dynamic Master Dashboard (complete)
  - Bonus: Category grouping with dashboard_order.json
  - Bonus: Navigation chips with emojis
  - Bonus: Parent category ordering
- **Phase 3: Plant Detail Modal (complete)**
  - Modal overlay with iframe for journal display
  - Dynamic journal template with plant-specific data
  - Journal header with pill and current state
  - Complete journal entry display (probes, observations, actions, photos)
  - Modal interaction (ESC to close, click backdrop to close)
  - Photo grid with consistent sizing and captions

### 🚧 In Progress
- **Phase 5: Photo Management System**
  - Photo Prep Tool (Version 1)
  - Google Drive integration for photo serving
  - Placeholder photo upload (Version 2)
  - Photo lightbox modal (Version 2)

### 📋 Next Up
- Phase 4: GPT Integration Forms (deferred)
  - Update Plant Data Form
  - Add Containers Form
  - Add Products Form

---

## 🗺️ Development Phases

### Phase 1: Foundation Setup (COMPLETE)
- [x] Repo structure
- [x] Flask webserver (`app.py`)
- [x] Data manager (`data_manager.py`)
- [x] Base CSS (`style.css`)
- [x] Requirements file

### Phase 2: Dynamic Master Dashboard (COMPLETE)
- [x] Load plant data from JSON files
- [x] Display plants as tiles
- [x] Show basic plant info
- [x] Apply unified CSS
- [x] Category grouping (dashboard_order.json)
- [x] Navigation with emojis

### Phase 3: Plant Detail Modal (COMPLETE)
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

### Phase 4: GPT Integration Forms (DEFERRED)
- [ ] Update Plant Data Form (journal entries, fragments, complete data)
- [ ] Add Containers Form
- [ ] Add Products Form

### Phase 5: Photo Management System (IN PROGRESS)
- [ ] **Photo Prep Tool (Version 1 - Priority)**
  - [ ] Create `/photo-prep` route and form
  - [ ] File upload handling (multiple files)
  - [ ] PIL/Pillow image compression (~85% quality)
  - [ ] Automated file renaming: `{plant_id}-{YYYYMMDD}-{##}.jpeg`
  - [ ] Subfolder organization by plant_id
  - [ ] Generate formatted ChatGPT message with filenames
  - [ ] Display output in copyable code block
- [ ] **Google Drive Photo Integration**
  - [ ] Create `/photos/<plant_id>/<filename>` route
  - [ ] Serve photos from Google Drive folder
  - [ ] Update journal template to use new photo route
  - [ ] Photos organized in plant-specific subfolders
- [ ] **Placeholder Photo Upload (Version 2)**
  - [ ] Make placeholder boxes clickable
  - [ ] Single photo upload on click
  - [ ] Auto-determine filename from context
  - [ ] Compress and move to correct subfolder
  - [ ] Update JSON with actual filename
  - [ ] Refresh display to show photo
- [ ] **Photo Lightbox Modal (Version 2)**
  - [ ] Create lightbox modal component
  - [ ] Make thumbnails clickable
  - [ ] Display full-size image
  - [ ] Navigation controls (keyboard, arrows)
  - [ ] Show caption below image

**See `docs/photo_requirements.md` for complete specifications.**

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

### Data Structure
- Individual plant files: `data/plants/*.json`
- Shared data: `data/containers.json`, `data/products.json`, `data/meta.json`
- Dashboard ordering: `data/dashboard_order.json`
- See `docs/schema.md` for complete data schema
- All dates: `M/D/YYYY` format
- All times: `H:MM AM/PM` format

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

Example topics:
- Master Garden Dashboard (README.md)
- Master Garden AI Assistant Prompt (PROMPT.md)
- Master Garden Data Schema (schema.md)

---

## 📝 Git Commit Guidelines

### Pre-Commit Review Process

**CRITICAL:** Before every commit, ALWAYS review and update:
1. **PROMPT.md** - Update status, phases, and timestamp
2. **README.md** - Update progress, features, and timestamp

This ensures documentation stays in sync with code changes.

### When to Suggest a Commit

Suggest a commit when:

1. **Feature completion** - A complete feature or sub-task is finished and working
2. **Logical checkpoint** - A meaningful unit of work is complete (e.g., "add data_manager.py with all CRUD functions")
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

**Examples:**
```bash
git add -A && git commit -m "feat: Add plant journal modal with dynamic content

- Create journal.html template with Jinja2
- Add /journal/<plant_id> route to app.py
- Implement modal overlay with iframe
- Add modal.js for interaction handling
- Display journal entries with probes and photos"
```

```bash
git add -A && git commit -m "docs: Update PROMPT.md and README.md for Phase 3 completion

- Mark Phase 3 tasks as complete
- Update current phase status
- Add next steps for Phase 4"
```

```bash
git add -A && git commit -m "style: Refine journal header and photo grid styling

- Add negative margins for compact header layout
- Update photo grid padding and caption sizing
- Adjust journal entry horizontal padding"
```

### Commit Command Template

**Always provide the commit as a single copyable command:**

```bash
git add -A && git commit -m "type: Brief description

- Bullet point of what changed
- Another change
- Another change"
```

The user will copy and paste this directly into their terminal.

---

## 💬 Communication Style

- Be concise and technical when appropriate
- Explain decisions and trade-offs
- Ask clarifying questions when requirements are ambiguous
- Suggest improvements but respect user's preferences
- Keep it lean and simple (project philosophy)
- Proactively suggest commits at logical checkpoints

---

## 📚 Additional Resources

- **Data Schema:** See `docs/schema.md` for complete JSON structure
- **Features:** See README.md Features section for all phases
- **ChatGPT Integration:** See `chatgpt/` folder for plant channel templates
- **Project Structure:** See README.md for complete folder tree

---

## 🔄 Updating This File

When significant progress is made:

1. Update "Current Development Status" section
2. Check off completed tasks in "Development Phases"
3. Update the "Last Updated" timestamp at the top
4. Review and update any relevant conventions or guidelines
5. Commit the changes with proper documentation updates

---

**Remember:** This project values simplicity and clarity. Keep the codebase lean, maintainable, and well-documented. When in doubt, ask the user for clarification rather than making assumptions.