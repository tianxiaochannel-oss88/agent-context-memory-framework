# OpenClaw Adapter Guide

Language: English | [中文](../../zh/adapters/openclaw.md)

This guide explains how to adapt the Agent Context Memory Framework to an existing OpenClaw-style local agent workspace.

It is not a blind installer. OpenClaw workspaces often contain persona files, memory files, tool rules, service configuration, gateway settings, and secrets. A safe adoption should move and index content, not overwrite it.

## When to Use This

Use this guide when an OpenClaw workspace has symptoms such as:

- Large bootstrap or workspace files being injected repeatedly.
- `MEMORY.md`, `TOOLS.md`, or agent instructions becoming too large.
- Persona instructions competing with deployment, proxy, debugging, or tool rules.
- Long-running sessions reaching high context usage.
- Tool-heavy sessions looping or producing too many repeated tool calls.
- Memory facts becoming stale, especially ports, processes, providers, gateway state, and deployment status.

## Safety Rules

Before changing anything:

1. Back up the workspace.
2. Record current file sizes.
3. Do not edit secrets or provider credentials.
4. Do not delete memory during the first pass.
5. Do not rewrite the core persona automatically.
6. Treat runtime facts as volatile and verify them live before acting.

Recommended backup:

```bash
mkdir -p backups/framework/$(date +%Y%m%d-%H%M%S)
cp AGENTS.md MEMORY.md TOOLS.md backups/framework/$(date +%Y%m%d-%H%M%S)/ 2>/dev/null
```

If the workspace has separate persona files, include them in the backup as well.

## Target Layout

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
    openclaw.md
    deployment.md
    proxy.md
    creative-workflows.md
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

## Step 1: Inventory Current Context

Create a simple inventory before editing:

```bash
wc -c AGENTS.md MEMORY.md TOOLS.md 2>/dev/null
find . -maxdepth 3 -type f | sort
```

Classify current content:

```text
core persona      -> memory/persona/core.md
stable preferences -> MEMORY.md or memory/persona/profile.md
tool details      -> docs/tools/*.md
work domains      -> memory/topics/*.md
daily logs        -> memory/daily/*.md
runtime policy    -> AGENTS.md / BOOTSTRAP_INDEX.md
```

## Step 2: Create a Bootstrap Index

Add `BOOTSTRAP_INDEX.md` as the routing map:

```md
# Bootstrap Index

## Always Load

- `AGENTS.md` - minimal behavior and safety policy.
- `MEMORY.md` - hot memory index.
- `TOOLS.md` - thin tool index.
- `memory/persona/core.md` - core persona.

## Load on Demand

- `memory/topics/index.md` - topic routing.
- `memory/topics/openclaw.md` - OpenClaw runtime and context notes.
- `memory/topics/deployment.md` - deployment workflows.
- `memory/topics/proxy.md` - proxy and network routing.
- `docs/tools/*.md` - detailed tool instructions.

## Volatile Facts

Verify current state before acting on ports, processes, providers, gateway status, model state, deployment state, branches, and paths.
```

## Step 3: Slim Hot Files

Keep hot files short:

```text
AGENTS.md:
  minimal behavior policy, confirmation gates, lazy-loading rule

MEMORY.md:
  stable preferences, persona entry point, topic index pointer

TOOLS.md:
  tool list, when to use each tool, risk level, details path
```

Move details into:

```text
memory/topics/*.md
docs/tools/*.md
docs/framework/*.md
memory/daily/*.md
```

Do not delete moved content in the first pass. Keep a backup and leave pointers.

## Step 4: Add OpenClaw Topic Memory

Create `memory/topics/openclaw.md`:

```md
# Topic: OpenClaw Runtime

## Stable Notes

- Keep bootstrap small.
- Prefer lazy-loaded topic memory for runtime debugging.
- Separate context exhaustion, gateway reachability, provider errors, and tool loops.

## Volatile Facts

- Gateway status
- Provider status
- Current model
- Ports
- Launch service state
- Proxy routing
- Context usage

## Verification Checklist

- Check current config before changing context settings.
- Check live gateway status before assuming the runtime is down.
- Check provider or quota errors before blaming context size.
- Check process and port state before using memory-derived port facts.

## Maintenance Rule

OpenClaw runtime notes may be proposed automatically, but changes to core persona, hot memory, tool routing, or framework policy require approval.
```

## Step 5: Optional Runtime Settings

If your OpenClaw version supports these settings, consider:

```text
contextInjection: continuation-skip
loopDetection: enabled
smaller bootstrapMaxChars / bootstrapTotalMaxChars
shorter contextPruning TTL
```

Do not copy these blindly. Verify your runtime version and current configuration first.

## Step 6: Smoke Tests

Create golden prompts under `tests/golden-prompts/`:

```text
Who are you?
What memory files should you load for an OpenClaw runtime issue?
If memory says the gateway is on a port, do you trust it directly?
What do you check first when context usage is high?
What needs approval before being changed?
```

Passing behavior:

- Core persona remains stable.
- Topic memory is loaded only when relevant.
- Volatile facts are verified before action.
- Core files are not silently rewritten.
- Safe mode can fall back to minimal policy plus core persona.

## Step 7: Maintenance Loop

Allow:

```text
observe usage
write read receipts
generate session summaries
create pending proposals
run smoke tests
generate health reports
```

Require approval:

```text
edit AGENTS.md
edit MEMORY.md hot layer
edit TOOLS.md routing
edit memory/persona/core.md
delete or supersede durable memory
loosen permission gates
```

## Result

The OpenClaw workspace keeps its persona and durable memory, but startup context becomes smaller. Work memory moves to topics, tool details move to docs, volatile facts are verified live, and framework upgrades become reviewable instead of silent.
