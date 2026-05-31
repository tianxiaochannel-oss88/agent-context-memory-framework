# Hermes Adapter Guide

Language: English | [中文](../../zh/adapters/hermes.md)

This guide explains how to adapt the Agent Context Memory Framework to a Hermes-style local agent setup.

Hermes installations may differ by version and deployment mode. Treat this as an adoption checklist, not a universal installer.

Do not force Hermes to copy an OpenClaw-style file layout. The framework layers should map onto Hermes' active overlay model: compact identity, user profile, hot memory index, workspace routing, and archived detail.

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
7. Do not reload memories, rebuild system prompts, or change toolsets mid-conversation unless the runtime provides an explicit immediate-invalidation path. Prefer deferred changes that take effect in the next session.

## Layer Mapping

Map the framework layers to the Hermes files that the installed runtime actually uses. A common local overlay looks like this:

```text
~/.hermes/SOUL.md
  -> core persona / identity

~/.hermes/memories/USER.md
  -> stable user profile and preferences

~/.hermes/memories/MEMORY.md
  -> compact hot memory index

~/.hermes/workspace/AGENTS.md
  -> workspace routing, safety gates, archive map

~/.hermes/workspace/openclaw-migration-archive/<timestamp>/
  -> cold/warm archived OpenClaw memory, topics, tool notes, and framework docs
```

If a Hermes workspace already uses `AGENTS.md`, `BOOTSTRAP_INDEX.md`, `TOOLS.md`, and `MEMORY.md`, the generic framework layout is still valid. If it uses `SOUL.md`, `USER.md`, `memories/MEMORY.md`, and workspace routing instead, keep that native shape and document the mapping.

## Step 1: Map Existing Hermes Files

Start with read-only discovery:

```bash
hermes_home="${HERMES_HOME:-$HOME/.hermes}"
find "$hermes_home" -maxdepth 3 -type f \
  \( -name 'SOUL.md' -o -name 'USER.md' -o -name 'MEMORY.md' -o -name 'AGENTS.md' \) \
  | sort
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
core persona        -> ~/.hermes/SOUL.md, or memory/persona/core.md in a custom workspace
stable preferences  -> ~/.hermes/memories/USER.md, or a compact hot/profile file
hot memory index    -> ~/.hermes/memories/MEMORY.md
workspace routing   -> ~/.hermes/workspace/AGENTS.md
Hermes runtime notes -> archive/topic files, for example memory/topics/hermes.md
tool details        -> archive/tool docs, not hot memory
daily logs/raw notes -> archive/raw memory or daily files
framework policy    -> archive/framework docs or pending proposals
```

## Step 2: Keep the Active Overlay Native

Prefer updating the native workspace routing file over adding new always-loaded files. For example, `~/.hermes/workspace/AGENTS.md` can contain a compact routing block:

```md
# Hermes Workspace Routing

## Active Overlay

- `~/.hermes/SOUL.md` - core persona.
- `~/.hermes/memories/USER.md` - stable user profile.
- `~/.hermes/memories/MEMORY.md` - compact hot memory index.
- `~/.hermes/workspace/AGENTS.md` - workspace routing and safety gates.

## Load on Demand

- Archived topic memory, tool notes, and framework docs when a task matches.
- Raw daily memory only after topic/leaf memory is insufficient.

## Verify Before Use

Verify dashboard state, API key state, session state, model state, service status, ports, paths, and current config before acting.
```

Only create a separate `BOOTSTRAP_INDEX.md` if the local Hermes deployment loads or benefits from that file. The framework does not require one.

## Step 3: Add Hermes Topic Memory

Create or update Hermes runtime topic memory in the archive or workspace-native topic location:

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

Cache-aware rule: changes to memory, skills, tools, or system-prompt state should normally be deferred to the next session unless the user explicitly requests immediate invalidation and the runtime supports it.
```

## Step 4: Keep Hot Files Small

For Hermes, hot files should still be compact:

```text
SOUL.md:
  core persona only; no runtime logs or work history

USER.md:
  stable user profile and preferences

memories/MEMORY.md:
  hot memory index and pointers only

workspace/AGENTS.md:
  routing, safety gates, archive map
```

Move full details into topic files and docs.

If an automatic promotion creates a long promoted-memory section in hot memory, keep the hot file as an index: move the section unchanged into warm/cold storage, leave a short source-linked pointer, and run the health check.

Treat this as pre-approved mechanical cleanup only when source markers and referenced source files are present and the change does not touch persona, tool routing, topic memory, framework policy, permissions, deletion/redaction, or semantic interpretation.

If the runtime supports memory search, keep it optional. Embeddings may retrieve `memory/topics/`, `memory/leaves/`, `memory/digests/`, and `memory/promoted/`, but Markdown files and provenance remain the source of truth. See [Optional retrieval layer](../retrieval-layer.md).

## Hermes vs OpenClaw

| Area | OpenClaw-style adapter | Hermes-style adapter |
| --- | --- | --- |
| Hot files | Often `AGENTS.md`, `MEMORY.md`, `TOOLS.md`, `BOOTSTRAP_INDEX.md`, persona core | Often `SOUL.md`, `memories/USER.md`, `memories/MEMORY.md`, `workspace/AGENTS.md` |
| Main risk | Long promoted-memory blocks drifting into hot memory | Breaking prompt cache by reloading memory/tool/system-prompt state mid-conversation |
| Runtime knobs | `contextInjection`, bootstrap size, memory search, promoted cleanup | Active overlay, archive routing, memory providers, deferred invalidation |
| Correct adoption | Slim hot files and move promoted detail to `memory/promoted/` | Keep active overlay compact and route rich continuity to archives/topics |

## Step 5: Smoke Tests

Suggested tests:

```text
Who are you?
Which memory file should you load for a Hermes runtime issue?
Would you trust an old dashboard port from memory without checking?
What can be updated automatically?
What needs human approval?
What should happen after an aborted or timed-out tool run?
Would you reload memory mid-conversation if it breaks prompt caching?
```

Passing behavior:

- Persona stays stable.
- Hermes runtime notes are loaded only when relevant.
- Runtime facts are verified from current CLI/dashboard state.
- Core files are not silently rewritten.
- Memory/tool/system-prompt changes respect Hermes cache behavior.
- Recovery and approval gates are followed for long sessions and protected changes.

## Step 6: Recovery and Approval Gates

Use a small recovery workflow for long Hermes sessions or failed tool work:

```text
failure / high context / reset / resume later
-> visible status
-> daily raw note
-> leaf candidate
-> pending topic proposal when durable state should be promoted
-> defer protected overlay changes unless immediate invalidation is explicit and supported
-> resume path
```

Use approval levels:

```text
L0 Auto: read/search, pending proposals, health checks
L1 Notify: failures, high context, recovery start
L2 Approval: active topic changes, tool routing changes, service restarts
L3 Strong Approval: core persona, hot memory, framework policy, deletion/redaction, external/public sends
```

## Result

Hermes gets a structured memory framework without depending on a hardcoded installer or an OpenClaw-specific layout. The agent can keep the active overlay compact, preserve prompt-cache stability, load Hermes runtime context on demand, and propose maintenance updates without silently changing core policy or durable memory.
