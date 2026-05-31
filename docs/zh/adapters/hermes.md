# Hermes 适配指南

语言版本：[English](../../en/adapters/hermes.md) | 中文

这份文档说明如何把 Agent Context Memory Framework 接入 Hermes-style 本地 agent setup。

Hermes 的安装形态可能随版本和部署方式不同而变化，所以这里提供的是安全整理清单，不是通用一键安装脚本。

不要强行让 Hermes 复制 OpenClaw-style 文件布局。框架层级应映射到 Hermes 的 active overlay 模型：紧凑 identity、user profile、hot memory index、workspace routing 和 archived detail。

## 适用场景

当 Hermes setup 出现这些情况时适用：

- instruction 或 memory 文件过大。
- persona、tool、workflow、runtime notes 混在一起。
- 启动上下文重复注入或响应变慢。
- dashboard URL、API key 状态、session 状态、model 状态、workspace path 等本地事实过期。
- 需要可控的记忆沉淀和人工确认的框架升级。

## 先确认当前 Hermes Runtime

修改文件前先确认本机安装态：

```bash
which hermes
hermes --help
hermes dashboard --help
```

如果 dashboard 命令可用，常见本地入口是：

```bash
hermes dashboard
```

dashboard 可能用于配置、API key 和 session 管理。不要只凭 memory 相信路径或端口，先看当前版本和 help 输出。

## 安全规则

1. 备份现有 instruction、memory 和 config 文件。
2. 框架接入期间不要修改 API key 或 secret。
3. 不假设默认 workspace path。
4. 不自动重写 persona 或长期记忆。
5. 记录 runtime facts 前先复核当前 Hermes config 和 dashboard 行为。
6. adapter 变更先进入 pending proposals，确认后再应用。
7. 除非 runtime 提供明确的 immediate invalidation 路径，否则不要在会话中途 reload memories、重建 system prompt 或改变 toolsets。优先让变更延迟到下一 session 生效。

## 层级映射

把框架层级映射到当前 Hermes runtime 实际使用的文件。常见本地 active overlay 是：

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

如果某个 Hermes workspace 已经使用 `AGENTS.md`、`BOOTSTRAP_INDEX.md`、`TOOLS.md`、`MEMORY.md`，通用框架布局仍然有效。如果它使用 `SOUL.md`、`USER.md`、`memories/MEMORY.md` 和 workspace routing，就保持 Hermes 原生形态，只记录映射关系。

## Step 1：映射现有 Hermes 文件

先只读发现：

```bash
hermes_home="${HERMES_HOME:-$HOME/.hermes}"
find "$hermes_home" -maxdepth 3 -type f \
  \( -name 'SOUL.md' -o -name 'USER.md' -o -name 'MEMORY.md' -o -name 'AGENTS.md' \) \
  | sort
```

如果当前不在 Hermes workspace，不要猜路径，先检查已安装 CLI：

```bash
which hermes
hermes --version 2>/dev/null || true
hermes --help
hermes dashboard --help
```

分类内容：

```text
core persona        -> ~/.hermes/SOUL.md，或自定义 workspace 里的 memory/persona/core.md
稳定偏好            -> ~/.hermes/memories/USER.md，或 compact hot/profile 文件
hot memory index    -> ~/.hermes/memories/MEMORY.md
workspace routing   -> ~/.hermes/workspace/AGENTS.md
Hermes runtime notes -> archive/topic files，例如 memory/topics/hermes.md
工具细节            -> archive/tool docs，不进 hot memory
daily/raw notes     -> archive/raw memory 或 daily files
framework policy    -> archive/framework docs 或 pending proposals
```

## Step 2：保持 Active Overlay 原生

优先更新 Hermes 原生 workspace routing 文件，而不是新增 always-loaded 文件。例如，`~/.hermes/workspace/AGENTS.md` 可以包含紧凑 routing block：

```md
# Hermes Workspace Routing

## Active Overlay

- `~/.hermes/SOUL.md` - core persona。
- `~/.hermes/memories/USER.md` - stable user profile。
- `~/.hermes/memories/MEMORY.md` - compact hot memory index。
- `~/.hermes/workspace/AGENTS.md` - workspace routing and safety gates。

## Load on Demand

- 任务命中时读取 archived topic memory、tool notes 和 framework docs。
- topic/leaf memory 不足时再读 raw daily memory。

## Verify Before Use

dashboard 状态、API key 状态、session 状态、model 状态、service 状态、端口、路径和当前 config，使用前必须复核。
```

只有当本地 Hermes deployment 会加载或受益于 `BOOTSTRAP_INDEX.md` 时，才创建单独的 `BOOTSTRAP_INDEX.md`。框架不强制要求这个文件。

## Step 3：建立 Hermes 专题记忆

