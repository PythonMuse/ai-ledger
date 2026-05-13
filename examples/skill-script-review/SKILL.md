---
name: script-review
description: Review a Python script written for an accounting workflow and translate its logic into plain English for audit documentation and sign-off
---

# Approved Use Case

Use Case ID: UC-005

---

# Purpose

This skill helps accounting and finance professionals review Python scripts that have been written to automate accounting tasks.

It is designed to:
- read a Python script and translate each step into plain accounting language
- identify what inputs the script requires and what outputs it produces
- flag any logic that needs human review or judgment before the script is run
- produce a plain-English summary suitable for audit documentation or internal sign-off
- confirm the script does not access prohibited data or perform actions outside its scope

This skill is **explanatory and assistive only**.

It does **not** approve the script for production use, authorize any posting action, or certify the script is free of errors.

---

# Allowed Inputs

- Python scripts (.py files) written for accounting workflows
- Scripts located in the approved project directory (e.g., `/src/` or `/scripts/`)
- Sample or masked data files referenced by the script

---

# Prohibited Inputs

Never review or document scripts that:

- access production databases without explicit authorization
- handle unmasked PII, SSNs, or bank account numbers
- send data to external systems or APIs not approved by IT governance
- include hardcoded credentials, tokens, or passwords

If prohibited content is detected, stop and ask for a sanitized version.

---

# Required Working Method

1. Confirm the script is from an approved project directory.
2. Read the script from top to bottom.
3. For each function or logical block, produce a plain-English description using this pattern:
   - **What it does** (one sentence)
   - **What it needs** (inputs)
   - **What it produces** (outputs or side effects)
4. Identify any steps that apply accounting judgment (rounding, classification, threshold logic) and flag them for human review.
5. Identify any external files, databases, or APIs the script touches.
6. Produce the output in the format below.
7. Do not run the script.

---

# Output Format

## Script Review Summary

**Script:** `filename.py`
**Reviewed by:** AI (script-review skill, UC-005)
**Requires human sign-off:** Yes

---

## What This Script Does

One paragraph, plain English. What problem does the script solve? What accounting process does it automate?

---

## Step-by-Step Logic

| Step | Function / Block | Plain-English Description |
|------|-----------------|--------------------------|
| 1 | `function_name()` | What it does in one sentence |
| 2 | `next_function()` | What it does in one sentence |

---

## Inputs Required

| Input | Type | Description |
|-------|------|-------------|
| File or variable name | CSV / DataFrame / etc. | What it represents |

---

## Outputs Produced

| Output | Type | Description |
|--------|------|-------------|
| File or return value | CSV / DataFrame / etc. | What it contains |

---

## Steps Requiring Human Review

List any logic that applies accounting judgment and needs a human to confirm it is correct before the script runs in production:

- [ ] Item 1 — describe the judgment call
- [ ] Item 2 — describe the judgment call

---

## External Dependencies

List any files, databases, APIs, or environment variables the script accesses outside its own logic.

---

## Reviewer Checklist

- [ ] Logic matches the intended accounting workflow
- [ ] Input files are from approved sources
- [ ] Output format is suitable for the downstream process
- [ ] All judgment calls in the review list have been confirmed
- [ ] No prohibited data is accessed
- [ ] Reviewer has signed off before script is run in production

---

# Style Rules

- Write in plain English — no Python syntax in the summary
- Use accounting vocabulary (reconciliation, variance, matching, posting, etc.)
- Flag uncertainty clearly: if the script logic is ambiguous, say so
- Keep the summary concise enough to attach to a workpaper

---

# Example Invocation

Use this skill when a team member has used AI to write a script and needs to understand and sign off on it before running it.

Example prompt:

"Use the script-review skill on the file `/src/reconcile_bank.py` and produce a plain-English summary I can attach to my workpaper."

---

# Evidence

Save the review output to:

`evidence/run-logs/`

Suggested file naming pattern:

`YYYY-MM-DD_UC-005_script-review_filename.md`

---

# Human Review

Required reviewer:
- Controller
- Accounting Manager
- Senior Accountant (if delegated)

The review output documents what the script does. It does not authorize the script to run. Human sign-off is required before any script is used on production data or as part of an audit-ready workflow.
