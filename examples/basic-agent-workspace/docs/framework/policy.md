# Framework Policy

## L0 Auto

- Read/search memory.
- Generate candidate summaries.
- Generate pending proposals.
- Run smoke tests.

## L1 Notify

- Tool failure, aborted run, timeout, or high context pressure.
- Recovery workflow starting.
- Ambiguous external delivery state.

## L2 Approval

- Promote leaf memory into active topic memory.
- Update active topic memory.
- Change tool routing.
- Change recurring workflow behavior.

## L3 Strong Approval

- Core persona changes.
- Hot memory changes.
- Framework policy changes.
- Permission boundary changes.
- Deleting or redacting long-term memory.
- External/public sends or destructive operations.

Generic "continue" is not enough for L3. Ask for explicit target-specific approval.

## Memory Tree Lite

- Raw records remain append-only by default.
- Leaf and topic summaries must preserve `source_refs`.
- Volatile facts require verification before action.
