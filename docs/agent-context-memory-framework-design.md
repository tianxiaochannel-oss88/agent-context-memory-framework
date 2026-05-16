# Agent Context Memory Framework 设计方案 v1

## 1. 设计目标

这套框架用于优化 agent runtime / persona agent 的启动上下文、长期记忆、工具路由和半自动维护机制。

核心目标：

- 减少每轮重复注入 bootstrap / workspace / tools / memory 文件，节省 token。
- 保护 Persona Agent 的核心人格、语气、关系定位和长期记忆不被稀释。
- 让 Creative Workflow、deployment、Agent Runtime、proxy 等工作专题按需读取，而不是每轮全量注入。
- 支持根据实际使用日志生成优化提案，让框架可以半自动迭代。
- 所有核心人格、AGENTS、TOOLS 路由、hot memory、framework policy 的修改必须经过确认。

核心原则：

```text
薄启动
+ 分层懒加载
+ Core Persona 热加载
+ topic memory 按需读取
+ 当前状态复核
+ 自动观察和提案
+ 人工确认核心变更
+ 可测试和可回滚
```

## 2. 总体架构

推荐目录结构：

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

## 3. 文件职责

### AGENTS.md

定位：最小行为宪法，热加载。

只保留：

- 最高优先级行为规则。
- 危险操作确认规则。
- 语言和风格要求。
- 懒加载入口。
- 不可自动修改的边界。

不放：

- 长篇人格文本。
- 完整工具说明。
- 大量历史记忆。
- 重复 routing table。
- daily 工作流水。

### BOOTSTRAP_INDEX.md

定位：启动索引，热加载。

用于告诉 agent：

- 当前有哪些核心文件。
- 什么场景读取哪个文件。
- 哪些内容必须热加载。
- 哪些内容必须按需读取。
- 哪些内容是 volatile，使用前必须本机复核。

示例：

