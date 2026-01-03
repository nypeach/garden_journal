## Recommendation (based on how Projects + the GitHub connector actually behave)

**Use a hybrid model:**
- ✅ **Repo = canonical source of truth for guides**
- ✅ **Project = short “operating layer” + links/paths to the canonical repo guides**
- ✅ **When you change guides in repo, you periodically refresh the Project copy of the *short* operating layer (not the whole guide)**

This gives you the best of both worlds:
- the guides evolve with your daily commits
- the Project stays stable + prevents drift in behavior
- you avoid constantly copy/pasting 5,000+ lines into Project instructions

---

# Why NOT “repo-only” for guides

Even though I *can* search the GitHub repo when you ask, there are two practical constraints:

1) **The assistant won’t automatically fetch updated guides from the repo unless it is explicitly told to.**
   The model does not constantly pull from GitHub in the background.

2) **Indexing lag can cause behavior drift.**
   If you change a guide today and ask me to follow it immediately, the connector may still be referencing yesterday’s version until it refreshes.

So if the project instructions *only* say “use the guide in the repo,” you may get:
- inconsistent execution on days when the connector hasn’t caught up yet
- the assistant applying older rules

---

# Why NOT “project-only” for guides

If the Project contains the full long guide and becomes the canonical source:
- it becomes annoying to maintain
- you’ll start making changes in the repo and forget to update the project
- eventually the repo and project versions diverge

Then the assistant will do the wrong thing because the Project instructions will win.

---

# The sweet spot: Repo Canonical + Project Operating Layer

## ✅ Repo contains:
- **Full Master Garden Assistant Guide**
- **All plant schema + examples**
- **All operating guides / workflows / edge cases**
- **All plant JSON + auxiliary data files**
- **All “assistant behavior documents” as markdown**

This is your “source code.”

## ✅ Project contains:
A *short* but authoritative summary that:
1. Defines Plant Channels
2. Defines rule priority and what counts as authoritative
3. Tells the assistant exactly *when* to read the repo guide
4. Encodes the key “never hallucinate / only use user inputs” requirements
5. Encodes your formatting requirements (probe summary format, daily JSON schema, etc.)
6. States how to handle updates (“If repo guide conflicts with project, project wins” — or vice versa, depending on your preference)

Think of Project instructions as your “runtime config.”

---

# How to make repo guides work seamlessly inside Projects

### Pattern that works extremely well

**Project instructions say:**
- “The canonical guide lives in the repo at `docs/master_garden_assistant.md`”
- “At the start of each plant channel, load the most recent guide from that path and treat it as authoritative”
- “If there is any conflict between what’s in this thread and the repo guide, the thread wins (or the project wins — whichever you choose)”
- “If the repo guide cannot be accessed (sync lag), fall back to the copy embedded in Project artifacts”

So you always have:
- an authoritative canonical guide (repo)
- a fail-safe fallback copy (project)
- a deterministic conflict-resolution system

---

# The most practical workflow for you (minimal friction)

## 1) Store guides in repo
Put them in something like:
- `docs/plant_channels/`
  - `master_guide.md`
  - `project_operating_instructions.md`
  - `schema_daily_entry.md`
  - `probe_reading_format.md`
  - `special_circumstances.md`

## 2) Copy only **one** short file into Project artifacts
Copy the single file:
- `project_operating_instructions.md`

That file is your *compact* summary the assistant always sees.

## 3) Keep “full guide” repo-only
The long document stays in GitHub.
The project operating instructions tell the assistant:
- what file path to use
- to consult it when needed
- to treat it as canonical for details

This avoids stuffing the entire guide into Project instructions while still keeping the assistant aligned.

---

# Handling your daily guide updates (important)

Since you update daily, I recommend this:

✅ **The repo is always canonical**
✅ The Project operating instructions are **stable** (only updated when behavior changes materially)

Then if you change something big in the repo:
- you also update the *short Project operating layer* to point to the new version (or to note the change)
- optionally bump a version number inside the operating layer:
  - `Guide Version: 2026-01-03`

This prevents “silent drift.”

---

# Answering your specific question

### “Do you recommend guides be copied into the project as markdown files or referenced in GitHub?”

**Yes — copy the *short operating layer* into Project artifacts.**
**Reference the full guides from GitHub as canonical.**

This gives:
- ✅ stability (project always has the summary)
- ✅ scalability (repo holds all depth)
- ✅ speed (assistant doesn’t need to search repo every turn)
- ✅ resilience (if GitHub indexing lags, project still works)

---

# The one exception (when you *should* copy the full guide into the project)

If you are about to:
- rely on the assistant when you’re offline
- run many new plant channels quickly
- depend on zero failure tolerance for formatting and schema compliance

Then copying the full guide into project artifacts can be worth it.

But for your normal workflow (daily commits, constant iteration), the hybrid model is much better.

---

# My suggested final “rules of authority” hierarchy (simple + predictable)

1) **System messages** (OpenAI platform rules)
2) **Project Instructions** (short operating layer)
3) **Plant Channel “init message”** (the one you paste at start of each plant thread)
4) **Repo guides** (canonical for deep detail)
5) **Conversation context** (daily readings, photos, your corrections)
6) **Memory** (lowest priority; should never override project/channel rules)

This makes your system deterministic.

---

If you want, I can draft:
- a **short** `project_operating_instructions.md` you can drop into the repo
- the matching **Project Instructions** text that references it
- and a standard pattern you can paste into every Plant Channel that automatically tells the assistant where to load the guide from in your repo
