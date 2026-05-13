# Examples

Practical finance workflow examples — scripts, notebooks, and sample data that solve real accounting problems.

---

## What Goes Here

Each example lives in its own folder with everything needed to run it:

```
examples/
└── bank-reconciliation/
    ├── README.md            ← what this example does
    ├── data/                ← sample data files
    └── reconcile.py         ← the script or notebook
```

## Available Examples

| Example | Description |
|---------|-------------|
| [ai-project-memory](ai-project-memory/) | Starter template for AI-assisted projects with external memory files (plan.md, status_update.md, CLAUDE.md) |
| [trust-but-verify-checklist](trust-but-verify-checklist/) | Six-section audit-friendly checklist for controlling AI workflows in accounting -- from data masking through documentation |
| [skill-bank-reconciliation](skill-bank-reconciliation/) | Reusable SKILL.md for bank reconciliation -- matching bank to GL, classifying exceptions, audit-ready output |
| [skill-margin-analysis](skill-margin-analysis/) | Reusable SKILL.md for margin analysis -- gross margin by segment, period comparison, concentration risk |
| [skill-excel-interpretation](skill-excel-interpretation/) | Reusable SKILL.md for interpreting complex multi-tab Excel workbooks -- tab roles, column maps, analysis rules |
| [skill-script-review](skill-script-review/) | Reusable SKILL.md for reviewing Python scripts in plain English -- translate logic for audit documentation and sign-off |
| [legacy-data-import](legacy-data-import/) | Script to copy files from legacy folder structures into workings/data/raw/ -- placeholder paths, run log, never modifies source files |
| [workings-template](workings-template/) | Full starter kit for a version-controlled workings folder -- CLAUDE.md, .gitignore, plan.md, status log, copy script, and folder structure. Clone each year. |

---

## Example Ideas

These are examples we'd like to build. Contributions welcome.

- **Bank reconciliation** — match bank transactions to GL entries
- **AR aging analysis** — aging buckets, overdue trends, customer risk
- **Financial dashboard** — KPI reporting with Python (Streamlit or matplotlib)
- **Expense classification** — categorize transactions using AI
- **Audit trail documentation** — generate audit-ready output from scripts

---

Want to contribute an example? See [CONTRIBUTING.md](../CONTRIBUTING.md) for how to get started.
