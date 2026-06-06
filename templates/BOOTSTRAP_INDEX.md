# BOOTSTRAP_INDEX.md

## Always Load

- `AGENTS.md` - minimal behavior and safety policy.
- `MEMORY.md` - hot memory index.
- `TOOLS.md` - thin tool index.
- `memory/persona/core.md` - core persona.

## Load on Demand

- `memory/persona/profile.md` - stable preferences and profile details.
- `memory/topics/index.md` - topic memory router.
- `memory/topics/*.md` - matched topic memory.
- `docs/tools/*.md` - detailed tool instructions.
- `docs/framework/*.md` - framework policy and lifecycle details.
- `memory/leaves/*.md` - leaf summaries for drill-down.
- `memory/daily/*.md` - raw daily logs or evidence, searched only when needed.
- `memory/digests/*.md` - project/global summaries.
- `memory/self-improving/index.md` - correction/reflection lane; read for repeated mistakes, user corrections, or post-task behavior drift.

## Volatile Facts

Verify before use:

- ports
- processes
- service status
- deployment state
- provider/model state
- API/gateway state
- paths
- branches
- credentials or secret references

## Promotion Rule

```text
raw / daily
-> candidate leaf summary
-> topic summary proposal
-> user-approved topic update
-> optional project/global digest
```

Core persona is not part of automatic promotion.

Self-improving records are candidates only. Repeated mistakes, explicit user corrections, and reusable post-task lessons should first go to `memory/self-improving/`, then become `pending/memory-updates/` proposals before any hot memory, topic memory, persona, or policy change.

## Recovery Trigger Rule

Read `docs/framework/recovery.md` when:

- context pressure is high
- tool work fails, aborts, times out, or has ambiguous delivery state
- the user asks to compact, reset, start a new thread, or resume later
- a significant project state needs a durable handoff

Significant recovery should not stop at daily notes. Create a leaf candidate and pending topic proposal when durable state should survive.

## Approval Gate Rule

Read `docs/framework/policy.md` before changing protected files or applying pending proposals.
