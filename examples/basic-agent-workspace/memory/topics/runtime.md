---
id: mem-topic-runtime-demo
type: topic_summary
topic: runtime
status: active
confidence: medium
created_at: 2026-01-01
updated_at: 2026-01-01
last_verified: null
content_hash: sha256:demo-topic-runtime
source_hashes:
  - sha256:demo-leaf-runtime
stability: mixed
valid_until: null
verify_before_use: true
review_state: approved
reviewed_by: human
conflict_status: none
conflicts_with: []
redaction_state: none
source_refs:
  - memory/leaves/2026-01-01-runtime-check.md
derived_from:
  - leaf-2026-01-01-runtime-check
supersedes: null
---

# Topic: Runtime

## Stable Facts

- DemoAgent should separate remembered service names from current service state.
- Runtime status must be verified live before action.

## Current Workflow

1. Read this topic summary.
2. Drill down to the leaf summary if details are needed.
3. Verify process, port, and log state before acting.

## Known Failure Modes

- Treating old port notes as current truth.
- Confusing context exhaustion with service failure.

## Verification Checklist

- Check current service status.
- Check current process list.
- Check current logs.
- Check current port listeners.

## Provenance

- Source: `memory/leaves/2026-01-01-runtime-check.md`
- Evidence: fake demo source only.
- Last verified: not verified in a real environment.
