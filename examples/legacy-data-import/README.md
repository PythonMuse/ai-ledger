# Legacy Data Import

Copies files from legacy folder locations into your `workings/data/raw/` folder for the current period.

Part of the [Workings Layer Method](../../articles/22-workings-layer-method/) — designed to bridge legacy accounting folder structures and the new controlled workings layer, without modifying any source files.

---

## What This Solves

When your accounting data lives in shared drives or legacy folder structures that can't be reorganized, you still need a controlled, repeatable way to bring data into your AI workflow each period.

Manually dragging files is error-prone and not reproducible. This script gives you a documented, auditable import step instead.

---

## What It Does

- Copies a defined list of legacy files into `workings/data/raw/`
- Never modifies, moves, or deletes source files
- Prompts before overwriting if a file already exists in the destination
- Writes a dated run log to the destination folder automatically
- Validates that placeholder paths have been filled in before running

---

## How to Use

**1. Open `copy_legacy_data.py`**

Fill in two sections:

```python
LEGACY_FILES = [
    ("GL export",       r"C:\Finance\Shared\GL\2026\gl_export.xlsx"),
    ("Bank statement",  r"C:\Finance\Shared\Bank\april_bank.csv"),
]

DESTINATION_FOLDER = r"C:\Finance\Budget\2026\workings\data\raw"
```

**2. Run the script**

```bash
python copy_legacy_data.py
```

**3. Review the log**

A log file is written to `workings/data/raw/` automatically:

```
2026-04-26_import_log.txt
```

---

## Where This Fits

```
Budget/
├── 2026/
│   ├── CLAUDE.md                    <- AI scope definition
│   ├── [legacy files stay here]
│   └── workings/
│       ├── .git/                    <- version control lives here only
│       ├── .gitignore               <- excludes data/raw/ from git
│       ├── copy_legacy_data.py      <- this script (or link to it)
│       ├── data/
│       │   ├── raw/                 <- files land here (not committed)
│       │   └── processed/
│       ├── scripts/
│       └── outputs/
```

---

## .gitignore Recommendation

Version control tracks your *process*, not your raw data files. Add this to your `workings/.gitignore`:

```
# Raw source data -- never commit
data/raw/

# Outputs (optional -- commit if you want a record of results)
# data/processed/

# Python
__pycache__/
*.pyc
*.pyo
.env
```

---

## Sending Outputs Back to Legacy Locations

If your team still expects outputs in the original folder structure, that is fine and intentional. The workings layer tracks the process. You save the final output back to wherever the team expects it.

To automate this, add an output copy step to your script:

```python
# After generating output, copy it back to the legacy location
import shutil
from pathlib import Path

OUTPUT_FILE = Path(r"workings\outputs\2026-04-26_bank_rec_v1.xlsx")
LEGACY_OUTPUT_PATH = Path(r"LEGACY_PATH_PLACEHOLDER\bank_rec_april.xlsx")

shutil.copy2(OUTPUT_FILE, LEGACY_OUTPUT_PATH)
print(f"Output saved to legacy location: {LEGACY_OUTPUT_PATH}")
```

Fill in `LEGACY_PATH_PLACEHOLDER` with the actual destination path before running.

---

## Files

| File | Description |
|------|-------------|
| `copy_legacy_data.py` | Main import script with placeholder paths to fill in |

---

*Related: [Workings Layer Method (Article 22)](../../articles/22-workings-layer-method/) | [AI Project Memory Example](../ai-project-memory/)*
