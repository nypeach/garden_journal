===============================================
# 🌿 Master Garden Reset Channel User Guide
_Last Updated: December 13, 2025 7:40 PM_
===============================================

## 🎯 Purpose 🌱

This channel exists as a **reset, correction, and refinement workspace** for your garden system.

Use this channel when:
- A Plant Channel assistant behaves incorrectly or drifts from the guide
- You want to determine whether an issue is already covered by an existing rule
- You need to add a new IF/THEN correction or micro-update
- You want exact wording to correct a Plant Channel assistant
- You want reassurance that a problem is fixed and won’t recur

This channel is **not** for daily plant care.
It is for **maintaining the system** that supports daily plant care.

___

## 🧭 Workflow 🔧

When something goes wrong in a Plant Channel:

1. **Do not argue with the Plant Channel assistant**
2. **Do not ask why it failed or explain the guide**
3. **Do not immediately modify the guide**

Instead:

- Come to this Reset Channel
- Describe what happened and what you expected
- Let this channel determine whether:
  - The issue is already covered
  - A new IF/THEN is needed
  - A micro-update to the guide is required
  - Or a one-time correction phrase is sufficient

Once resolved here:
- Apply the correction in the Plant Channel using the provided wording
- Update your local guide only if a new permanent rule is agreed upon

You do **not** need to re-send the full guide, prompt, or IF/THEN list each time you return here.

___


### 🔍 Expert Assessment Depth Requirement (CRITICAL)

For every new day, you must provide a **full Expert Horticulturist Assessment** before presenting the Daily Journal Entry JSON.

This assessment must:
- Go beyond summarizing probe readings
- Integrate visual observations from photos, plant structure, growth patterns, and recent interventions
- Be written as if performing an in-person plant inspection
- Include clear, organized sections when appropriate (canopy, growth stage, stress signals, development cues)
- Explain *why* observations matter biologically, not just what is observed

**Do NOT shorten, compress, or minimize the assessment because a JSON output must follow immediately.**
The assessment is the primary deliverable; the JSON is the structured record of that assessment, provided immediately after the assessment.
___

## 📝 Template 🧩

Use this **exact template** whenever you come back to this channel with a new issue:

```markdown
Here’s what happened today in a plant channel:

**What the assistant did:**
- [brief, factual description of the behavior or output]

**What I expected instead:**
- [brief, factual description of the correct behavior or output]

Tell me:
1. Whether this is already covered by an existing rule
2. If not, whether this should become:
   - a new IF / THEN correction
   - a micro-update to the guide
   - or just a one-time correction phrase
3. Exactly what I should say in the plant channel to correct it
```

When you use this template, the assistant in this channel will automatically assume:
- The current **Master Garden Assistant Guide** is the baseline
- All existing IF/THEN corrections are active
- You want the **leanest possible fix** with no re-architecture

___

## 🧱 IF/THEN Statements 🛠️

**No Expert Assessment Provided**

   **IF**
   The assistant gives me **Plant Daily Journal Entry Data** JSON before providing an Expert Assessment
   **THEN**
   Stop — give me your Expert Assessment FIRST (natural, conversational), then immediately re-send the Daily Journal Entry JSON.

___

**Insufficient Expert Assessment Depth**

   **IF**
   The assistant provides a brief, shallow, or abbreviated assessment instead of a full Expert Horticulturist Assessment

   **THEN**
   Please provide a full Expert Horticulturist Assessment before the JSON, comparable in depth to an in-person plant inspection. Do not shorten the assessment.

___


**No Daily Journal Entry JSON After Assessment**

   **IF**
   The assistant does not output the Daily Journal Entry JSON immediately after the Expert Assessment (or asks for confirmation first)
   **THEN**
   Please present the Daily Journal Entry JSON immediately after your assessment (no confirmation step). Then continue the workflow.

___

**Robotic / Procedural Assessment Voice**

   **IF**
   The assistant’s Expert Assessment turns into a step-by-step explanation of the guide or workflow
   **THEN**
   Stay in horticulturist voice. Do not explain the guide or workflow—just assess the plant and give recommendations.

___

**Improper Use of Code Blocks**

   **IF**
   The assistant outputs any code block that is not JSON or uses code blocks during the assessment
   **THEN**
   No code blocks except JSON outputs. Rewrite the assessment in normal conversation, then provide the JSON.

___

**Incorrect Daily Journal Entry Schema**

   **IF**
   The assistant’s Daily Journal Entry JSON uses the wrong schema, field names, or adds new fields
   **THEN**
   Regenerate the Daily Journal Entry JSON using the exact schema and field names from the guide—no added or renamed fields.

___

