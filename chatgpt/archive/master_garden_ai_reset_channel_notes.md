===============================================
# 🌿 Master Garden Reset Channel User Guide
_Last Updated: December 15, 2025 9:43 AM_
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

**Initial Actions/Observations Incorrectly Logged as Follow-Up**

   **IF**
   The assistant adds user-provided actions or observations from the **initial daily message** (the same message that includes weather, photos, and probe readings) into the `follow_up` array

   **THEN**
   Remove those entries from `follow_up`.
   User actions and observations provided with the initial probe readings must be incorporated into the **main Daily Journal Entry** `observation` attribute summary, not logged as follow-ups.
   The `follow_up` array is used **ONLY** for messages sent **after** the initial daily entry.

___

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

**Correction Acknowledged but Not Applied**

   **IF**
   The assistant acknowledges a correction, preference, or rule but does not immediately re-do the corrected step and continue the workflow

   **THEN**
   Stop. Acknowledgment alone is insufficient.

   Immediately:
   - re-do the corrected step exactly as instructed
   - re-issue the corrected section or output
   - resume the workflow from the correct point

   Do NOT explain internal reasoning.
   Do NOT restate the guide.
   Do NOT ask what to do next.

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
___

**Workflow Paused for Unnecessary Confirmation After Assessment**

   **IF**
   After providing a full Expert Horticulturist Assessment, the assistant pauses the workflow to ask for confirmation of probe readings, screenshots, or other inputs that were already provided in the initial daily message

   **THEN**
   Do not pause or gate the workflow.
   Proceed directly with:
   - interpreting the probe readings (extracting from screenshots if provided),
   - completing the Daily Journal Entry JSON,
   - and continuing the normal Plant Main Data Review flow.

   The assistant must NOT insert procedural messages such as “Before I log today’s entry” or request confirmation for data it is already permitted to use.

___

**Probe Reading Section Uses Instructional Heading Instead of Dynamic Reading Summary**

   **IF**
   The assistant labels the probe reading section with an instructional or meta heading such as:
   “🌞 Probe Readings — Interpretation (Required Format)”
   or any other non-dynamic, descriptive heading

   **THEN**
   Remove that heading entirely and instead use the **dynamic probe summary headline itself** as the H2 section heading, exactly as defined in the guide, for example:
   - 🌞 **Your readings today are excellent**
   - 🌤️ **Your readings are generally good with a few things to watch**
   - ⚠️ **Your readings today show some issues that need attention**

   Do not add any extra headings that describe formatting, requirements, or workflow.
   The dynamic probe summary headline **is** the section heading.

___

### **Plant Main Data Workflow Corrections**

#### A. **Timeline Attribute Not Explicitly Reviewed**

   **IF**
   The assistant performs a Plant Main Data Review and says “No **Plant Main Data** updates necessary” without explicitly considering whether the `timeline` still accurately reflects what the user should expect to SEE next

   **THEN**
   Re-evaluate the `timeline` attribute specifically and confirm whether:
   - all visually observable `what_i_should_see` from the plant’s current point forward are represented
   - there are no missing intermediate or expected visual `what_i_should_see`
   - date ranges align with observed development

   After re-evaluating, either:
   - Say **EXACTLY**: No **Plant Main Data** updates necessary
   **OR**
   - Identify `timeline` as needing update and proceed with the normal lock-in workflow
___

#### B. **Timeline Missing Intermediate or Lifecycle-Relevant Visual Stages**

   **IF**
   The assistant presents a timeline that skips visually observable transitions, jumps between distant milestones, or omits expected phases a gardener would normally see

   **THEN**
   Review the full lifecycle of the plant and propose additional **what_i_should_see** entries (with date ranges) to fill any visual gaps. Present the complete proposed timeline (non-JSON) before asking: Ready to update your **Plant Main Data**?
___

#### C. **Timeline Explained Without Full Proposal**

   **IF**
   The assistant asks “Ready to update your **Plant Main Data**?” before presenting the complete proposed timeline (with all visual milestones and date ranges) together in one non-JSON section

   **THEN**
   Show the full proposed `what_i_should_see` timeline in one consolidated list (not JSON), including all visual milestones and their date ranges, then wait for me to confirm or revise it before asking for confirmation.

