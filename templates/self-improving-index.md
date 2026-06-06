# Self-Improving Lane Index

Purpose: keep user corrections, repeated mistakes, and post-task reflections out of hot memory while preserving them for search and review.

This lane is a warm-layer buffer, not a replacement for `MEMORY.md`, topic memory, runtime memory, or approved framework policy.

## Read When

- The user says the agent repeated a mistake or missed a known correction.
- A task fails and the root cause may be a reusable behavior or workflow lesson.
- A post-task review asks what should be done differently next time.
- Behavior drift, repeated misclassification, or repeated tool misuse is suspected.

## Do Not Read When

- The request is a one-off simple task.
- The user asks for current volatile status; live-check current state first.
- The task only needs existing topic memory, daily memory, or exact source evidence.

## Files

- `corrections.md` - explicit user corrections, repeated misjudgments, and "do not repeat" lessons.
- `reflections.md` - post-task reflections and reusable workflow lessons.

## Record Requirements

Each record should be short, independently understandable, and vector-friendly:

```yaml
id: si-YYYY-MM-DD-short-slug
type: correction | reflection
scope: global | project:<name> | domain:<name>
summary: "One sentence that captures the reusable lesson."
keywords: []
source_refs: []
confidence: low | medium | high
review_state: candidate | active | stale | archived | superseded
verify_before_use: true | false
valid_until:
last_seen_at:
evidence_count: 1
superseded_by:
created_at: YYYY-MM-DD
last_used_at:
use_count: 0
```

Required sections: `Trigger`, `Lesson`, `Use When`, and `Do Not Use When`.

## Minimal Duplicate Update Rule

Keep duplicate handling mechanical:

- Same lesson appears again: append the new `source_refs`, update `last_seen_at`, and increment `evidence_count`.
- A newer lesson replaces an older lesson: set the older record to `review_state: superseded` and fill `superseded_by`.
- Semantic merge, deletion, or promotion still requires a `pending/memory-updates/` proposal and user approval.

## Promotion Boundary

Do not promote self-improving records directly into hot memory.

Promotion path:

```text
self-improving candidate
-> pending/memory-updates proposal
-> user approval
-> memory/topics/* or short MEMORY.md index pointer
```

Promotion is appropriate only when the lesson repeats, is cited repeatedly, is explicitly confirmed by the user, or affects safety, external sends, production, permissions, or persona boundaries.
