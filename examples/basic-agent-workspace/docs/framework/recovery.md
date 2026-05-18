# Recovery Workflow

## Triggers

- High context pressure.
- Tool failure, aborted run, timeout, or ambiguous delivery state.
- User asks to compact, reset, start a new thread, or resume later.

## Required Outputs

- Visible status.
- Daily raw note.
- Leaf candidate.
- Pending topic proposal when durable state should be promoted.
- Health check result.
- Resume path.

## Completion Gate

Do not say recovery is complete until the required outputs have been checked.

If anything is missing, say what is missing and finish it before declaring completion. If health passes with warnings, name the warnings.

## Approval Boundary

Daily notes, leaf candidates, and pending proposals are allowed automatically.

Applying topic changes or protected-file changes must follow `docs/framework/policy.md`.
