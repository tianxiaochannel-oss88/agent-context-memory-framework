# Optional Retrieval Layer

Language: English | [中文](../zh/retrieval-layer.md)

The framework is vector-friendly by design, but vector search is optional.

Markdown files remain the source of truth. Embeddings and rerankers help the agent find relevant memory faster; they do not decide whether a memory is correct, current, approved, or safe to use.

## Role in the Framework

```text
MEMORY.md / BOOTSTRAP_INDEX.md
  -> thin hot index and routing hints

memory/topics/
memory/leaves/
memory/digests/
memory/promoted/
  -> structured searchable memory corpus

embedding search
  -> retrieves likely relevant files or snippets

rerank model
  -> optionally reorders retrieved candidates

source_refs / derived_from / provenance
  -> verifies where the retrieved memory came from
```

Use retrieval acceleration to find the right memory. Use provenance, review state, and live verification to decide whether the memory is trustworthy enough for action.

## When to Add Vector Search

Add local or remote embedding search when at least one condition is true:

- keyword search and topic indexes miss relevant memory too often
- the Markdown corpus has hundreds or thousands of leaf/topic/digest records
- the agent frequently works across many topics and cannot predict the right topic file
- users ask questions that depend on fuzzy similarity rather than exact keywords

Do not add vector search just because it is available. For small workspaces, `rg`, topic indexes, and Memory Tree Lite summaries are usually enough.

## What to Index

Good candidates:

- `memory/topics/*.md`
- `memory/leaves/*.md`
- `memory/digests/*.md`
- `memory/promoted/*.md`
- selected `memory/daily/*.md` records when daily logs are not too noisy
- framework docs and tool docs when the agent must search operating rules

Be conservative with:

- raw chat transcripts
- generated logs
- volatile runtime snapshots
- large binary-derived text dumps
- secret-adjacent files

Do not rely on vector search as the only path to core persona. Keep core persona reachable from the hot index.

## Retrieval Rules

```text
1. Retrieve candidates from topic/leaf/digest/promoted memory.
2. Prefer entries with source_refs, derived_from, confidence, and review_state.
3. For volatile runtime facts, verify live before action.
4. If retrieved memories conflict, prefer newer reviewed summaries or ask for confirmation.
5. If the action is risky, inspect the source file instead of trusting the embedding hit.
```

Reranking can improve ordering, but rerank output is not proof. It is only a better guess about relevance.

## OpenClaw-Style Example

Use placeholders, not local machine paths:

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

The exact schema depends on the runtime version. Verify the current runtime documentation and configuration before copying any setting.

## macOS and Windows Notes

Keep public docs platform-neutral:

- Use placeholders such as `<model-id>` or `<workspace>` instead of absolute local paths.
- Do not commit model cache paths, `.dreams`, session corpora, API keys, or private workspace memory.
- Document shell examples separately when needed: zsh/bash for macOS and Linux, PowerShell for Windows.
- macOS setups may use Metal acceleration depending on the runtime.
- Windows setups may use CUDA, DirectML, or CPU fallback depending on the runtime.
- Avoid assuming the same model cache directory across systems.
- Keep Markdown line endings stable; scripts may need OS-specific variants.

## Health Checks

A retrieval-aware health report can check:

- hot memory remains short and index-like
- indexed files include source pointers
- core persona is not dependent on vector search
- volatile facts are marked `verify_before_use`
- promoted hot-layer cleanup preserves source comments
- large recall caches are not confused with hot context injection

## Boundary

Vector search makes the framework easier to use at scale. It does not replace:

- thin startup context
- Memory Tree Lite summaries
- provenance
- approval gates
- live verification
- recovery completion gates
