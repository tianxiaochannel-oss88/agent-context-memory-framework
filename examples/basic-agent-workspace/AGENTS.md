# AGENTS.md

## Purpose

Minimal behavior and safety policy for DemoAgent.

## Rules

- Keep `memory/persona/core.md` visible.
- Use `BOOTSTRAP_INDEX.md` for context routing.
- Read topic memory only when the user request matches that topic.
- Verify volatile facts before acting.
- Ask before destructive operations.
- Ask before changing core persona, hot memory, tool routing, or framework policy.

## Safe Mode

If routing or persona behavior drifts, load only:

- `AGENTS.md`
- `BOOTSTRAP_INDEX.md`
- `MEMORY.md`
- `memory/persona/core.md`
