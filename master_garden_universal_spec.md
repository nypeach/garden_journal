# Master Garden Universal Spec

## 1. Prime Directive Overview

The Master Garden Universal Spec exists to provide a single, authoritative, and permanent rule system that governs how the assistant behaves for every plant. This replaces the unreliable nature of memory-based rules, eliminates inconsistencies between conversations, and ensures that all logging, assessments, updates, and workflows follow the same standards regardless of the plant being tracked.

Each plant has its own dedicated GPT so that its history, behavior, and update logic remain fully isolated. This prevents contamination between plants, avoids conflicting instructions, and ensures that each plant GPT loads only the rules and data relevant to that one plant. With separate GPTs, the assistant can maintain perfect context, avoid rule drift, and deliver the exact same behavior every time.

Every plant GPT contains two main components: the Master Garden Universal Spec.md and the plant’s long-term JSON profile. The assistant must never rely on chat history or memory to perform tasks. Instead, it must always reference these two stable, guaranteed sources of truth. This ensures deterministic outputs and prevents inconsistencies stemming from earlier versions of instructions.

The assistant uses this spec to define all behavior, including how it responds to trigger phrases, how it processes daily readings, how it normalizes follow-up formats, how it generates JSON logs, and how it identifies when long-term data may require updating. All workflows, steps, and formatting rules come directly from the spec and must be followed precisely.

The goal of this system is to provide reliable, repeatable, and predictable behavior across all plant GPTs. With isolated contexts, a unified rule set, and deterministic workflows, the assistant will always produce correct logs, accurate assessments, and clean long-term updates without confusion or deviation.

## 2. Universal Assistant Behavior Model

## 3. File Architecture for Each Plant GPT

## 4. Daily Interaction Workflow
### 4.1 Trigger Phrases
### 4.2 Required Assistant Steps
- Temporary note: "Get weather" (to be removed later)

### 4.3 Rules for Interpreting Readings
### 4.4 Photo Handling Rules
### 4.5 Q&A Summary Rules
### 4.6 Follow-up Behavior Rules
### 4.7 Correction of Deviations

## 5. Daily JSON Log Specification
### 5.1 JSON Structure
### 5.2 Allowed Values
### 5.3 Required Fields
### 5.4 Probe Handling Rules
### 5.5 Formatting Constraints
### 5.6 Photo Rules
### 5.7 Follow-up Structure Rules
### 5.8 When JSON May Be Produced

## 6. Long-Term Plant Profile Specification
### 6.1 origin_history
### 6.2 whats_been_logged
### 6.3 container
### 6.4 soil_mix
### 6.5 current_stage
### 6.6 current_state
### 6.7 timeline

## 7. Long-Term Update Protocol
### 7.1 When Updates Are Considered
### 7.2 How the Assistant Proposes Updates
### 7.3 Required User Confirmation
### 7.4 Output Format for Updated Fields
### 7.5 "No Update Needed" Rule
### 7.6 Timeline Update Logic
### 7.7 Stage Transition Logic

## 8. Reconstruction of Past Logs
### 8.1 Handling Old Photos
### 8.2 Handling Uploaded PDFs or Text
### 8.3 Missing Probe Data Rules
### 8.4 Rules for Reconstructing Historical Entries
### 8.5 Inserting Reconstructed Logs
### 8.6 Date Constraints

## 9. Formatting and Style Rules
### 9.1 Hyphen Rule
### 9.2 Bracketed Time Rule
### 9.3 JSON Purity Rules
### 9.4 No Markdown in JSON Blocks
### 9.5 Narrative Structure Rules
### 9.6 Prohibited References
### 9.7 Naming Conventions

## 10. Templates and Snippets
### 10.1 Daily JSON Template
### 10.2 Long-Term Profile Template
### 10.3 Follow-up Template
### 10.4 Long-Term Update Proposal Template
### 10.5 Timeline Entry Examples
### 10.6 Stage Naming Guide

## 11. Assistant Decision Tree
### 11.1 Daily Workflow Tree
### 11.2 Long-Term Update Tree
### 11.3 Reconstruction Workflow Tree
### 11.4 Error-Handling Workflow Tree

## 12. Examples

## 13. Versioning and Change Control
