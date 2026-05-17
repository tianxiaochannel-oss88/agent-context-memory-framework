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

## Approval Boundary

Daily notes, leaf candidates, and pending proposals are allowed automatically.

Applying topic changes or protected-file changes must follow `docs/framework/policy.md`.