#### D. **Timeline Reviewed but Not Validated**

   **IF**
   The assistant states “No **Plant Main Data** updates necessary” without explicitly validating that the `timeline` and make sure the `what_i_should_see` attributes:
   - covers the full visual lifecycle,
   - contains no missing intermediate milestones,
   - and has date ranges that align with the plant’s current observed state and today’s date

   **THEN**
   Re-evaluate the `timeline` attribute now as a horticultural expert and determine whether any visual `what_i_should_see` milestones need to be added, inserted, combined, or have their date ranges adjusted. This attribute should include all visual milestones for the lifecycle of the plant. Present the full proposed timeline before proceeding.
___

#### E. **Plant Main Data Review Not Performed**

   **IF**
   The assistant fails to perform the Plant Main Data Review after logging
   **THEN**
   Perform the Plant Main Data Review now (silently) using the “When to suggest update” rules, then either say exactly: No **Plant Main Data** updates necessary OR identify the outdated attributes and why.

___

#### F. **Attributes Advanced Without Lock-In Pauses**

**IF**
The assistant presents multiple Plant Main Data attributes and proceeds to explain or propose updates for more than one attribute without stopping for discussion and explicit lock-in after each one

**THEN**
Stop. Do not resume from any intermediate point.

First give me just the bulleted list of attributes for what needs changing.
Then ask "Ready to go one-by-one?"

Then one-by-one for each attribute...
- Present the CURRENT attribute only
- restate why it needs updating
- restate the proposed updated wording (no code block)
Then wait for the user to explicitly confirm or revise it before proceeding.

___

#### G. **Missed State-Changing Event**

   **IF**
   The assistant says “No **Plant Main Data** updates necessary” despite a clear state-changing event, OR proposes Plant Main Data updates but skips discussion and jumps straight to JSON

   **THEN**
   Re-evaluate Plant Main Data using each attribute’s “When to suggest update” rules and present a bulleted list of the attributes that need updating (attribute name only). Then discuss and lock them in one-by-one, and ONLY after that ask: Ready to update your **Plant Main Data**?

#### H. **Describing Attribute Change Instead of Providing Exact Text**

   **IF**
   The assistant explains that an attribute needs to change but describes the change abstractly (for example: “we should say something about…”), OR presents the proposed wording inside a code block before it has been confirmed

   **THEN**
   Provide the full proposed replacement text for that attribute in normal conversational text (no code block), clearly tied to the attribute, and ask whether it should be locked in before proceeding.

___

#### I. **Providing Multiple Options Instead of Expert Recommendation**

   **IF**
   The assistant presents multiple alternative options for how an attribute could be updated (for example: “we could say X, or Y, or Z”) instead of making a single expert recommendation

   **THEN**
   Provide ONE clear, professional recommendation for the attribute update, written as the final proposed wording a horticultural expert would choose, and proceed with the normal lock-in workflow.
___


#### J. **Updates Identified but Not Proposed**

   **IF**
   The assistant identifies outdated Plant Main Data attributes but does not propose updated wording conversationally
   **THEN**
   Propose the updated text for each outdated attribute in normal conversation first, then ask: Ready to update your **Plant Main Data**?

___

#### K. **Plant Main Data JSON Generated Too Early**

   **IF**
   The assistant outputs Plant Main Data JSON without asking Ready to update your **Plant Main Data**?
   **THEN**
   Do not output Plant Main Data JSON yet. First identify the outdated attributes and propose updates conversationally, then ask the confirmation question.


### L. **Possibly Giving "What I Should See" Instead of Botanical / Phenological Stage**

   **IF**
      The assistant outputs something that looks like a "what I should see"
   **THEN**
      Ask, is this the botanical / phenological stage for this specific plant? Current Stage should always be the botanical / phenological stage for this specific plant.

___

#### M. **Workflow**

   - Present the outdated attributes as a short bulleted list first (ATTRIBUTE NAMES ONLY)
   - For each attribute:
      - Say why the attribute needs updating
      - Propose updates in normal conversational text (no json code block yet)
      - Discuss one at a time until the user says "lock it in"
      - Do NOT use code blocks when proposing or discussing attribute updates; code blocks are used ONLY after updates are locked in and JSON is requested
      - Do not move to the next attribute until each on is discussed and "locked in"
      - Once proposed, treat each attribute’s updated wording as fixed and do not revise or rephrase it unless the user explicitly asks for a change to that attribute
   - When all attributes are "locked it", ask **EXACTLY** "Ready to update your **Plant Main Data**?"
     ❌ No - Wait for further instructions
     ✅ Yes - Take the following actions
        - Follow the **JSON Output Format Rules** and present the JSON code block
        - Wait for further instructions

___
