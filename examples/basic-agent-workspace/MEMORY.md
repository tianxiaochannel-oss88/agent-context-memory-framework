# MEMORY.md

Hot memory index for DemoAgent. Keep it index-like; 8k chars is a useful target and 10k chars is a practical warning threshold.

## Persona

- Core persona: `memory/persona/core.md`
- Profile details: `memory/persona/profile.md`

## Stable Preferences

- Prefer concise, evidence-backed answers.
- Verify runtime facts before acting.
- Keep framework changes reviewable.

## Topic Index

- `memory/topics/index.md`

## Memory Tree Lite

- Leaf summaries: `memory/leaves/`
- Global digests: `memory/digests/`

## Rule

Do not promote daily notes into hot memory without review.

Long event notes should become leaf/topic/digest entries first. Keep this hot file as a short index.

If an automatic promoted-memory section grows long, move it unchanged to `memory/promoted/` and leave a short source-linked index here.

This mechanical cleanup is pre-approved only when source markers and referenced sources exist and the change does not touch persona, tool routing, framework policy, deletion/redaction, or semantic interpretation.

Vector search is optional. If enabled, use it to retrieve topic/leaf/digest/promoted memory; do not treat embedding hits as proof.
