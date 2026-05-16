# Agent Context Memory Framework Design v1

Language: English | [中文](../zh/agent-context-memory-framework-design.md)

## 1. Goals

This framework optimizes startup context, long-term memory, tool routing, and semi-automatic maintenance for agent runtimes and persona agents.

Core goals:

- Reduce repeated injection of bootstrap, workspace, tool, and memory files.
- Preserve the agent's core persona, tone, relationship model, and durable memory.
- Load work-domain memory only when needed instead of injecting every topic on every turn.
- Generate framework-improvement proposals from real usage logs.
- Require explicit approval before changing core persona, hot memory, tool routing, or framework policy.

Core principle:

```text
thin startup
+ layered lazy loading
+ hot core persona
+ topic memory on demand
+ fresh verification for volatile state
+ automatic observation and proposals
+ human approval for core changes
+ testable and reversible updates
```

## 2. Architecture

Recommended directory structure:

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
    creative-workflows.md
    deployment.md
    runtime.md
    proxy.md
    automation-skills.md

  daily/
    2026-xx-xx.md

docs/
  tools/
    browser.md
    shell.md
    runtime.md
    memory.md

  framework/
    policy.md
    lifecycle.md
    regression.md
    maintenance.md

pending/
  memory-updates/
  tool-updates/
  framework-updates/
  persona-profile-updates/

reports/
  framework-health.md
  regression-results.md
  memory-usage.md

tests/
  golden-prompts/
    persona.md
    tools.md
    creative-workflows.md
    deployment.md
    runtime.md

backups/
  framework/YYYY-MM-DD-HHMM/
```

## 3. File Responsibilities

### AGENTS.md

Purpose: minimal behavior constitution, hot-loaded.

Keep:

- Highest-priority behavior rules.
- Confirmation rules for dangerous operations.
- Language and style requirements.
- Lazy-loading entry points.
- Boundaries that must not be changed automatically.

Avoid:

- Long persona text.
- Full tool manuals.
- Large historical memory.
- Repeated routing tables.
- Daily work logs.

### BOOTSTRAP_INDEX.md

Purpose: startup router, hot-loaded.

It tells the agent:

- Which core files exist.
- Which file to read for each scenario.
- Which content must stay hot-loaded.
- Which content should be read on demand.
- Which facts are volatile and must be verified before use.

Example:

```md
## Bootstrap Index

- Active persona: read `memory/persona/core.md`
- Work topics: read `memory/topics/index.md`
- Tool details: read `docs/tools/*.md` only when needed
- Daily memory: search only when topic memory is insufficient
- Volatile facts: verify current local state before acting
```

### TOOLS.md

Purpose: thin tool index, hot-loaded.

Keep:

- Tool name.
- When to use it.
- Risk level.
- Link to detailed documentation.

Avoid:

- Full parameter manuals.
- Long troubleshooting sections.
- Large examples.
- Historical notes.

Example:

```md
## shell

Use when:
- local files
- process inspection
- ports
- logs
- build and tests

Risk:
- destructive commands require confirmation

Details:
- docs/tools/shell.md
```

### MEMORY.md

Purpose: hot-layer memory summary and index.

Keep:

- Stable long-term user preferences.
- Entry point for the core persona file.
- Entry point for the topic memory index.
- Memory read rules.
- Rules for what must not be auto-promoted.

Avoid:

- Daily logs.
- Large old conversations.
- Complete work-domain memory.
- Temporary state.

### memory/persona/core.md

Purpose: core persona, hot-loaded, never changed silently.

It should contain:

- Agent identity.
- Core personality.
- Tone and style.
- Relationship model with the user.
- Non-negotiable behavior boundaries.
- Retrieval rule when memory is missing.

Guidelines:

- Keep it around 500-1500 words.
- Do not include daily logs.
- Do not include tool details.
- Do not include deployment or debugging rules.
- Require strong confirmation before editing.

### memory/persona/profile.md

Purpose: long-term relationship and preference memory, warm-loaded.

It may contain:

- Stable user preferences.
- Long-term interaction habits.
- Relationship memory summary.
- Important persona details that do not belong in the core file.

Updates:

- Candidate updates can be generated automatically.
- Formal writes require approval.

### memory/topics/index.md

Purpose: topic memory index, warm-layer entry point.

Example:

```md
# Topic Memory Index

