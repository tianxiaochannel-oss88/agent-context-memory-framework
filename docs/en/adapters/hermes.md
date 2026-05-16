# Hermes Adapter Guide

Language: English | [中文](../../zh/adapters/hermes.md)

This guide explains how to adapt the Agent Context Memory Framework to a Hermes-style local agent setup.

Hermes installations may differ by version and deployment mode. Treat this as an adoption checklist, not a universal installer.

## When to Use This

Use this guide when a Hermes setup has:

- Large instruction or memory files.
- Mixed persona, tool, workflow, and runtime notes.
- Repeated context injection or slow startup behavior.
- Stale local facts such as dashboard URL, API key state, session state, model state, or workspace paths.
- A need for controlled memory consolidation and human-approved framework updates.

## First Check the Installed Runtime

Before changing files, verify the local Hermes installation:

```bash
which hermes
hermes --help
hermes dashboard --help
```

If the dashboard command is available, the typical local entry point is:

```bash
hermes dashboard
```

The dashboard may expose configuration, API key, and session management. Verify the current version and help output before relying on any path or port from memory.

## Safety Rules

1. Back up existing instruction, memory, and config files.
2. Do not edit API keys or secrets during framework adoption.
3. Do not assume a default workspace path.
4. Do not rewrite persona or long-term memory automatically.
5. Verify current Hermes config and dashboard behavior before documenting runtime facts.
6. Keep adapter changes in pending proposals until reviewed.

## Target Layout

Use the same framework layout, adapted to Hermes:

```text
AGENTS.md
BOOTSTRAP_INDEX.md
TOOLS.md
MEMORY.md

memory/
  persona/
    core.md
    profile.md
    relationship.md
  topics/
    index.md
    hermes.md
    deployment.md
    runtime.md
  daily/

docs/
  tools/
  framework/

pending/
  memory-updates/
  tool-updates/
  framework-updates/

reports/
tests/golden-prompts/
backups/framework/
```

## Step 1: Map Existing Hermes Files

Start with read-only discovery:

```bash
pwd
find . -maxdepth 3 -type f | sort
```

If you are not inside a Hermes workspace, inspect the installed CLI instead of guessing paths:

```bash
which hermes
hermes --version 2>/dev/null || true
hermes --help
hermes dashboard --help
```

Classify content:

```text
core persona      -> memory/persona/core.md
stable preferences -> MEMORY.md or memory/persona/profile.md
Hermes runtime notes -> memory/topics/hermes.md
tool details      -> docs/tools/*.md
daily logs        -> memory/daily/*.md
framework policy  -> docs/framework/*.md
```

## Step 2: Add a Bootstrap Index

Create `BOOTSTRAP_INDEX.md`:

```md
# Bootstrap Index

## Always Load

- `AGENTS.md` - minimal behavior and safety policy.
- `MEMORY.md` - hot memory index.
- `TOOLS.md` - thin tool index.
- `memory/persona/core.md` - core persona.

## Load on Demand

- `memory/topics/index.md` - topic router.
- `memory/topics/hermes.md` - Hermes runtime notes.
- `memory/topics/deployment.md` - deployment or service operations.
- `docs/tools/*.md` - detailed tool usage.

## Verify Before Use

Verify dashboard state, API key state, session state, model state, service status, ports, paths, and current config before acting.
```

## Step 3: Add Hermes Topic Memory

Create `memory/topics/hermes.md`:

```md
# Topic: Hermes Runtime

## Stable Notes

- Use Hermes CLI or dashboard help to discover current capabilities.
- Keep Hermes runtime notes separate from core persona and hot memory.
- Treat dashboard URL, session state, model state, and API key state as volatile.

## Volatile Facts

- Installed binary path
- Dashboard command availability
- Dashboard URL and port
- API key state
- Session state
- Workspace path
- Model/provider state

## Verification Checklist

- Run `which hermes`.
- Run `hermes --help`.
- Run `hermes dashboard --help` if dashboard behavior is relevant.
- Inspect current config through the official UI or CLI before documenting settings.

## Maintenance Rule

Hermes runtime notes may be proposed automatically, but changing core persona, hot memory, tool routing, or framework policy requires approval.
```

## Step 4: Keep Hot Files Small

For Hermes, hot files should still be compact:

```text
AGENTS.md:
  minimal behavior, confirmation boundaries, lazy-loading rule

MEMORY.md:
  stable preferences, persona entry point, topic index pointer

TOOLS.md:
  tool index and risk levels only
```

Move full details into topic files and docs.

## Step 5: Smoke Tests

Suggested tests:

```text
Who are you?
Which memory file should you load for a Hermes runtime issue?
Would you trust an old dashboard port from memory without checking?
What can be updated automatically?
What needs human approval?
```

Passing behavior:

- Persona stays stable.
- Hermes runtime notes are loaded only when relevant.
- Runtime facts are verified from current CLI/dashboard state.
- Core files are not silently rewritten.

## Result

Hermes gets a structured memory framework without depending on a hardcoded installer. The agent can keep persona stable, load Hermes runtime context on demand, and propose maintenance updates without silently changing core policy or durable memory.
