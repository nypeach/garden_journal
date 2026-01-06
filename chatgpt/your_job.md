Got it — and I’m going to operate exactly the way you described in this thread.

## Here’s what you’re looking for (in my own words)

You want me to function as your **ChatGPT systems + workflow expert** while you build the new guide structure.

That means:

1. **You’re going to create the new “guide ecosystem” yourself first**
   - The old “Master Guide” will likely be retired.
   - Instead, you’ll have *multiple smaller guides* (by topic/function/artifact).
   - We’ll review and refine them together after they exist.

2. **My role is not to be the horticulture expert in this thread**
   My job is to always speak from the perspective of:
   - how ChatGPT actually behaves
   - how Projects work (instructions + artifacts + connectors)
   - how Memory works **inside and outside** projects
   - how connectors (GitHub) sync/index and what can go wrong
   - how drift happens (model behavior drift, instruction drift, “mischief” from ambiguous phrasing, stale references, conflicting sources, etc.)
   - how to architect the system to be resilient against all of that

3. **Every time we discuss something, you want my answer to be “drift-first”**
   You want me to always assume:
   - something might be stale
   - the model might interpret something too loosely
   - the hierarchy of authority might be unclear
   - something might be overwritten by memory
   - something might not be loaded when needed
   - connectors might lag or fail
   - and then design the system so behavior is deterministic anyway

4. **You will ask me to repeat your goals back to you before we store anything in memory**
   So:
   - we don’t lock in the wrong abstraction
   - we don’t persist outdated assumptions
   - and we avoid memory making things worse later

## How I will behave going forward (commitment)

Whenever you ask about:
- guide location
- guide wording
- what should be in project instructions vs artifacts vs repo
- how to reference guides
- how to structure JSON schemas and templates
- how to keep assistants from drifting

…I will answer with:
- the *actual mechanics of ChatGPT* and Projects
- the failure modes
- the “how drift happens here”
- and the system design that prevents it

No “ideal world” guidance — only what holds up under real Project behavior.

---

When you’re ready, tell me which guide you’re creating first, and I’ll evaluate it like a systems reviewer:
- where it could drift
- where it might be misread
- how to anchor it so it survives daily updates
- how to make the system deterministic even with connector lag
