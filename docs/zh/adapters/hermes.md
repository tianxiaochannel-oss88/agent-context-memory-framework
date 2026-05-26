# Hermes 适配指南

语言版本：[English](../../en/adapters/hermes.md) | 中文

这份文档说明如何把 Agent Context Memory Framework 接入 Hermes-style 本地 agent setup。

Hermes 的安装形态可能随版本和部署方式不同而变化，所以这里提供的是安全整理清单，不是通用一键安装脚本。

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

## 目标结构

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

## Step 1：映射现有 Hermes 文件

先只读发现：

```bash
pwd
find . -maxdepth 3 -type f | sort
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
core persona       -> memory/persona/core.md
稳定偏好           -> MEMORY.md 或 memory/persona/profile.md
Hermes runtime notes -> memory/topics/hermes.md
工具细节           -> docs/tools/*.md
daily 流水         -> memory/daily/*.md
framework policy   -> docs/framework/*.md
```

## Step 2：建立 Bootstrap Index

创建 `BOOTSTRAP_INDEX.md`：

```md
# Bootstrap Index

## Always Load

- `AGENTS.md` - 最小行为和安全策略。
- `MEMORY.md` - 热层记忆索引。
- `TOOLS.md` - 薄工具索引。
- `memory/persona/core.md` - 核心人格。

## Load on Demand

- `memory/topics/index.md` - topic router。
- `memory/topics/hermes.md` - Hermes runtime notes。
- `memory/topics/deployment.md` - 部署或服务操作。
- `docs/tools/*.md` - 工具细节。

## Verify Before Use

dashboard 状态、API key 状态、session 状态、model 状态、service 状态、端口、路径和当前 config，使用前必须复核。
```

## Step 3：建立 Hermes 专题记忆

创建 `memory/topics/hermes.md`：

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
```

## Step 4：保持热层文件轻量

Hermes 也应保持热层文件短小：

```text
AGENTS.md:
  最小行为、确认边界、懒加载规则

MEMORY.md:
  稳定偏好、人格入口、topic index 指针

TOOLS.md:
  只保留工具索引和风险等级
```

完整细节放进 topic 文件和 docs。

如果自动 promotion 在 `MEMORY.md` 里生成很长的 promoted-memory section，仍要保持 hot file 是索引：把该 section 原样移动到 `memory/promoted/`，在 hot memory 里只留短 source-linked pointer，然后运行 health check。

只有来源标记和引用源文件都存在，且不触碰 persona、tool routing、topic memory、framework policy、权限、删除/脱敏或语义解释时，才把它视为预批准的机械清理。

## Step 5：Smoke Tests

建议测试：

```text
你是谁？
Hermes runtime 问题应该读取哪个 memory 文件？
你会不检查就相信旧 dashboard 端口吗？
哪些内容可以自动更新？
哪些内容必须人工确认？
tool aborted 或 timeout 后应该怎么处理？
```

通过标准：

- Persona 稳定。
- Hermes runtime notes 只在相关任务里读取。
- Runtime facts 来自当前 CLI/dashboard 状态复核。
- 核心文件不会被静默改写。
- 长会话和受保护变更遵守 recovery 与审批门禁。

## Step 6：Recovery 和审批门禁

长 Hermes 会话或工具失败时使用轻量 recovery workflow：

```text
failure / high context / reset / resume later
-> 可见状态通知
-> daily raw note
-> leaf candidate
-> 需要长期保留时生成 pending topic proposal
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

Hermes 可以获得结构化 memory framework，而不依赖硬编码安装器。Agent 能保持人格稳定，按需加载 Hermes runtime context，并提出维护建议，而不会静默修改核心策略或长期记忆。
