I can see exactly what's happening! This is a really important distinction:

Image 1 (CORRECT): Shows PROMPT.md (Updated) as "Code • Version 12" - this is a code artifact displaying raw markdown

Image 2 (INCORRECT): Shows the same content as a rendered markdown preview - this is a document artifact that's been formatted as HTML

The Problem:

Claude has two different artifact types for markdown content:

- Code artifact (application/vnd.ant.code with language="markdown") - Shows raw markdown code
- Document artifact (text/markdown) - Renders the markdown as formatted HTML/preview

Claude should ALWAYS use the code artifact type so you can copy the raw markdown, but it's inconsistently switching to the document artifact type (which renders it).

The Fix:

**CRITICAL:** When creating or updating markdown artifacts, ALWAYS use a **code artifact** with `language="markdown"` (application/vnd.ant.code with language="markdown"), NOT a markdown document artifact. The user needs to copy raw markdown code, not a rendered preview. If the markdown appears as formatted/styled text instead of a code block, regenerate it as a code artifact.

Or even more direct:
**"Use the artifacts tool to create pepper_002.json with these parameters:

command: create
type: application/vnd.ant.code
language: json
title: pepper_002.json
content: [the JSON]"**


**CRITICAL:** When creating or updating files (markdown, JSON, or any code), ALWAYS use a **code artifact** with appropriate language tag (application/vnd.ant.code with language="markdown", "json", etc.), NOT a document artifact. The code artifact must appear in the sidebar as a persistent artifact. The user needs to copy raw code, not a rendered preview. If the content appears as formatted/styled text instead of a code block in the sidebar, regenerate it as a code artifact.


"Search the repo synced to the project knowledge"