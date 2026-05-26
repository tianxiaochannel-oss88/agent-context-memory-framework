# Basic Agent Workspace Example

This is a fake minimal workspace showing how the framework files fit together.

It is safe to read and copy from, but do not copy it over a real workspace without adapting the placeholder content and making a backup first.

## What This Demonstrates

- Thin hot files: `AGENTS.md`, `MEMORY.md`, `TOOLS.md`, `BOOTSTRAP_INDEX.md`
- Core persona in `memory/persona/core.md`
- Topic routing through `memory/topics/index.md`
- Memory Tree Lite with `memory/leaves/`, `memory/promoted/`, and `memory/digests/`
- Provenance metadata with `source_refs`, `derived_from`, `review_state`, and `verify_before_use`
- Approval gates under `docs/framework/policy.md`
- Recovery trigger workflow under `docs/framework/recovery.md`
- Smoke-test prompts under `tests/golden-prompts/`
- Vector-friendly memory shape without requiring a vector database

## Fake Scenario

The example agent is `DemoAgent`, a generic local automation assistant. The example topic is runtime troubleshooting for a fictional service called `demo-service`.
