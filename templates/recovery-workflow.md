# Recovery Trigger Workflow

Purpose: make recovery a fixed workflow instead of an informal note.

## Triggers

Run this workflow when:

- context pressure is high
- a tool fails, aborts, times out, or returns ambiguous delivery state
- the user asks to compact, reset, start a new thread, or resume later
- a project needs a durable handoff point

## Context Pressure

- `>=70%`: warn before starting long tool or generation loops.
- `>=80%`: do not start heavy work; create a recovery point or move to a fresh thread.
- `>=90%`: emergency recovery only.

If exact context usage is unavailable, infer pressure from thread age, repeated failures, or tool stalls, and state uncertainty.

## Required Outputs

For significant incidents, create or verify:

1. Visible status to the user.
2. Project recovery file or resume note when useful.
3. Raw daily note.
4. Leaf candidate with `source_refs` and `derived_from`.
5. Pending topic proposal when durable state should be promoted.
6. Framework health check.
7. Exact resume path.

Daily-only recovery is incomplete for incidents that affect durable project state, accepted assets, failure rules, or future resume instructions.

## Completion Gate

Do not say `recovery complete` until every required output has been checked.

If an item is missing, report it clearly:

```text
Recovery body is written, but the framework item still missing is: <item>.
I will complete it before declaring recovery complete.
```

If the health check passes with warnings, name the warnings explicitly.

## Approval Gates

Recovery may automatically create daily notes, leaf candidates, and pending proposals.

It must ask before applying L2 changes and require target-specific approval before L3 changes. See `docs/framework/policy.md`.
