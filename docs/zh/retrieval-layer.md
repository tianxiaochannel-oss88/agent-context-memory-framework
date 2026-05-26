# 可选检索层

语言版本：[English](../en/retrieval-layer.md) | 中文

这个框架天然适合向量检索，但向量搜索是可选能力，不是硬依赖。

Markdown 文件仍然是事实来源。embedding 和 rerank 负责帮助 agent 更快找到相关记忆；它们不负责判断一条记忆是否正确、是否最新、是否已审批、是否可以安全执行。

## 在框架里的角色

```text
MEMORY.md / BOOTSTRAP_INDEX.md
  -> 薄热层索引和路由提示

memory/topics/
memory/leaves/
memory/digests/
memory/promoted/
  -> 结构化、可检索的记忆语料

embedding search
  -> 召回可能相关的文件或片段

rerank model
  -> 可选，对召回候选重新排序

source_refs / derived_from / provenance
  -> 验证这条记忆来自哪里
```

检索加速器负责“找到相关记忆”。是否可信、是否该执行，要看 provenance、review state，以及必要时的 live verification。

## 什么时候需要向量搜索

满足下面任一条件时，再考虑接入本地或远程 embedding search：

- 关键词搜索和 topic index 经常找不到相关记忆
- Markdown corpus 已经有几百到上千条 leaf/topic/digest 记录
- agent 经常跨多个专题工作，无法提前判断该读哪个 topic 文件
- 用户问题依赖模糊语义相似，而不是精确关键词

不要因为“有向量模型”就强行接入。小型 workspace 通常用 `rg`、topic index 和 Memory Tree Lite 摘要就够。

## 应该索引什么

适合索引：

- `memory/topics/*.md`
- `memory/leaves/*.md`
- `memory/digests/*.md`
- `memory/promoted/*.md`
- 经过控制的 `memory/daily/*.md`
- 需要搜索规则时的 framework docs 和 tool docs

谨慎索引：

- 原始聊天全文
- 自动生成日志
- 易变 runtime 快照
- 大型文本 dump
- 可能靠近 secret 的文件

不要把 vector search 当成读取 core persona 的唯一路径。core persona 必须能从热层索引稳定找到。

## 检索规则

```text
1. 优先从 topic / leaf / digest / promoted memory 召回候选。
2. 优先使用带 source_refs、derived_from、confidence、review_state 的记录。
3. 涉及易变 runtime facts 时，执行前必须现场复核。
4. 召回结果冲突时，优先使用较新的、已 review 的摘要；必要时向用户确认。
5. 高风险动作不能只信 embedding hit，必须打开来源文件核查。
```

rerank 可以改善排序，但 rerank 结果不是证据。它只是更好的相关性猜测。

## OpenClaw 风格配置示例

公开文档里使用占位符，不写本机路径：

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "provider": "local",
        "model": "hf:your-org/your-embedding-model.gguf"
      }
    }
  },
  "plugins": {
    "entries": {
      "memory-core": {
        "enabled": true,
        "config": {
          "dreaming": {
            "enabled": true
          }
        }
      }
    }
  }
}
```

具体配置结构取决于 runtime 版本。复制任何配置前，都要先核对当前 runtime 文档和本机配置。

## macOS 和 Windows 注意事项

公开文档保持跨平台：

- 用 `<model-id>`、`<workspace>` 这类占位符，不写绝对本机路径。
- 不提交模型缓存路径、`.dreams`、session corpus、API key 或私有 workspace memory。
- shell 示例需要区分：macOS / Linux 用 zsh/bash，Windows 用 PowerShell。
- macOS 可能使用 Metal 加速，取决于 runtime。
- Windows 可能使用 CUDA、DirectML 或 CPU fallback，取决于 runtime。
- 不假设不同系统有相同的模型缓存目录。
- Markdown 换行一般问题不大，但脚本可能需要按系统拆分。

## Health Check 可以检查什么

检索友好的 health report 可以检查：

- hot memory 是否仍然短而像索引
- 被索引文件是否带 source pointer
- core persona 是否不依赖 vector search 才能读取
- 易变事实是否标记 `verify_before_use`
- promoted hot-layer cleanup 是否保留来源注释
- 大型 recall cache 是否没有被误判为 hot context injection

## 边界

向量搜索让框架在规模变大后更好用，但它不替代：

- 薄启动上下文
- Memory Tree Lite 摘要
- provenance
- approval gates
- live verification
- recovery completion gates
