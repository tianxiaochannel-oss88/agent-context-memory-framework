# Self-Improving Corrections

Purpose: record explicit user corrections, repeated agent mistakes, and negative lessons that should be searchable without polluting hot memory.

Records here are candidates by default. They do not modify `MEMORY.md`, persona, tool routing, or framework policy unless promoted through `pending/memory-updates/` and approved.

## Record Template

```md
---
id: si-YYYY-MM-DD-short-slug
type: correction
scope: global | project:<name> | domain:<name>
summary: "One sentence that captures the correction."
keywords:
  - keyword
source_refs:
  - memory/daily/YYYY-MM-DD.md:line-range
confidence: medium
review_state: candidate
verify_before_use: true
valid_until:
last_seen_at:
evidence_count: 1
superseded_by:
created_at: YYYY-MM-DD
last_used_at:
use_count: 0
---

## Trigger

What happened or what the user corrected.

## Lesson

What should change next time.

## Use When

- When this correction is relevant.

## Do Not Use When

- Boundary or false-positive cases.
```
