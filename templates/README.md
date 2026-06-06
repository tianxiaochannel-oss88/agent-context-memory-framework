# Templates

Copy these files into an agent workspace and replace placeholder values.

They are intentionally generic. They should not be used to overwrite existing persona, memory, or tool files without a backup and review.

## Files

- `AGENTS.md` - minimal behavior policy.
- `BOOTSTRAP_INDEX.md` - startup context router.
- `MEMORY.md` - hot memory index.
- `TOOLS.md` - thin tool index.
- `persona-core.md` - core persona template.
- `topic-memory.md` - topic memory template.
- `leaf-summary.md` - Memory Tree Lite leaf summary template.
- `global-digest.md` - project/global digest template.
- `self-improving-index.md` - warm correction/reflection lane router.
- `self-improving-corrections.md` - explicit user correction record template.
- `self-improving-reflections.md` - post-task reflection record template.
- `framework-policy.md` - approval gates and protected-change policy.
- `recovery-workflow.md` - recovery trigger checklist for long context, failures, and handoffs.
- `framework-health-report.md` - framework health report template.

Optional retrieval guidance is documented in `docs/en/retrieval-layer.md` and `docs/zh/retrieval-layer.md`. It is not a template file because model IDs, cache paths, and acceleration backends are runtime- and OS-specific.