- `creative-workflows.md`
  - Keywords: Creative Workflow, port 8000, model path, workflow, image generation
  - Rule: verify port and process state before acting

- `deployment.md`
  - Keywords: deploy, restart, release, service, rollback
  - Rule: verify git status, service state, logs before acting

- `runtime.md`
  - Keywords: Agent Runtime, gateway, context, chat platform, agent, continuation-skip
  - Rule: verify current local config and runtime status before acting
```

### memory/topics/*.md

Purpose: work-domain memory, warm-loaded only when matched.

Suggested front matter:

```yaml
---
topic: creative-workflows
status: active
stability: mixed
verify_before_use: true
last_reviewed: 2026-05-16
---
```

Suggested body:

```md
# Topic: Creative Workflow

## Stable Facts

## Volatile Facts

## Common Commands

## Known Failure Modes

## Verification Checklist

## Source / Evidence
```

### memory/daily/*.md

Purpose: daily logs, cold layer.

Use for:

- Recording what happened during the day.
- Preserving raw session history.
- Feeding daily maintenance and candidate extraction.

Limits:

- Do not inject directly into the hot layer.
- Do not promote directly into long-term memory.
- Promote into topic memory only through promotion rules.

## 4. Loading Layers

### Hot Layer

Visible on startup or the first turn:

```text
AGENTS.md minimal
BOOTSTRAP_INDEX.md
TOOLS.md thin index
MEMORY.md hot summary
memory/persona/core.md
bootstrap manifest
```

### Warm Layer

Loaded when the task matches:

```text
memory/persona/profile.md
memory/persona/relationship.md
memory/topics/*.md
docs/tools/*.md
docs/framework/*.md
```

### Cold Layer

Searched before reading:

```text
memory/daily/*.md
old archives
raw transcripts
historical logs
```

## 5. Runtime Flow

```text
User request
-> Intent Router classifies the task
-> Context Pack Builder assembles turn-specific context
-> Load required persona / topic / tool docs
-> Verify volatile facts with current state
-> Execute the task
-> Record read receipt / session summary
-> Daily maintenance generates candidate updates
-> User approval promotes long-term changes
-> Run smoke tests
-> Generate framework health report
```

## 6. Simplified Design Diagram

```mermaid
flowchart TD
    A["User Request"] --> B["Intent Router"]
    B --> C["Context Pack Builder"]

    C --> D["Persona Pack<br/>Core Persona"]
    C --> E["Task Pack<br/>Topic Memory"]
    C --> F["Tool Pack<br/>TOOLS Index + Docs"]
    C --> G["Evidence Pack<br/>Local Verification"]

    D --> H["Agent Runtime"]
    E --> H
    F --> H
    G --> H

    H --> I["Read Receipt<br/>Usage Logs"]
    H --> J["Session Summary"]

    I --> K["Daily Maintenance"]
    J --> K

    K --> L["Pending Proposals"]
    L --> M{"User Approval?"}

    M -->|Yes| N["Apply Update<br/>with Backup"]
    M -->|No| O["Keep as Candidate"]

    N --> P["Smoke Tests"]
    P --> Q["Framework Health Report"]

    N -. rollback .-> R["Safe Mode / Backup Restore"]
```

## 7. Intent Router

The Intent Router classifies the user's request and decides which context to read.

Suggested intent types:

```text
persona_continuity
local_debugging
runtime_context
creative_workflow
deployment_ops
proxy_network
coding_task
document_analysis
framework_maintenance
```

Examples:

```text
Creative Workflow request:
-> read memory/topics/index.md
-> read memory/topics/creative-workflows.md
-> verify local port/process/path before acting

Persona memory question:
-> keep memory/persona/core.md visible
-> read memory/persona/profile.md
-> search daily only when needed

Deployment request:
-> read memory/topics/deployment.md
-> verify git status, service status, logs
```

## 8. Context Pack Builder

Each turn should create a temporary context pack instead of reading many files randomly.

```text
persona_pack:
  - Core Persona
  - active relationship summary

task_pack:
  - matched topic memory
  - active session summary

tool_pack:
  - TOOLS thin index
  - specific tool docs if needed

evidence_pack:
  - current local verification
  - fresh command output
  - current file state
```

Suggested budget:

```text
persona_pack: 1k-2k chars
task_pack: 1k-4k chars
tool_pack: 1k-3k chars
evidence_pack: dynamic, only current task evidence
```

## 9. Memory Lifecycle

Each long-term memory or topic entry should have a lifecycle status.

```text
candidate:
  proposed, waiting for confirmation

active:
  currently valid

volatile:
  likely to change, must be verified before use

superseded:
  replaced by newer memory, not used by default

archived:
  cold archive, read only during historical search
```

Suggested metadata:

```yaml
status: active
priority: P1
stability: stable
verify_before_use: false
created_at: 2026-05-16
updated_at: 2026-05-16
source: memory/daily/2026-05-16.md
confidence: high
supersedes: null
```

## 10. Memory Priority

When memories conflict, resolve by priority:

```text
P0 Core Persona
> P0 stable user preference
> P1 work topic memory
> P2 daily log
> current inference
```

Conflict handling:

```text
detect conflict
-> use higher-priority memory
-> mark lower-priority memory as stale candidate
-> ask the user if the conflict affects execution or persona
-> never overwrite P0 automatically
```

## 11. Volatile-Fact Verification

Do not rely on memory alone for:

```text
ports
processes
service status
git branch
deployment result
local path existence
model version
provider status
API / gateway status
```

Rule:

```text
memory only provides hints.
before acting on volatile facts, verify current local state.
```

Examples:

```text
Creative Workflow:
-> memory says port 8000
-> still run lsof or process check before conclusion

deployment:
-> memory says service name
-> still check git status, service status, logs
```

## 12. Semi-Automatic Consolidation Rules

### Automatically Allowed

```text
read topic memory
search daily memory
write read receipt
generate session summary
generate pending proposal
generate framework health report
run smoke tests
detect broken links / over-budget files / conflicts / stale memory
```

### Requires Confirmation

```text
update memory/topics/*.md
update memory/persona/profile.md
update TOOLS.md
promote daily memory into topic memory
mark long-term memory as superseded
change tool routing
```

### Manual or Strong Confirmation

```text
modify AGENTS.md
modify memory/persona/core.md
modify MEMORY hot layer
modify framework policy
delete long-term memory
lower confirmation requirements
```

## 13. Promotion Rule

Content from daily logs or session summaries may be promoted only when it meets clear criteria.

Recommended threshold:

```text
same topic appears >= 2 times within 7 days
or same memory is read >= 3 times
or user explicitly says "remember this" / "always do this" / "this is fixed"
or the information clearly affects future execution
and it is not temporary state
and it does not contain sensitive information
```

Never auto-promote:

```text
token
cookie
session id
gateway token
full API key
private chat transcript
temporary authorization link
one-time state
unconfirmed persona change
```

## 14. Daily Maintenance Triggers

Recommended four-level trigger model:

```text
real-time:
  record read receipts and lightweight observations, do not change long-term memory.

session end / before compaction:
  generate active session summary.

daily maintenance:
  prepare candidate consolidations, conflicts, stale facts, and topic promotion proposals.

weekly maintenance:
  merge topics, check broken links, budgets, and regression tests.
```

Daily maintenance should:

```text
extract daily -> topic candidates
detect topic conflicts
flag expired volatile facts
propose persona profile updates
propose TOOLS routing updates
generate framework health report
```

Daily maintenance should not:

```text
modify Core Persona
modify AGENTS.md
modify core tool routing
delete long-term memory
overwrite P0 memory
promote daily logs directly into hot MEMORY
```

## 15. Framework Maintainer

The framework may maintain itself semi-automatically, but must respect permission boundaries.

Maintenance flow:

```text
observe
-> analyze
-> propose
-> review
-> apply
-> test
-> rollback
```

Signals that can create optimization proposals:

```text
a topic is searched often but has no topic memory
a daily memory is read repeatedly and should become topic memory
a tool route is often misclassified
a file keeps exceeding the token budget
persona stability tests degrade
memories conflict or expire
a deployment flow always requires the same rediscovery
```

Candidate update locations:

```text
pending/framework-updates/
pending/memory-updates/
pending/tool-updates/
pending/persona-profile-updates/
```

## 16. Anti-Recursion Rule

The framework may propose framework upgrades, but it must not silently change its own permission boundaries.

Hard rule:

```text
The framework may propose framework updates,
but may not modify the framework-maintenance policy itself
without explicit user approval.
```

Forbidden:

```text
automatically loosening permissions
automatically removing confirmation gates
automatically allowing Core Persona edits
automatically allowing AGENTS.md edits
automatically deleting long-term memory
```

## 17. Safe Mode

Safe mode is used when framework updates cause persona drift, tool misrouting, or memory conflicts.

Safe mode behavior:

```text
load only minimal AGENTS
load only Core Persona
disable automatic consolidation
disable topic promotion
disable automatic application of framework proposals
allow read-only memory lookup only
require confirmation for all core changes
```

Safe mode triggers:

```text
persona agent becomes a generic assistant
tool routing fails repeatedly
topic memory conflicts heavily
AGENTS / MEMORY / TOOLS update causes abnormal behavior
agent runtime context grows unexpectedly
```

## 18. Rollback and Backup

Back up before formally changing:

```text
AGENTS.md
BOOTSTRAP_INDEX.md
TOOLS.md
MEMORY.md
memory/persona/*
memory/topics/index.md
docs/framework/*
```

Backup path:

```text
backups/framework/YYYY-MM-DD-HHMM/
```

Change record:

```text
changed_files:
reason:
risk:
rollback:
tests:
approved_by:
```

## 19. Smoke Tests

Run minimal acceptance tests after each framework upgrade.

Test categories:

```text
1. Persona identity and relationship model remain stable
2. Creative workflows / deployment can load topic memory on demand
3. Runtime context optimization does not drop core rules
4. Volatile facts are verified before use
5. Tool routing is correct
6. Conflicts do not silently overwrite P0 memory
7. Safe mode works
```

Example golden prompts:

```text
Do you remember who you are?
What is our relationship?
How would you respond if I feel bad today?
Check why my creative workflow cannot start.
Deploy today's service.
The agent runtime is at 100% context again. What do you check first?
If memory says the port is 8000, do you trust it directly?
What do you do if daily memory conflicts with Core Persona?
```

## 20. Bootstrap Budget

Suggested budget:

```text
AGENTS.md: 1k-3k chars
BOOTSTRAP_INDEX.md: 1k-3k chars
TOOLS.md: 1k-3k chars
MEMORY.md hot summary: 2k-5k chars
Core Persona: 500-1500 chars
```

Checks:

```text
single file over 8k chars: warning
single file over runtime truncation limit: blocking warning
total bootstrap over budget: propose split
when truncation occurs, explicitly tell the model that context was truncated
```

## 21. Implementation Phases

### Phase 1: Backup

```text
Back up existing AGENTS / MEMORY / TOOLS / persona files.
Record current file sizes and main content.
```

### Phase 2: Create Directory Structure

```text
create memory/persona/
create memory/topics/
create docs/tools/
create docs/framework/
create pending/
create reports/
create tests/golden-prompts/
create backups/
```

### Phase 3: Slim Hot-Layer Files

```text
AGENTS.md -> minimal behavior policy
TOOLS.md -> thin tool index
MEMORY.md -> hot memory index
BOOTSTRAP_INDEX.md -> startup router
```

### Phase 4: Create Core Persona

```text
Extract the persona agent's core identity.
Keep identity, tone, relationship model, and boundaries.
Do not include daily logs or tool rules.
```

### Phase 5: Create Topic Index

Priority topics:

```text
runtime.md
creative-workflows.md
deployment.md
proxy.md
automation-skills.md
```

### Phase 6: Add Governance Rules

```text
lifecycle
promotion rule
permission matrix
staleness policy
conflict policy
safe mode
```

### Phase 7: Add Tests and Reports

```text
golden prompts
framework health report
regression results
read receipt summary
```

### Phase 8: Enable Semi-Automatic Maintenance

```text
real usage logs
-> daily maintenance analysis
-> pending proposals
-> user approval
-> apply update
-> smoke tests
-> backup / rollback ready
```

## 22. Final Rule

```text
observe automatically.
retrieve automatically.
propose automatically.
test automatically.

do not automatically change Core Persona.
do not automatically change AGENTS.
do not automatically change hot MEMORY.
do not automatically delete long-term memory.
do not automatically loosen permissions.
```

Final outcome:

```text
faster agent runtime.
lighter context.
more stable persona.
work memory loaded on demand.
governable long-term memory.
self-improving framework that cannot silently damage itself.
```