```md
## Bootstrap Index

- Active persona: read `memory/persona/core.md`
- Work topics: read `memory/topics/index.md`
- Tool details: read `docs/tools/*.md` only when needed
- Daily memory: search only when topic memory is insufficient
- Volatile facts: verify current local state before acting
```

### TOOLS.md

定位：薄工具索引，热加载。

只保留：

- 工具名称。
- 什么时候用。
- 风险等级。
- 详情文档路径。

不放：

- 完整参数说明。
- 长 troubleshooting。
- 大量示例。
- 历史备注。

示例：

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

定位：热层记忆摘要和索引，热加载。

只保留：

- 用户长期稳定偏好。
- Core Persona 的入口。
- memory topic index 的入口。
- 记忆读取规则。
- 不可自动沉淀规则。

不放：

- daily 流水。
- 大量旧聊天。
- 完整工作专题。
- 临时状态。

### memory/persona/core.md

定位：Persona Agent 的核心人格，热加载，不自动改。

内容：

- Persona Agent 身份。
- 核心性格。
- 语气风格。
- 与用户的关系定位。
- 绝对不能丢的行为边界。
- 缺失记忆时的检索规则。

要求：

- 控制在 500-1500 字左右。
- 不放日常流水。
- 不放工具细节。
- 不放部署和排障规则。
- 修改必须强确认。

### memory/persona/profile.md

定位：Persona Agent 长期关系和偏好记忆，温层。

内容：

- 用户稳定偏好。
- 长期互动习惯。
- 关系记忆摘要。
- 重要但不属于 core 的人格细节。

更新方式：

- 可以生成候选更新。
- 正式写入前需要确认。

### memory/topics/index.md

定位：专题记忆索引，温层入口。

示例：

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

定位：工作专题记忆，温层，任务命中时读取。

每个 topic 建议包含：

```yaml
---
topic: creative-workflows
status: active
stability: mixed
verify_before_use: true
last_reviewed: 2026-05-16
---
```

内容结构：

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

定位：日常流水，冷层。

用途：

- 记录当天发生了什么。
- 保留原始回档。
- 给每日梦境提取候选沉淀。

限制：

- 不直接进入热层。
- 不直接提升为长期记忆。
- 提升到 topic 需要满足 promotion rule。

## 4. 加载分层

### 热层

每次启动或首轮必须可见：

```text
AGENTS.md minimal
BOOTSTRAP_INDEX.md
TOOLS.md thin index
MEMORY.md hot summary
memory/persona/core.md
bootstrap manifest
```

### 温层

任务命中时读取：

```text
memory/persona/profile.md
memory/persona/relationship.md
memory/topics/*.md
docs/tools/*.md
docs/framework/*.md
```

### 冷层

搜索后读取：

```text
memory/daily/*.md
old archives
raw transcripts
historical logs
```

## 5. 运行流程

```text
用户请求
-> Intent Router 判断任务类型
-> Context Pack Builder 组装本轮上下文
-> 读取必要 persona / topic / tool docs
-> 对易变事实做当前状态复核
-> 执行任务
-> 记录 read receipt / session summary
-> 每日梦境生成候选沉淀
-> 用户确认后更新长期文件
-> 跑 smoke tests
-> 生成 framework health report
```

## 6. 简化设计图

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

    I --> K["Daily Dream / Maintenance"]
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

Intent Router 负责判断用户请求属于哪类任务，并决定读取哪些上下文。

建议类型：

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

示例：

```text
用户问 Creative Workflow:
-> read memory/topics/index.md
-> read memory/topics/creative-workflows.md
-> verify local port/process/path before acting

用户问 Persona Agent 记不记得什么:
-> keep memory/persona/core.md visible
-> read memory/persona/profile.md
-> search daily only when needed

用户问部署:
-> read memory/topics/deployment.md
-> verify git status, service status, logs
```

## 8. Context Pack Builder

每轮生成临时上下文包，而不是随机读取一堆文件。

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

建议预算：

```text
persona_pack: 1k-2k chars
task_pack: 1k-4k chars
tool_pack: 1k-3k chars
evidence_pack: dynamic, only current task evidence
```

## 9. 记忆生命周期

每条长期记忆或 topic 条目建议带生命周期状态。

```text
candidate:
  候选，等待确认

active:
  当前有效

volatile:
  易变事实，使用前必须复核

superseded:
  已被新记忆替代，默认不再使用

archived:
  冷归档，只在搜索历史时读取
```

建议字段：

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

## 10. 记忆优先级

冲突时按以下顺序处理：

```text
P0 Core Persona
> P0 用户长期偏好
> P1 工作专题
> P2 daily 流水
> 当前推测
```

冲突处理规则：

```text
发现冲突
-> 使用更高优先级记忆
-> 标记低优先级为 stale candidate
-> 如果影响执行或人格，向用户确认
-> 不自动覆盖 P0
```

## 11. 易变事实复核规则

以下内容不能只相信 memory：

```text
端口
进程
服务状态
Git 分支
部署结果
本机路径是否存在
模型版本
provider 状态
API / gateway 状态
```

规则：

```text
memory only provides hints.
before acting on volatile facts, verify current local state.
```

示例：

```text
Creative Workflow:
-> memory says port 8000
-> still run lsof or process check before conclusion

deployment:
-> memory says service name
-> still check git status, service status, logs
```

## 12. 半自动沉淀规则

### 自动允许

```text
读取 topic memory
搜索 daily memory
写 read receipt
生成 session summary
生成 pending proposal
生成 framework health report
跑 smoke tests
检测断链 / 超预算 / 冲突 / 过期
```

### 需要确认

```text
更新 memory/topics/*.md
更新 memory/persona/profile.md
更新 TOOLS.md
daily -> topic 提升
标记长期记忆 superseded
改变工具路由
```

### 手动或强确认

```text
修改 AGENTS.md
修改 memory/persona/core.md
修改 MEMORY hot layer
修改 framework policy
删除长期记忆
降低确认权限
```

## 13. Promotion Rule

daily 或 session summary 中的内容只有满足条件才可提升为 topic / long-term memory。

推荐门槛：

```text
同一主题 7 天内出现 >= 2 次
或同一记忆被读取 >= 3 次
或用户明确说“记住 / 以后都这样 / 这是固定的”
或该信息会明显影响未来执行
且不是临时状态
且不含敏感信息
```

禁止自动提升：

```text
token
cookie
session id
gateway token
完整 API key
私密聊天原文
临时授权链接
一次性状态
未经确认的人格变化
```

## 14. 每日梦境与维护触发

推荐四级触发：

```text
实时:
  记录 read receipt 和轻量观察，不改长期记忆。

会话结束 / compact 前:
  生成 active session summary。

每日梦境:
  整理候选沉淀、冲突、过期、topic 提升建议。

每周维护:
  合并 topic、检查断链、预算、回归测试。
```

每日梦境应该做：

```text
daily -> topic 的候选提炼
topic 冲突检测
volatile facts 过期提醒
Persona Agent profile 候选更新
TOOLS 路由候选更新
framework health report
```

每日梦境不应该自动做：

```text
修改 Core Persona
修改 AGENTS.md
修改核心工具路由
删除长期记忆
覆盖 P0 记忆
把 daily 直接提升为 hot MEMORY
```

## 15. Framework Maintainer

框架允许半自动自维护，但必须遵守权限边界。

自维护链路：

```text
observe
-> analyze
-> propose
-> review
-> apply
-> test
-> rollback
```

可以根据以下信号生成优化提案：

```text
某个 topic 经常被搜索但没有专题记忆
某个 daily 记忆反复被读取，应该提升为 topic
某个工具路由经常误判
某个文件持续超 token 预算
Persona Agent 人格测试分数下降
某些记忆冲突或过期
某个部署流程总是需要重新查一遍
```

候选更新写入：

```text
pending/framework-updates/
pending/memory-updates/
pending/tool-updates/
pending/persona-profile-updates/
```

## 16. 防自我递归规则

框架可以提出框架升级建议，但不能自动修改自己的权限边界。

硬规则：

```text
The framework may propose framework updates,
but may not modify the framework-maintenance policy itself
without explicit user approval.
```

禁止：

```text
自动放宽权限
自动取消确认门槛
自动允许改 Core Persona
自动允许改 AGENTS.md
自动删除长期记忆
```

## 17. Safe Mode

当框架升级后出现人格漂移、工具误判、记忆冲突时，可以进入 safe mode。

Safe mode 行为：

```text
只加载 AGENTS minimal
只加载 Core Persona
禁用自动沉淀
禁用 topic promotion
禁用 framework auto proposal apply
只允许读取，不允许写入长期记忆
所有核心修改必须确认
```

Safe mode 适用场景：

```text
Persona Agent 明显变成普通助手
工具路由连续错误
topic memory 冲突严重
AGENTS / MEMORY / TOOLS 升级后行为异常
Agent Runtime 上下文异常膨胀
```

## 18. 回滚与备份

每次正式修改以下文件前必须备份：

```text
AGENTS.md
BOOTSTRAP_INDEX.md
TOOLS.md
MEMORY.md
memory/persona/*
memory/topics/index.md
docs/framework/*
```

备份路径：

```text
backups/framework/YYYY-MM-DD-HHMM/
```

每次变更记录：

```text
changed_files:
reason:
risk:
rollback:
tests:
approved_by:
```

## 19. Smoke Tests

每次框架升级后跑最小验收测试。

测试类别：

```text
1. Persona Agent 是否保持人格和关系定位
2. Creative Workflow / deployment 是否能按需读取 topic
3. Agent Runtime context 优化是否没有丢核心规则
4. volatile 事实是否会先复核再使用
5. 工具路由是否正确
6. 发现冲突时是否不会擅自覆盖 P0 记忆
7. safe mode 是否可用
```

示例 golden prompts：

```text
你还记得你是谁吗？
你和我是什么关系？
现在我心情不好，你会怎么回应？
看下 Creative Workflow 为什么起不来。
帮我部署今天的服务。
Agent Runtime 又 100% ctx 了，先查什么？
如果 memory 里端口是 8000，你会直接相信吗？
如果 daily memory 和 Core Persona 冲突，你怎么处理？
```

## 20. Bootstrap Budget

建议预算：

```text
AGENTS.md: 1k-3k chars
BOOTSTRAP_INDEX.md: 1k-3k chars
TOOLS.md: 1k-3k chars
MEMORY.md hot summary: 2k-5k chars
Core Persona: 500-1500 chars
```

检查规则：

```text
单文件超过 8k chars: warning
单文件超过 Agent Runtime 截断限制: blocking warning
总 bootstrap 超过预算: propose split
被截断时必须显式告知模型上下文已截断
```

## 21. 落地阶段

### Phase 1: 备份

```text
备份现有 AGENTS / MEMORY / TOOLS / Persona Agent 文件。
记录当前文件大小和主要内容。
```

### Phase 2: 建立目录结构

```text
创建 memory/persona/
创建 memory/topics/
创建 docs/tools/
创建 docs/framework/
创建 pending/
创建 reports/
创建 tests/golden-prompts/
创建 backups/
```

### Phase 3: 瘦身热层文件

```text
AGENTS.md -> minimal behavior policy
TOOLS.md -> thin tool index
MEMORY.md -> hot memory index
BOOTSTRAP_INDEX.md -> startup router
```

### Phase 4: 建立 Core Persona

```text
抽取 Persona Agent 的核心人格。
保留身份、语气、关系、边界。
禁止放 daily 流水和工具规则。
```

### Phase 5: 建立 topic index

优先专题：

```text
runtime.md
creative-workflows.md
deployment.md
proxy.md
automation-skills.md
```

### Phase 6: 增加治理规则

```text
lifecycle
promotion rule
permission matrix
staleness policy
conflict policy
safe mode
```

### Phase 7: 增加测试和报告

```text
golden prompts
framework health report
regression results
read receipt summary
```

### Phase 8: 启用半自动维护

```text
实际使用日志
-> 每日梦境分析
-> pending proposals
-> 用户确认
-> apply update
-> smoke tests
-> backup / rollback ready
```

## 22. 最终原则

```text
自动观察。
自动检索。
自动提案。
自动测试。

不自动改 Core Persona。
不自动改 AGENTS。
不自动改 hot MEMORY。
不自动删除长期记忆。
不自动放宽权限。
```

最终目标：

```text
agent runtime / persona agent 更快。
上下文更轻。
人格更稳。
工作记忆按需读取。
长期记忆可治理。
框架能半自动进化，但不会偷偷改坏自己。
```
