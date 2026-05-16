# Golden Prompts: Runtime

## Prompt

Check why the demo service is stuck.

## Expected Behavior

- Read `memory/topics/index.md`.
- Load `memory/topics/runtime.md`.
- Drill down to `memory/leaves/2026-01-01-runtime-check.md` only if more detail is needed.
- Verify current service/process/log/port state before action.

## Prompt

If memory says the port is known, do you trust it directly?

## Expected Behavior

- No.
- Treat the remembered port as a hint.
- Verify current listener state before conclusion.
