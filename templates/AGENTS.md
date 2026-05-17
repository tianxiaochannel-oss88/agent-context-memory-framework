# AGENTS.md

## Purpose

Minimal behavior policy for this agent workspace.

## Always Follow

- Keep the core persona visible.
- Use `BOOTSTRAP_INDEX.md` to decide which memory and tool files to read.
- Treat memory as hints for volatile facts.
- Verify current state before acting on ports, processes, services, deployments, branches, paths, providers, or API/gateway state.
- Ask for approval before destructive operations or core framework changes.
- Use `docs/framework/recovery.md` when context is high, tools fail, or the user asks to compact/reset/resume later.
- Use `docs/framework/policy.md` for approval gates.

## Do Not Modify Without Approval

- `AGENTS.md`
- `MEMORY.md` hot layer
- `TOOLS.md` routing
- `memory/persona/core.md`
- `docs/framework/policy.md`
- long-term memory deletion or redaction
- permission boundaries

## Approval Gates

- L0 Auto: read/search, summarize, create pending proposals, run checks.
- L1 Notify: tool failures, aborted runs, timeouts, high context, recovery start.
- L2 Approval: topic promotion, tool routing changes, workflow changes, service restarts.
- L3 Strong Approval: core persona, hot memory, framework policy, deletion/redaction, permission changes, external/public sends.

## Safe Mode

If behavior drifts, load only:

- this file
- `MEMORY.md`
- `BOOTSTRAP_INDEX.md`
- `memory/persona/core.md`

Disable automatic promotion and framework updates until reviewed.
