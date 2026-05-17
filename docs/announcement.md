# Agent Context Memory Framework Announcement Variants

## 30-second version

Long-running AI agents do not just need bigger context windows. They need context hygiene.

Agent Context Memory Framework is a lightweight reference design for durable agents: thin startup, hot core persona, lazy-loaded topic memory, searchable archives, provenance-aware summaries, live verification for volatile facts, and human-reviewed self-evolution.

Repository: https://github.com/tianxiaochannel-oss88/agent-context-memory-framework

## Maintainer version

We have been experimenting with a context and memory hygiene pattern for long-running agents.

The core idea is to keep startup context thin while preserving durable memory:

- Hot layer: minimal behavior policy, core persona, memory index, tool index.
- Warm layer: topic memory, profile notes, detailed tool docs.
- Cold layer: daily logs, archives, transcripts, raw evidence.
- Evidence layer: live verification for volatile facts such as ports, processes, provider state, deployment state, and runtime configuration.

The safety boundary is important: agents may observe usage and create pending improvement proposals, but they should not silently rewrite core persona, hot memory, tool routing, permission boundaries, or framework policy.

This is not proposed as a mandatory runtime. It is a reference design, templates, and non-destructive adapter guidance for durable agent workspaces.

Repository: https://github.com/tianxiaochannel-oss88/agent-context-memory-framework

## 中文短版

长期运行的 AI Agent 不只是需要更大的上下文窗口，更需要上下文卫生。

Agent Context Memory Framework 是一个轻量参考设计：薄启动、核心人格热加载、专题记忆按需读取、冷层归档可搜索、摘要保留来源、易变事实现场复核，并且核心人格/记忆/工具路由/策略的演化必须走人工确认。

它不是强制 runtime，也不是一键安装器，而是一套可渐进采用的目录结构、模板、安全边界和适配指南。

仓库：
https://github.com/tianxiaochannel-oss88/agent-context-memory-framework

## OpenClaw-facing short note

I have a small reference design for long-running agent context/memory hygiene that may be relevant to OpenClaw documentation or future optional conventions.

It focuses on keeping startup context thin, preserving core persona, lazy-loading topic memory/tool docs, verifying volatile runtime facts live, and requiring human review before agents modify high-risk layers such as persona, hot memory, tool routing, or framework policy.

I do not think this needs to be a mandatory runtime feature. It may be useful as a docs pattern or prior art for durable personal agents.

Reference: https://github.com/tianxiaochannel-oss88/agent-context-memory-framework
