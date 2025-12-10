===============================================
# 🌿 Master Garden AI Assistant Prompt
_Last Updated: December 10, 2025 3:05 PM_
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
- `webserver.py` - Flask server (NOT app.py)
- `data_manager.py` - JSON read/write operations
- `static/style.css` - Single CSS file for all pages
- `templates/*.html` - All HTML templates
- `data/` - JSON data files (plants, containers, products)
- `docs/schema.md` - Complete data schema documentation

---

## 🎯 Current Development Status

**Current Phase:** Phase 1 - Foundation Setup

### ✅ Completed
- Repository structure defined
- README.md created with full feature roadmap
- PROMPT.md created (this file)
- Project documentation established

### 🚧 In Progress
- Flask webserver setup
- data_manager.py implementation
- Base CSS creation

### 📋 Next Up
- Phase 2: Dynamic Master Dashboard

---

## 🗺️ Development Phases

### Phase 1: Foundation Setup
- [x] Repo structure
- [ ] Flask webserver
- [ ] Data manager
- [ ] Base CSS

### Phase 2: Dynamic Master Dashboard
- Load plant data from JSON files
- Display plants as tiles
- Show basic plant info
- Apply unified CSS

### Phase 3: Plant Detail Modal
- Click plant tile → modal overlay
- Display plant main data
- Display journal entries
- Show probe readings and observations

### Phase 4: GPT Integration Forms
- Update Plant Data Form (journal entries, fragments, complete data)
- Add Containers Form
- Add Products Form

### Phase 5: Photo Management System
- Photo upload interface
- Image compression and storage
- Photo display in journal

**See README.md for complete phase details and sub-tasks.**

---

## 🔑 Key Project Conventions

### Naming Conventions
- Use `webserver.py` (not `app.py`) for the Flask server
- Keep Python utility files in root (e.g., `data_manager.py`)
- Use descriptive, snake_case for Python files
- Use kebab-case for HTML files

### Code Organization
- Flask routes in `webserver.py`
- Data operations in `data_manager.py`
- Templates use Jinja2 for dynamic content
- Single `style.css` for all pages
- ChatGPT-related files in `chatgpt/` folder

### Data Structure
- Individual plant files: `data/plants/*.json`
- Shared data: `data/containers.json`, `data/products.json`, `data/meta.json`
- See `docs/schema.md` for complete data schema
- All dates: `M/D/YYYY` format
- All times: `H:MM AM/PM` format

### File Artifacts
- Always create code artifacts for files the user will copy
- Use appropriate language tags (markdown, json, python, html, css)
- Never use document artifacts for code/configuration files

---

## 📝 Git Commit Guidelines

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
git add -A && git commit -m "feat: Add Flask webserver with basic routes

- Set up Flask app in webserver.py
- Add home route for dashboard
- Add route for plant detail modal
- Configure template and static directories"
```

```bash
git add -A && git commit -m "docs: Update README with Phase 2 progress

- Mark dashboard tasks as complete
- Update current phase status
- Add next steps for Phase 3"
```

```bash
git add -A && git commit -m "fix: Correct JSON parsing in data_manager

- Handle empty plant files gracefully
- Add error logging for malformed JSON
- Return empty dict instead of None"
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
4. Commit the changes

---

**Remember:** This project values simplicity and clarity. Keep the codebase lean, maintainable, and well-documented. When in doubt, ask the user for clarification rather than making assumptions.