---
name: accounting-number-normalization
description: Convert accounting-formatted values (e.g., ($1,234.56)) into clean numeric values usable for calculations in Python
---

# Approved Use Case

Use Case ID: UC-010

---

# Purpose

This skill converts accounting-formatted numeric values into clean Python floats before any calculation or analysis is performed.

It is designed to:
- strip currency symbols and thousands separators
- convert parenthetical negatives `(123)` to signed negatives `-123`
- handle blank and null values consistently
- preserve the original data layer untouched

This skill is **preprocessing only**.

It does **not** interpret business meaning, validate totals, or replace a reviewer's reconciliation step.

---

# Allowed Inputs

Use only approved source data such as:

- pandas Series or DataFrame columns
- values sourced from Excel exports (CSV or .xlsx)
- values sourced from accounting system reports
- sample or masked data for testing

All transformations should be applied to a **copy** of the source data. The raw layer must never be overwritten.

---

# Prohibited Inputs

Never apply this skill directly to:

- files containing unmasked SSNs, EINs, or bank account numbers
- data outside the approved project directory
- production data without a raw backup confirmed

If a column contains mixed identifiers and amounts, stop and ask for a cleaned source file.

---

# Required Working Method

1. Confirm the source column contains accounting-formatted values (not already numeric).
2. Confirm a raw copy of the data is preserved before transformation.
3. Apply the core cleaning logic in a separate processed layer.
4. Validate output using the checklist below before using in any calculation.
5. Log the transformation step in the project workings file.

---

# Core Logic

```python
def clean_accounting_number(series):
    return (
        series.astype(str)
        .replace(r'[\$,]', '', regex=True)           # Remove currency symbols and commas
        .replace(r'\((.*?)\)', r'-\1', regex=True)   # Convert (123) → -123
        .replace(r'^\s*$', '0', regex=True)          # Handle blank strings
        .astype(float)
    )
```

---

# Optional Enhancement

Handle additional real-world formatting edge cases:

```python
def clean_accounting_number_advanced(series):
    return (
        series.astype(str)
        .str.strip()
        .replace(r'[\$,]', '', regex=True)
        .replace(r'\((.*?)\)', r'-\1', regex=True)
        .replace(r'–', '-', regex=True)              # Special dash characters
        .replace(r'-$', '', regex=True)              # Trailing negatives like 123-
        .replace(r'^\s*$', '0', regex=True)
        .astype(float)
    )
```

---

# Output Format

A clean pandas Series with:

- dtype: `float64`
- all parenthetical values converted to signed negatives
- all currency symbols and commas removed
- blank/null values represented as `0.0` (or `NaN` if preferred — document the choice)

---

# Validation Checklist

Before using cleaned output in any calculation:

- [ ] Sum matches expected totals
- [ ] No unexpected `NaN` values
- [ ] Negative values correctly represented (spot-check 3–5 rows)
- [ ] Data type confirmed numeric (`float64`)
- [ ] Sample rows manually verified against source

---

# Common Failure Modes

| Issue | Cause |
|---|---|
| Values not converting | Hidden characters or non-standard formatting |
| Positives instead of negatives | Parentheses pattern not matched |
| `NaN` values appear | Non-numeric strings present in column |
| Totals off | Partial cleaning or mixed formats in same column |

---

# Style Rules

- Always transform in a **processed** layer — never mutate the raw source
- Log the function name and column name in the workings file
- Document whether blanks are treated as `0` or `NaN` — both are valid, but be explicit

---

# Audit & Governance Notes

- Raw data must be preserved (raw layer)
- Transformation applied in processed layer only
- Transformation logic must be documented for reproducibility
- Treat this as a standard preprocessing control in financial workflows
- Reference: [Workings Layer Method](../../articles/22-workings-layer-method/README.md)

---

# Example Invocation

Use this skill when a column from an Excel export contains accounting-formatted values and calculations are returning unexpected results.

Example prompt:

> "Use the accounting-number-normalization skill on the `Amount` column in the transactions DataFrame. Preserve the raw data and save the cleaned column to the processed layer."

---

# Evidence

Log transformation steps to:

`workings/` or `evidence/run-logs/`

Suggested file naming pattern:

`YYYY-MM-DD_accounting-number-normalization_[source-file].md`

---

# Related Articles

- [AI Didn't Break Your Numbers. Excel Did.](../../articles/24-excel-number-trap/README.md) — origin article for this skill
- [The Workings Layer Method](../../articles/22-workings-layer-method/README.md) — raw vs processed layer discipline
- ["AI Can't Work With Our Excel Files"... or Can It?](../../articles/15-ai-and-excel-files/README.md) — instruction layer for Excel workflows

---

*Also available in the [PythonMuse Workflow Kit](https://github.com/PythonMuse/pythonmuse-workflow-kit)*

*Tag: #Top10Traps #1 | #DataCleaning #AccountingAI #PythonMuse*
