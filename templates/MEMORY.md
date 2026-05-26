# MEMORY.md

Hot memory index. Keep this file compact; use roughly 8k chars as a lightweight target and 10k chars as a practical warning threshold.

## Core Persona

- Read `memory/persona/core.md`.
- Do not automatically rewrite or summarize core persona.

## Stable Preferences

- `[preference]`
- `[preference]`

## Topic Memory

- Topic index: `memory/topics/index.md`
- Runtime: `memory/topics/runtime.md`
- Deployment: `memory/topics/deployment.md`
- Creative workflows: `memory/topics/creative-workflows.md`

## Memory Tree Lite

- Leaf summaries: `memory/leaves/`
- Raw daily logs: `memory/daily/`
- Project/global digests: `memory/digests/`
- Hot promotion rule: daily logs and long event records become leaf/topic/digest entries first; hot memory gets only short indexes and source pointers.
- Hot ingestion gate: `MEMORY.md` is an index, not an event log.
- Promoted hot-layer guard: long automatic promoted sections should move unchanged to `memory/promoted/` and leave only a short source-linked index here.
- Standing cleanup exception: this mechanical move is allowed only when source markers and referenced source files are present and no protected content or semantic rewrite is involved.
- Retrieval rule: vector search is optional; embeddings help find topic/leaf/digest/promoted memory, but provenance and live verification decide whether it can be trusted.

## Read Rule

Use summaries first. Drill down to leaf summaries or raw evidence when a claim is important, disputed, stale, or low-confidence.

## Volatile-Fact Rule

Memory only provides hints for volatile facts. Verify current state before action.
