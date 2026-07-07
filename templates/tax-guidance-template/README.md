# Tax Guidance Template

This template is a companion to [Article 30 — AI Routines for Accountants](https://github.com/PythonMuse/ai-ledger/tree/main/articles/30-ai-routines-for-accountants).

It gives your team a ready-to-use folder structure for turning external regulatory or policy guidance into a structured, version-controlled, AI-assisted monitoring workflow.

---

## How to Use This Template

1. Copy this entire folder into your project.
2. Rename it to match your topic (e.g., `sales-tax-nexus/`, `lease-accounting-policy/`).
3. Fill in each file using the instructions inside it.
4. Commit the folder to your version control system.
5. Update `routines/monitor-guidance.yaml` with your source URL and review schedule.
6. Share the `README.md` with your team so everyone knows how the folder works.

---

## Folder Structure

```
tax-guidance-template/
├── sources/
│   └── source-summary.md         ← Official guidance, summarised
├── company-guidance/
│   └── company-application.md    ← Your team's interpretation
├── skills/
│   └── review-skill.md           ← AI skill for this topic
├── routines/
│   └── monitor-guidance.yaml     ← Scheduled monitoring configuration
├── evidence/
│   └── change-review-log.md      ← Audit trail for approved changes
└── README.md                     ← This file
```

---

## Who Reviews What

| File | Who creates it | Who reviews it |
|---|---|---|
| `source-summary.md` | AI (guided by a prompt) | Tax / subject-matter professional |
| `company-application.md` | AI + team input | Tax manager or controller |
| `review-skill.md` | AI + team input | Process owner |
| `monitor-guidance.yaml` | AI + process owner | IT or workflow approver |
| `evidence/` files | AI (proposed only) | Human reviewer before commit |

---

**PythonMuse LLC**
*Practical AI for accounting and finance professionals.*
*github.com/PythonMuse/ai-ledger*