在 archive 或 workspace 原生 topic 位置创建/更新 Hermes runtime topic memory：

```md
# Topic: Hermes Runtime

## Stable Notes

- 使用 Hermes CLI 或 dashboard help 发现当前能力。
- Hermes runtime notes 与 core persona / hot memory 分离。
- dashboard URL、session 状态、model 状态、API key 状态都属于易变事实。

## Volatile Facts

- installed binary path
- dashboard command availability
- dashboard URL and port
- API key state
- session state
- workspace path
- model/provider state

## Verification Checklist

- 运行 `which hermes`。
- 运行 `hermes --help`。
- dashboard 相关问题运行 `hermes dashboard --help`。
- 写入设置前通过官方 UI 或 CLI 检查当前 config。

## Maintenance Rule

Hermes runtime notes 可以自动生成候选更新，但 core persona、hot memory、tool routing、framework policy 的修改必须确认。

Cache-aware rule: memory、skills、tools 或 system-prompt state 变更通常应延迟到下一 session，除非用户明确要求 immediate invalidation 且 runtime 支持。
```

## Step 4：保持热层文件轻量

Hermes 也应保持热层文件短小：

```text
SOUL.md:
  只放 core persona，不放 runtime logs 或工作历史

USER.md:
  稳定用户 profile 和偏好

memories/MEMORY.md:
  只放 hot memory index 和指针

workspace/AGENTS.md:
  routing、安全门禁、archive map
```

完整细节放进 topic 文件和 docs。

如果自动 promotion 在 hot memory 里生成很长的 promoted-memory section，仍要保持 hot file 是索引：把该 section 原样移动到 warm/cold storage，在 hot memory 里只留短 source-linked pointer，然后运行 health check。

只有来源标记和引用源文件都存在，且不触碰 persona、tool routing、topic memory、framework policy、权限、删除/脱敏或语义解释时，才把它视为预批准的机械清理。

如果 runtime 支持 memory search，也保持可选。embedding 可以召回 `memory/topics/`、`memory/leaves/`、`memory/digests/` 和 `memory/promoted/`，但 Markdown 文件和 provenance 仍然是事实来源。详见：[可选检索层](../retrieval-layer.md)。

## Hermes vs OpenClaw

| Area | OpenClaw-style adapter | Hermes-style adapter |
| --- | --- | --- |
| Hot files | 常见为 `AGENTS.md`、`MEMORY.md`、`TOOLS.md`、`BOOTSTRAP_INDEX.md`、persona core | 常见为 `SOUL.md`、`memories/USER.md`、`memories/MEMORY.md`、`workspace/AGENTS.md` |
| Main risk | 长 promoted-memory block 漂进 hot memory | 会话中途 reload memory/tool/system-prompt state 破坏 prompt cache |
| Runtime knobs | `contextInjection`、bootstrap size、memory search、promoted cleanup | active overlay、archive routing、memory providers、deferred invalidation |
| Correct adoption | 瘦身 hot files，把 promoted detail 移到 `memory/promoted/` | 保持 active overlay 紧凑，把 rich continuity 路由到 archives/topics |

## Step 5：Smoke Tests

建议测试：

```text
你是谁？
Hermes runtime 问题应该读取哪个 memory 文件？
你会不检查就相信旧 dashboard 端口吗？
哪些内容可以自动更新？
哪些内容必须人工确认？
tool aborted 或 timeout 后应该怎么处理？
如果会破坏 prompt cache，你会在会话中途 reload memory 吗？
```

通过标准：

- Persona 稳定。
- Hermes runtime notes 只在相关任务里读取。
- Runtime facts 来自当前 CLI/dashboard 状态复核。
- 核心文件不会被静默改写。
- memory/tool/system-prompt 变更遵守 Hermes cache 行为。
- 长会话和受保护变更遵守 recovery 与审批门禁。

## Step 6：Recovery 和审批门禁

长 Hermes 会话或工具失败时使用轻量 recovery workflow：

```text
failure / high context / reset / resume later
-> 可见状态通知
-> daily raw note
-> leaf candidate
-> 需要长期保留时生成 pending topic proposal
-> protected overlay changes 默认 defer，除非 immediate invalidation 被明确要求且受支持
-> resume path
```

审批层级：

```text
L0 Auto: 读/搜、pending proposals、health checks
L1 Notify: failures、高上下文、recovery start
L2 Approval: active topic changes、tool routing changes、service restarts
L3 Strong Approval: core persona、hot memory、framework policy、删除/脱敏、外部公开发送
```

## 结果

Hermes 可以获得结构化 memory framework，而不依赖硬编码安装器，也不依赖 OpenClaw-specific layout。Agent 能保持 active overlay 紧凑、保护 prompt-cache stability、按需加载 Hermes runtime context，并提出维护建议，而不会静默修改核心策略或长期记忆。
