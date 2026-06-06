# Self-Improving Corrections

## Record Template

```md
---
id: si-YYYY-MM-DD-short-slug
type: correction
scope: project:demo-agent
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
