# Deterministic Script Release Checklist

*A companion template for [AI Helped Me Build It. AI Does Not Have to Run It.](../README.md)*

Deterministic does not mean correct. A script can apply the wrong rule perfectly, every month, forever. This checklist is the minimum to complete before a script, query, or Power Query becomes part of a recurring accounting process.

It covers the script itself. For the wider lifecycle (who approves a workflow for production, and how changes are handled afterwards), use the Builder-to-Production companion from Article 40: [Production Readiness](https://github.com/PythonMuse/pythonmuse-builder-to-production/blob/main/PRODUCTION_READINESS.md) and [Change Management](https://github.com/PythonMuse/pythonmuse-builder-to-production/blob/main/CHANGE_MANAGEMENT.md).

---

**Script / workflow:** [name]  **Version / commit:** [ ]  **Prepared by:** [ ]  **Date:** [ ]

## 1. Known-input tests

- [ ] A synthetic test file exists, deliberately seeded with the cases the rule must handle (formatting differences, blanks, boundary dates, near-misses).
- [ ] The expected output was **calculated by hand before** running the script, not copied from the script's first run.
- [ ] The script's output matches the expected output exactly.
- [ ] At least one known gap is documented (a case the approved rule does not catch), so nobody mistakes "consistent" for "complete."

> Example: the duplicate-payment demo in this folder checks its output against [`expected_exceptions.csv`](../data/expected_exceptions.csv) and documents that "ABC Corp" vs. "ABC Corporation" is missed on purpose.

## 2. Input checks (before any calculation runs)

- [ ] **Schema check:** every expected column is present, with the expected name. The run stops if one is missing or renamed.
- [ ] **Type check:** identifiers (invoice numbers, account numbers, vendor IDs) are read as text, so leading zeros survive and numbers don't turn into decimals.
- [ ] **Blank-key check:** rows missing a key field are routed to a person, not silently matched or dropped.
- [ ] **Period check:** the file covers the period it claims to cover.

## 3. Control totals

- [ ] Row count in = rows processed + rows excluded (with reasons).
- [ ] Dollar total in ties to the source system or source report.
- [ ] Output totals tie back to input totals where they should.

## 4. Stable environment

- [ ] Library versions are pinned (for example a `requirements.txt` with exact versions, or a locked environment), so an update can't change behavior silently.
- [ ] The as-of date is a fixed parameter or a labeled input cell, never `TODAY()`, `NOW()`, or the system clock.
- [ ] Thresholds and tolerances (materiality, date windows, amounts) live in one clearly labeled place, with the approval reference beside them.

## 5. Evidence of each run

- [ ] A run log records: run date, who ran it, input file names (and ideally a checksum), version / commit, row counts, and totals.
- [ ] An exception report is produced every run, even when it is empty ("0 exceptions" is evidence; no file is not).
- [ ] Outputs are written to a defined location; inputs are never overwritten.

## 6. Change control

- [ ] The script is under version control.
- [ ] Changes are reviewed by someone other than the author before release (see [Pull Requests Are Internal Controls](../../20e-pull-requests-are-controls/README.md)).
- [ ] Known-input tests are re-run after every change, including library upgrades.

## 7. Sign-off

| Role | Name | Date | Notes |
|---|---|---|---|
| Builder | | | |
| Reviewer (independent of builder) | | | |
| Process owner | | | |

---

*PythonMuse LLC | www.pythonmuse.com. Educational purposes only; not professional advice. Content licensed under CC BY-NC-SA 4.0.*
