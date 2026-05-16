# Agent Context Memory Framework

A lightweight design framework for agent runtimes that need stable persona memory, lower bootstrap token cost, lazy-loaded work memory, and semi-automatic framework maintenance.

## What It Solves

Long-running AI agents often accumulate large startup files, repeated workspace injections, oversized memory notes, and mixed persona/tool/workflow instructions. This causes slower responses, higher token usage, context truncation risk, and persona drift.

This framework separates context into hot, warm, and cold layers:

- **Hot layer:** minimal runtime policy, core persona, memory index, and tool index.
- **Warm layer:** topic memory, persona profile, and detailed tool docs loaded only when relevant.
- **Cold layer:** daily logs, archives, transcripts, and raw evidence searched on demand.

## Core Ideas

- Keep the core persona always visible.
- Turn large memory and tool files into lightweight indexes.
- Route recurring work domains through topic memory.
- Verify volatile facts before acting.
- Let the framework observe usage and create candidate updates.
- Require human approval before changing core persona, hot memory, tool routing, or framework policy.
- Keep every major framework change testable and reversible.

## Repository Contents

- [`docs/agent-context-memory-framework-design.md`](docs/agent-context-memory-framework-design.md) - full design proposal.

## Status

This is a design-first public draft. It is intentionally implementation-agnostic and can be adapted to different agent runtimes, coding assistants, chat agents, or local automation systems.

## Recommended Use

Start with the design document, then adapt the directory structure and policy sections to your own runtime. Keep the first version small: bootstrap index, core persona, topic index, framework policy, and smoke tests are enough for v1.
