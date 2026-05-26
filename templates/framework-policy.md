# Framework Policy

Purpose: let the framework improve from real usage without silently changing identity, memory authority, tool routing, or permissions.

## L0 Auto

Allowed without asking:

- read/search topic, leaf, daily, and archive memory
- generate session summaries
- create candidate proposals under `pending/`
- create leaf candidates from raw notes
- run health checks and golden prompts

## L1 Notify

Allowed, but must be visible to the user before continuing:

- tool failure, aborted run, timeout, or post-processing error
- high context pressure
- recovery workflow starting
- ambiguous external delivery state
- maintenance warning without protected-file changes

## L2 Approval

Ask before applying:

- update active topic memory
- promote a leaf into active topic memory
- update active digest memory
- change recurring workflow behavior
- update tool routing
- restart local services when not explicitly requested

## L3 Strong Approval

Require explicit, target-specific approval:

- modify core persona
- modify hot memory
- modify framework policy
- modify permission boundaries
- delete/redact long-term memory or source evidence
- external/public sends
- credential changes
- production or destructive operations

## Standing Promoted Cleanup Exception

Long automatic promoted-memory sections may be cleaned mechanically without case-by-case approval only when all conditions hold:

- the section has promotion source markers
- referenced source files still exist
- the target `memory/promoted/` file will not overwrite existing content
- the promoted section is moved unchanged
- hot memory receives only a short source-linked index
- no persona, tools, topic memory, framework policy, permissions, deletion/redaction, or semantic rewrite is involved

Stop and ask for explicit approval if any condition is uncertain.

Generic "continue" or "do it" does not count as L3 approval unless the protected target is named.

## Prompt Shape

```text
Approval needed:
- Target:
- Why:
- Risk:
- Rollback:
- Proposed action:

Do you approve?
```

For L3:

```text
This is a strong-approval item because it changes <protected target>.
Please explicitly approve changing <target>.
```
