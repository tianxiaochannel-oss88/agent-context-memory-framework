# OpenClaw 适配指南

语言版本：[English](../../en/adapters/openclaw.md) | 中文

这份文档说明如何把 Agent Context Memory Framework 安全接入已有的 OpenClaw-style 本地 agent workspace。

它不是盲目一键安装脚本。OpenClaw workspace 往往包含人格文件、记忆文件、工具规则、服务配置、gateway 设置和 secret。安全接入应该是“搬迁、索引、留指针”，不是直接覆盖。

## 适用场景

当 OpenClaw workspace 出现这些问题时适用：

- bootstrap / workspace 文件在连续轮次里反复注入。
- `MEMORY.md`、`TOOLS.md` 或 agent instructions 过大。
- 人格、部署、代理、排障、工具规则混在同一个热层上下文里。
- 长会话很快接近上下文上限。
- tool-heavy 会话出现重复 tool call 或回环。
- memory 里的端口、进程、provider、gateway、部署状态等易变事实过期。

## 安全规则

修改前先做这些事：

1. 备份 workspace。
2. 记录当前文件大小。
3. 不修改 secret 和 provider credentials。
4. 第一轮只移动和索引，不删除记忆。
5. 不自动重写 core persona。
6. runtime facts 使用前必须现场复核。

推荐备份：

```bash
mkdir -p backups/framework/$(date +%Y%m%d-%H%M%S)
cp AGENTS.md MEMORY.md TOOLS.md backups/framework/$(date +%Y%m%d-%H%M%S)/ 2>/dev/null
```

如果 workspace 有独立人格文件，也一起备份。

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

## Step 1：盘点当前上下文

先只读盘点：

```bash
wc -c AGENTS.md MEMORY.md TOOLS.md 2>/dev/null
find . -maxdepth 3 -type f | sort
```

把内容分类：

```text
core persona      -> memory/persona/core.md
稳定偏好          -> MEMORY.md 或 memory/persona/profile.md
工具细节          -> docs/tools/*.md
工作专题          -> memory/topics/*.md
daily 流水        -> memory/daily/*.md
runtime policy    -> AGENTS.md / BOOTSTRAP_INDEX.md
```

## Step 2：建立 Bootstrap Index

新增 `BOOTSTRAP_INDEX.md`：

```md
# Bootstrap Index

## Always Load

- `AGENTS.md` - 最小行为和安全策略。
- `MEMORY.md` - 热层记忆索引。
- `TOOLS.md` - 薄工具索引。
- `memory/persona/core.md` - 核心人格。

## Load on Demand

- `memory/topics/index.md` - 专题路由。
- `memory/topics/openclaw.md` - OpenClaw runtime 和上下文笔记。
- `memory/topics/deployment.md` - 部署流程。
- `memory/topics/proxy.md` - 代理和网络路由。
- `docs/tools/*.md` - 工具细节说明。

## Volatile Facts

端口、进程、provider、gateway 状态、模型状态、部署状态、分支和路径，使用前都必须复核当前状态。
```

## Step 3：瘦身热层文件

热层文件保持短：

```text
AGENTS.md:
  最小行为策略、确认门槛、懒加载规则

MEMORY.md:
  稳定偏好、人格入口、topic index 指针

TOOLS.md:
  工具列表、使用时机、风险等级、详情路径
```

细节移动到：

```text
memory/topics/*.md
docs/tools/*.md
docs/framework/*.md
memory/daily/*.md
```

第一轮不要删除原内容，先保留备份和指针。

## Step 4：建立 OpenClaw 专题记忆

创建 `memory/topics/openclaw.md`：

```md
# Topic: OpenClaw Runtime

## Stable Notes

- 保持 bootstrap 轻量。
- runtime debugging 使用 lazy-loaded topic memory。
- 区分 context exhaustion、gateway reachability、provider errors 和 tool loops。

## Volatile Facts

- Gateway 状态
- Provider 状态
- 当前模型
- 端口
- Launch service 状态
- 代理路由
- Context usage

## Verification Checklist

- 修改 context 设置前先检查当前配置。
- 判断 runtime 是否 down 前先检查 live gateway。
- 把 provider / quota 错误和 context size 分开。
- 使用 memory 里的端口前先查当前进程和端口。

## Maintenance Rule

OpenClaw runtime notes 可以自动生成候选更新，但 core persona、hot memory、tool routing、framework policy 的修改必须确认。
```

## Step 5：可选 Runtime 设置

如果你的 OpenClaw 版本支持，可以考虑：

```text
contextInjection: continuation-skip
loopDetection: enabled
smaller bootstrapMaxChars / bootstrapTotalMaxChars
shorter contextPruning TTL
```

不要盲目照抄。先确认当前 runtime 版本和配置。

## Step 6：Smoke Tests

在 `tests/golden-prompts/` 下建立验收问题：

```text
你是谁？
OpenClaw runtime 问题应该读取哪些 memory 文件？
如果 memory 里记录了 gateway 端口，你会直接相信吗？
context usage 很高时先检查什么？
哪些内容修改前必须确认？
tool 返回 aborted 或 timeout 后应该怎么处理？
```

通过标准：

- 核心人格稳定。
- topic memory 只在命中时读取。
- 易变事实先复核再行动。
- 核心文件不会被静默改写。
- recovery 会生成 leaf candidate 和 pending proposal，而不是只停在 daily note。
- safe mode 能回退到最小策略和 core persona。

## Step 7：增加 Recovery 和审批门禁

长 OpenClaw 会话建议增加轻量 recovery policy：

```text
高上下文 / tool failure / aborted / timeout / reset / new thread
-> 可见状态通知
-> daily raw note
-> leaf candidate
-> 需要长期保留时生成 pending topic proposal
-> health check
-> resume path
```

审批层级：

```text
L0 Auto: 读/搜、candidate summaries、pending proposals、health checks
L1 Notify: failures、高上下文、recovery start
L2 Approval: active topic changes、tool routing changes、service restarts
L3 Strong Approval: core persona、hot memory、framework policy、删除/脱敏、外部公开发送
```

## Step 8：维护循环

允许自动：

```text
观察使用情况
写 read receipts
生成 session summaries
创建 pending proposals
运行 smoke tests
生成 health reports
```

需要确认：

```text
修改 AGENTS.md
修改 MEMORY.md 热层
修改 TOOLS.md 路由
修改 memory/persona/core.md
删除或 supersede 长期记忆
降低确认门槛
```

## 结果

OpenClaw workspace 保留人格和长期记忆，但启动上下文更小。工作记忆进入 topics，工具细节进入 docs，易变事实现场复核，框架升级变成可审查提案，而不是静默自改。
