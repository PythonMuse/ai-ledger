# Change Review Log

This file records all proposed changes detected by the monitoring routine and their review outcomes.

---

## How to Use This Log

When the routine creates a proposed change package in `evidence/proposed-changes/`, the reviewer:

1. Opens the proposed change file
2. Reviews the detected change and recommended update
3. Records the decision below
4. If approved: updates the relevant guidance files and commits

---

## Log

| Date | Source checked | Change detected | Files impacted | Reviewer | Decision | Notes |
|---|---|---|---|---|---|---|
| [YYYY-MM-DD] | [Source name] | [Brief description] | [File names] | [Name] | Approved / Rejected / Needs research | [Notes] |

---

## Proposed Change Files

Proposed change packages are saved in `evidence/proposed-changes/` with the naming convention:

```
YYYY-MM-DD-proposed-update.md
```

Each file follows this structure:

- Date checked
- Source reviewed
- Summary of detected change
- Potential impact
- Files potentially impacted
- Recommended update
- Human review required: Yes
- Reviewer notes
- Decision: [ ] Approved  [ ] Rejected  [ ] Needs more research

---

*This log is the audit trail. Keep it updated. Commit it with every approved change.*