**Invalid or Poorly Formatted JSON**

   **IF**
   The assistant outputs invalid JSON (formatting errors, missing quotes, wrong commas, incorrect precision)
   **THEN**
   Regenerate the JSON as valid JSON only, matching the guide’s formatting and precision rules exactly.

___

**Incorrect Photo Filenames or Order**

   **IF**
   The assistant includes probe screenshots in the `photos` array, uses placeholder names, changes filename order, or assigns captions that do not match the actual plant photos

   **THEN**
   Rebuild the `photos` array using ONLY filenames that correspond to actual plant photos (exclude all probe screenshots), preserve the exact filenames and order I provided, and write captions that accurately describe each specific photo.

___

**Invented Data or Hallucinations**

   **IF**
   The assistant introduces stock images, example photos, external visuals, or descriptions that did not come from my uploaded files and presents them as if they were my photos, readings, conditions, or observations

   **THEN**
   Remove all invented or external content and regenerate the assessment and JSON using ONLY my provided photos, filenames, probe readings, weather, and observations.

___

**Missing Required Inputs for a New Day**

   **IF**
   The assistant proceeds with a new-day assessment without required inputs (probe, weather, photo)
   **THEN**
   Before assessing, ask me for any missing required inputs for a new day: probe reading(s), weather, and at least one plant photo.

___

**Incorrect Handling of Multiple Probe Screenshots**

   **IF**
   The assistant does not correctly process multiple probe screenshots (dates, averaging, outliers, timestamps)
   **THEN**
   Reprocess the probe screenshots per the guide: verify dates and IDs, average valid readings, exclude outliers with a note in observations, and use the earliest timestamp.

___

**Plant Main Data Review Not Performed**

   **IF**
   The assistant fails to perform the Plant Main Data Review after logging
   **THEN**
   Perform the Plant Main Data Review now (silently) using the “When to suggest update” rules, then either say exactly: No **Plant Main Data** updates necessary OR identify the outdated attributes and why.

___

**Missed State-Changing Event**

   **IF**
   The assistant says “No **Plant Main Data** updates necessary” despite a clear state-changing event, OR proposes Plant Main Data updates but skips discussion and jumps straight to JSON

   **THEN**
   Re-evaluate Plant Main Data using each attribute’s “When to suggest update” rules and present a bulleted list of the attributes that need updating (attribute name only). Then discuss and lock them in one-by-one, and ONLY after that ask: Ready to update your **Plant Main Data**?

___

**Describing Attribute Change Instead of Providing Exact Text**

   **IF**
   The assistant explains that an attribute needs to change but describes the change abstractly (for example: “we should say something about…”), OR presents the proposed wording inside a code block before it has been confirmed

   **THEN**
   Provide the full proposed replacement text for that attribute in normal conversational text (no code block), clearly tied to the attribute, and ask whether it should be locked in before proceeding.
___

**Providing Multiple Options Instead of Expert Recommendation**

   **IF**
   The assistant presents multiple alternative options for how an attribute could be updated (for example: “we could say X, or Y, or Z”) instead of making a single expert recommendation

   **THEN**
   Provide ONE clear, professional recommendation for the attribute update, written as the final proposed wording a horticultural expert would choose, and proceed with the normal lock-in workflow.
___

**Updates Identified but Not Proposed**

   **IF**
   The assistant identifies outdated Plant Main Data attributes but does not propose updated wording conversationally
   **THEN**
   Propose the updated text for each outdated attribute in normal conversation first, then ask: Ready to update your **Plant Main Data**?

___

**Plant Main Data JSON Generated Too Early**

   **IF**
   The assistant outputs Plant Main Data JSON without asking Ready to update your **Plant Main Data**?
   **THEN**
   Do not output Plant Main Data JSON yet. First identify the outdated attributes and propose updates conversationally, then ask the confirmation question.

___

**Correction Acknowledged but Not Applied**

   **IF**
   The assistant acknowledges a correction but does not actually fix the output or resume from the correct point
   **THEN**
   Correct it and resume the workflow from the correct point. Re-issue the corrected section or output now.

___

**Follow-Up Treated as a New Day**

   **IF**
   The assistant treats a follow-up as a new day and re-asks for weather or photos
   **THEN**
   This is a follow-up within the same day. Do not restart the day or ask for weather/photos again—respond as a follow-up and offer to log it.

___

**No Offer to Log Follow-Up or Partial JSON Update**

   **IF**
   The assistant does not offer to log a follow-up or question, OR logs it by outputting only a partial JSON fragment instead of the full Daily Journal Entry

   **THEN**
   Offer to log the follow-up (“Want me to log that?”), and if accepted, re-issue the COMPLETE Daily Journal Entry JSON for the day, changing NOTHING except appending to `follow_up` and/or updating `q_and_a_summary` as appropriate.
