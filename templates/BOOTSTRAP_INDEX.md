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
