# Workings Template

A starter kit for AI-assisted accounting workflows using the [Workings Layer Method](../../articles/22-workings-layer-method/).

Clone or copy this folder at the start of each period. Fill in the placeholders. Run inside `workings/` so version control and AI scope stay aligned.

---

## What's Included

| File / Folder | Purpose |
|---------------|---------|
| `CLAUDE.md` | AI instructions -- rules, permissions, data masking, tone |
| `.gitignore` | Excludes `data/raw/` and Python artifacts from git |
| `plan.md` | Workflow plan template -- objective, steps, sources, outputs |
| `status_update.md` | Session log -- milestone tracking |
| `data/raw/` | Landing zone for legacy source files (not committed) |
| `data/processed/` | Cleaned and intermediate data |
| `scripts/` | Processing scripts |
| `outputs/` | Generated reports and deliverables |
| `evidence/run-logs/` | Audit trail logs |
| `skills/` | Reusable SKILL.md files |

---

## How to Use Each Year

### 1. Clone or copy

If hosted as a git repo:
```bash
git clone <your-template-repo-url> workings
cd workings
```

If using it as a folder copy, paste it inside your year folder and initialize a new repo:
```bash
cd workings
git init
git add .
git commit -m "Initial setup from workings template"
```

### 2. Fill in the placeholders

Open `CLAUDE.md` and update the **Year-Specific Customization** section at the bottom:
- Period (year)
- Preparer name
- Engagement or entity name
- Legacy data paths (read-only source file locations)
- Legacy output paths (where final outputs get saved back to)

Open `plan.md` and fill in:
- Objective
- Source file locations
- Steps for this period
- Output destinations

### 3. Pull in source data

Run `copy_legacy_data.py` (in `scripts/`) to copy files from legacy locations into `data/raw/`. Fill in the legacy paths before running -- they are placeholders by design.

See [examples/legacy-data-import](../legacy-data-import/) for the full script and documentation.

### 4. Start Claude Code from inside `workings/`

```bash
cd workings
claude
```

Launching from inside `workings/` sets the AI operating boundary to this folder. It can read `../` paths to reference legacy files above, but cannot write outside `workings/`.

### 5. Commit changes as you go

Commit after each meaningful step:
```bash
git add .
git commit -m "2026-04-26: Completed GL reconciliation, output in outputs/"
```

---

## Year-Over-Year Audit Trail

Because every year starts from the same template, audit comparison is straightforward.

To compare this year's CLAUDE.md against last year's:
```bash
# From this year's workings folder
git diff ../2025/workings/CLAUDE.md CLAUDE.md
```

Or compare both years back to the template:
```bash
git diff <template-commit-hash> CLAUDE.md
```

This answers *"what changed from last year?"* without manually reviewing two folders.

---

## Folder Structure

```
workings/
├── .git/
├── .gitignore
├── CLAUDE.md
├── plan.md
├── status_update.md
├── scripts/
│   └── copy_legacy_data.py
├── data/
│   ├── raw/              <- not committed
│   └── processed/
├── outputs/
├── evidence/
│   └── run-logs/
└── skills/
    └── [skill folders go here]
```

---

## Cross-Year Analysis

When a workflow needs to look across multiple years, create a separate `workings/` folder at the parent level (e.g., `Budget/workings/`). Give it its own `CLAUDE.md` that explicitly names the year folders it reads from:

```
Budget/
├── workings/             <- cross-year analysis, its own git repo
│   ├── CLAUDE.md         <- names ../2025/ and ../2026/ explicitly
│   ├── scripts/
│   └── outputs/
├── 2025/
│   └── workings/         <- cloned from this template
└── 2026/
    └── workings/         <- cloned from this template
```

Keep the cross-year `workings/` as a separate git repo. It tracks the multi-year analysis independently of the year-level work.

---

*Related: [Workings Layer Method (Article 22)](../../articles/22-workings-layer-method/) | [Legacy Data Import Example](../legacy-data-import/)*
