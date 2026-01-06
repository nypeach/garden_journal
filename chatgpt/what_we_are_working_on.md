# 🌿 Master Garden Project — Thread Memory (Working Summary)
_Last Updated: January 5, 2026_

This document is a structured summary of what I remember from the start of this thread:
**what we are building, why, what has been accomplished, and what is left to do.**
(**Not saved to memory — this is just a working artifact.**)

---

## 1) What This Thread Is Fundamentally About

This thread is about rebuilding your entire **Master Garden system** into a **Project + Repo + Modes architecture** that:

- preserves the best part of ChatGPT (a real **professional horticulturist / extension agent** vibe)
- while still producing deterministic, backend-friendly outputs (especially JSON)
- without drift, hallucinated structure, missing fields, or inconsistent formatting

### The core design principle (the thing we’re protecting)

✅ **We are NOT trying to remove the assistant’s freedom.**
That approach destroys the most important part of the system: the assistant’s ability to sound and think like a real horticultural expert.

Instead, the goal is:

✅ **Determinism only at the seams** (where drift happens)
while preserving **maximum freedom in the expert narrative layer** (where ChatGPT is strongest).

That means:

- **Conversation layer = free**
  - rich horticultural reasoning
  - explanations, nuance, teaching
  - emoji / warmth / extension-agent voice
  - flexible, human output

- **Data layer = strict**
  - mode detection must be deterministic
  - schemas must be followed exactly
  - filenames and ordering must not be guessed
  - “what fields can change” must be explicit
  - JSON must always be crisp, backend-friendly, and consistent

### Why MODES are the unlock

MODES let you enforce strict rules only where they matter (the data layer),
without forcing the assistant into robotic compliance everywhere else.

So the real goal is:

✅ **Keep the horticulturalist expert alive**
while still guaranteeing:

- deterministic JSON output
- reliable recovery behavior
- minimal drift across plant channels

---

The system goal is:

✅ **Small prompts + strict structure + reliable recovery**
instead of giant guides that overload context and cause resets.

You are transforming an old ~166k “Master Guide” into:
- multiple **MODE-specific guides**
- stored in your GitHub repo
- referenced by your Project (so they’re stable and versioned)
- and eventually unified through **Project Instructions** once the guide ecosystem exists


---

## 2) Key Design Principles We’re Using (The “Rules of Reality”)

### 2.1 Drift-first systems thinking (my role)
In this thread, I am not the horticulture expert.
I am your **ChatGPT systems + workflow expert**, focusing on:
- how Projects actually behave
- how Memory works inside/outside projects
- how connectors (GitHub) sync/index and what can go wrong
- how assistants drift and misread authority
- how to create deterministic behavior even with lag/staleness/ambiguity

### 2.2 Your role
You are building the guide ecosystem first.
We refine together after artifacts exist.

### 2.3 Why Modes matter
Modes exist because:
- even with rules, assistants blend behaviors and confuse intent
- follow-ups get treated as new day entries
- plant main data review is forgotten or done wrong
- assistant loses the beginning of the workflow by the time it reaches later steps
- user observations get incorrectly turned into Q&A summaries

Modes force:
- smaller prompts
- smaller guide context
- scoped instructions
- predictable flow

---

## 3) The Architecture We Are Building

### 3.1 Repo as the source of truth for artifacts
- plant JSON files live in the repo
- inventory JSON and guides live in the repo
- schema docs live in the repo but are scoped to editing/maintenance contexts

### 3.2 Project ties it together
The Project:
- contains the instructions that define how the system operates
- uses synced repo files as authoritative artifacts
- creates a stable environment so you don’t re-paste large content constantly

### 3.3 Front-end is the “control plane”
Your app/front-end:
- generates deterministic prompts
- selects modes
- injects exactly what the assistant should review
- provides checklists of fields, current values, filenames, etc.
- reduces drift by preventing interpretation

This is the backbone of the entire system:
**Workflow engineering > prompt engineering**

---

## 4) What We Have Already Done (Accomplishments)

### 4.1 Inventory system was created + reviewed
You created in the repo:
- `chatgpt/inventory_first_guide.md`
- `data/inventory.json`
- `docs/inventory_schema.md`

We analyzed and resolved major drift risks:
- manufacturer instructions output needed an extraction rule
- schema mismatch (`product_amount` vs `concentrate`) was fixed
- inventory-first rule clarified (inventory FIRST, not ONLY)
- missing inventory fallback behavior added (“No product fits” → recommend substitute + exact measurements)
- we established that examples + constrained outputs are the best drift guardrails

### 4.2 We invented and validated the “Guide Analysis Mode / Topic Mode / Regular Mode” workflow
We discovered the best workflow between you and me is:

**Guide Analysis Mode**
- I can go nuts with analysis
- I then must provide a markdown with everything itemized

**Topic Mode**
- you drive one topic at a time
- I answer exactly per your instructions
- prevents context collapse / drift

**Regular Mode**
- freer discussion of mechanics and system design

This became the model for how we will build the guide ecosystem.

### 4.3 We designed and finalized PMD Mode guide
We designed **Plant Main Data Review Mode** based on the key insight:

- assistant should NOT autonomously review PMD after every New Day entry
- assistant naturally prompts for PMD updates when in expert horticulture mode
- PMD should therefore be user-triggered via **PMD Mode prompt**

We created and refined:
✅ `🌿 Master Garden Plant Main Data Review Guide` (under 200 lines)

Key features:
- prompt is the source of truth
- user provides checklist + current values
- assistant reviews one attribute at a time
- assistant proposes updates in quote blocks
- locked text becomes immutable until explicitly changed
- only outputs JSON fragment of updated fields after confirmation
- attribute-by-attribute rules contain **good vs bad examples** because examples are what actually works

We refined field-specific rules for:
- `whats_been_logged`
- `current_stage` (phenological stage, not visual description)
- `current_state` (present-tense visible condition only)
- `timeline` (user-observable milestones, not scientific phase language)

---

## 5) What Problems We Are Solving (from assist-corrections + history)

Patterns we have repeatedly fought:
- assistant treats follow-up as new day
- assistant re-runs entire workflow unnecessarily
- assistant breaks JSON schema
- assistant invents fields or values
- assistant puts probe screenshots into photos array
- assistant invents follow-up entries or future events
- assistant writes “User asked…” in `q_and_a_summary`
- assistant forgets PMD review or does it wrong
- assistant loses base JSON in context
- assistant produces huge multi-section assessments that aren’t usable

Core stability wins discovered so far:
- the best failure mode is: “I can’t see the base JSON — paste it”
- the front-end prompt structure prevents most failures
- examples prevent narrative-field drift better than rules alone
- minimizing context load prevents workflow resets

---

## 6) The Modes We Know We Need (and why)

### Mode 1: New Day Mode
- ingest weather + probe readings + photos
- evaluate readings at time taken
- give care instructions for 6:00 AM the next day
- incorporate plant history + garden location + weather forecast
- output Daily Journal Entry JSON correctly

This mode must solve:
- inconsistent assessment formatting
- overly verbose multi-section analysis
- incorrect Q&A summarization
- missing or malformed JSON
- inability to anchor daily entry as the authoritative record

### Mode 2: Follow-Up Mode
- append to today’s entry only
- do NOT restart workflow
- re-issue complete updated Daily Journal Entry JSON
- only update `follow_up`, `q_and_a_summary` if a real question exists, photos if provided

This mode must solve:
- assistant restarting assessment
- assistant editing wrong fields
- assistant inventing new schemas or entries
- assistant losing the base entry

### Mode 3: Plant Main Data Review Mode (PMD Mode)
✅ we have this guide now
- checklist driven
- one attribute at a time
- quote-block proposals
- locked text
- final JSON fragment

_**Note we must adjust the front end prompts**_
---

## 7) The Biggest Remaining Concern We Are Actively Designing Around

You do NOT want:
- robotic assistants
- deterministic output that kills the horticulturist vibe
- overly strict rules that destroy the “extension agent” tone

You DO want:
- strong horticultural narrative + voice
- but disciplined, correct JSON + field compliance underneath

So we are building a system where:
- **Modes constrain structure**
- but inside the narrative portions, the assistant still feels human and expert

---

## 8) What Is Left To Accomplish (Next Steps)

### 8.1 Build the remaining MODE guides
We still need to create and review:

1. **New Day Mode Guide**
   - main workflow guide
   - rules for assessment + required output formats
   - rules for `actions` fields and exact measurements
   - rules for photos array and captioning
   - rules for Q&A summary style (horticulturist voice)

2. **Follow-Up Mode Guide**
   - append-only behavior
   - re-issue complete Daily Journal Entry JSON
   - strict rules for not restarting
   - clear “ask for the base JSON” failure mode

3. **Plant Main Data Review Mode Guide**
   - ✅ completed (but may still evolve with usage)

### 8.2 Integrate inventory-first logic into New Day Mode
Now that inventory is stable, New Day Mode must:
- reference `inventory.json`
- follow inventory-first guide behavior
- enforce exact dosing fields for any action involving products

### 8.3 Incorporate assist-corrections.json patterns into each Mode
Instead of “corrections after the fact,” we want:
- the mode prompts and guides to prevent the drift upfront

### 8.4 Design the project instruction hierarchy
Only after all mode guides exist:
- create final **Project Instructions**
- define source-of-truth hierarchy:
  - project instructions > mode prompts > repo guides > repo schema docs
- define how assistant should behave if repo lookup fails
- define “don’t save to memory unless explicitly asked”
- define how to keep the expert horticulturist vibe while staying deterministic

---

## 9) Final Output Goal (What Success Looks Like)

For any plant channel, you want this experience:

- you send weather + probe readings + photos + timestamp
- assistant responds like a real horticulturist:
  - calm
  - expert
  - narrative
  - observant
  - context-aware
- but also outputs:
  - correct, consistent JSON
  - correct actions with exact measurements
  - no schema drift
  - no invented values
  - no “User asked” language
  - no workflow resets
  - and no need for you to paste huge schemas or guides repeatedly

---

## 10) What We’re Working On Right Now (Current State)

Right now we have:
- inventory artifacts + guide stabilized
- PMD Mode guide stabilized
- the interaction model between you and me stabilized (analysis/topic/regular)
- the next major target is:
  ✅ **New Day Mode**
  ✅ **Follow-Up Mode**
  ✅ then final Project Instructions

---
