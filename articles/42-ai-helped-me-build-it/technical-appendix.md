# AI Helped Me Build It: The Technical Appendix

*Under the hood of Article 42: the demo script line by line, the fine print on "deterministic," and how to turn a polite request into a control*

---

**PythonMuse LLC**
*Published October 2026*

---

This page is for readers who want to run the demo, read the code, or wire up the controls. [The article](./README.md) stands on its own; nothing here changes its argument. Think of this as the workpapers behind the memo.

---

## 1. The Duplicate-Payment Script, Line by Line

The article describes a Python script that follows criteria the accounting team approved. Here is its core.

> **Simplified illustration, not production-ready code.** It leaves out the schema checks, logging, and run evidence a production script needs. This is the core of [`duplicate_payment_test.py`](./duplicate_payment_test.py), which you can run yourself.

```python
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data"

# Read IDs as text, so 1043 never becomes "1043.0" and 001043 keeps its zeros
ap = pd.read_csv(DATA / "ap_payments.csv", parse_dates=["payment_date"],
                 dtype={"payment_id": str, "vendor_name": str, "invoice_number": str})

# Standardize so "INV-1043" and "inv 1043" are treated as the same invoice
def match_key(column):
    return column.fillna("").str.upper().str.replace(r"[^A-Z0-9]", "", regex=True)

ap["vendor_key"] = match_key(ap["vendor_name"])
ap["invoice_key"] = match_key(ap["invoice_number"])

# A blank key can't be tested, and pandas would pair blanks with each other.
# Send those rows to a person instead of guessing.
blank = (ap["vendor_key"] == "") | (ap["invoice_key"] == "") | ap["amount"].isna()
missing_keys = ap[blank]
testable = ap[~blank].copy()
testable["amount_cents"] = (testable["amount"] * 100).round().astype(int)  # compare pennies

# Pair payments with the same vendor, invoice, and exact amount
pairs = testable.merge(testable, on=["vendor_key", "invoice_key", "amount_cents"],
                       suffixes=("_a", "_b"))
pairs = pairs[pairs["payment_id_a"] < pairs["payment_id_b"]]

# Apply the date tolerance the accounting team approved
DATE_TOLERANCE_DAYS = 30
pairs["days_apart"] = (pairs["payment_date_b"] - pairs["payment_date_a"]).dt.days.abs()
duplicates = pairs[pairs["days_apart"] <= DATE_TOLERANCE_DAYS]
```

**Translation:**

1. Read invoice numbers as text, so 1043 stays 1043 instead of quietly becoming a decimal.
2. Make vendor names and invoice numbers comparable: uppercase, no punctuation, no spaces.
3. Set aside any payment with a blank vendor or invoice number for a person to review. They can't be tested automatically, and left in, pandas would happily pair every blank with every other blank.
4. Convert amounts to whole cents, so tiny floating-point leftovers from exports or calculations can't make equal amounts look different. (Yes, that is a real problem: in most programming languages, 0.1 + 0.2 does not exactly equal 0.3. Numbers are rarely as clean as they look; see [AI Didn't Break Your Numbers. Excel Did.](../24-excel-number-trap/README.md))
5. Find payments that share a vendor, an invoice number, and an amount.
6. Keep only pairs paid within 30 days of each other.
7. The full script then writes everything to one exception report and counts what was tested.

### The bug we caught

A confession, because it proves the point: the first draft of this snippet, written with AI help, had exactly the kind of bug that disclaimer warns about. If the invoice column held only numbers plus one blank, 1043 became "1043.0", the punctuation strip turned it into "10430", and the two blank-invoice payments were reported as a duplicate of each other. We caught it the boring way: by running the code against seeded test data with a known answer. Which is rather the point of the whole article.

### Run it yourself

The article folder includes the full [`duplicate_payment_test.py`](./duplicate_payment_test.py), a synthetic [`ap_payments.csv`](./data/ap_payments.csv), and a hand-calculated [`expected_exceptions.csv`](./data/expected_exceptions.csv). The sample data is seeded on purpose: "INV-1043" vs. "inv 1043", a blank invoice number, payments 29 days apart (flagged) and 31 days apart (not flagged), and one pair the script deliberately misses ("ABC Corp" vs. "ABC Corporation," the subject of the article's "Deterministic Does Not Mean Correct" section).

Run `python duplicate_payment_test.py` and it checks its own output against the expected answer. The [test file](./test_duplicate_payment_demo.py) pins down every deliberate edge case, including the one the script misses, so nobody "fixes" the lesson out of the sample data.

If you are new to scripts altogether, [What the Heck Is a Script?](../25-what-the-heck-is-a-script/README.md) is the gentle on-ramp.

---

## 2. Why "Same Rules" Isn't Quite Enough

The article's definition is **same inputs + same rules (in the same environment) = same outputs.** Three bits of fine print.

### The environment is part of the input

That small "in the same environment" matters. A script running on a different version of a library is, quietly, a slightly different script. [Python Libraries for Accountants](../28-python-libraries-for-accountants/README.md) explains why each project should have its own environment with the same library versions every time it runs.

### Excel's volatile functions (and a SQL cousin)

`TODAY()`, `NOW()`, and `RAND()` are the exceptions to Excel's determinism. They recalculate on their own. If your aging schedule uses `TODAY()`, it will give you a different answer tomorrow. Very on brand for Excel. The fix is boring and effective: put the as-of date in a cell, label it, and point every formula at that cell.

Databases have a cousin of this problem: a SQL query without `ORDER BY` doesn't promise to return rows in the same order twice.

### Temperature zero does not make an LLM deterministic

And before anyone asks: yes, there is a "temperature" setting, and no, turning it to zero does not make the problem go away. Even at the most conservative settings, providers don't guarantee identical output. Anthropic's API documentation says so in as many words, and OpenAI describes its own reproducibility controls as best effort. (Both are linked in the Sources below.)

---

## 3. Turning a Polite Request into a Control

The article's point: *"Do not touch the payroll folder"* in an agent file is an instruction the model is asked to follow. A hard boundary is enforced by the harness itself: tool allowlists, permission settings, folder access, sandboxing. Here is what that looks like in practice.

### Claude Code

Some fields in an agent file *are* enforced. In Claude Code, a subagent's `tools:` line is an allowlist: the subagent simply doesn't get tools that aren't on it. The sentences are not.

Turning "please don't touch payroll" into a control is a few lines in the project's `.claude/settings.json`:

```json
{
  "permissions": {
    "deny": [
      "Read(./payroll/**)",
      "Edit(./payroll/**)"
    ]
  }
}
```

Deny rules are checked before allow rules, and an allow rule can't carve an exception out of one. One honest caveat, straight from Anthropic's own documentation: these rules govern Claude's file tools and the shell commands Claude Code recognizes, not a Python script that opens the file on its own. For enforcement at the operating-system level, Claude Code has a sandbox. Controls have a scope. Know it.

### Other harnesses, same idea

> **A note on tools:** I build in Claude Code inside Visual Studio Code, because that is what our environment uses. Other harnesses have the same idea under different names. In **OpenAI Codex**, the `sandbox_mode` setting (`read-only`, `workspace-write`, or `danger-full-access`) is enforced by the operating system, and `approval_policy` decides when Codex must stop and ask. In **GitHub Copilot's agent mode in VS Code**, you choose which tools the agent can use from the tools picker, and tool calls and terminal commands wait for your approval unless you have auto-approved them (agent sandboxing there is still in preview). If your organization has no harness at all, the Excel version of this lesson is folder permissions and workbook protection rather than a "please don't edit" note on the tab: the control lives in the system, not in the instructions.

Settings like these change often, so check your provider's current documentation before you rely on one. To inventory your own boundaries, use the ["Control or Polite Request?" Boundary Audit](./templates/boundary_audit.md).

---

## 4. The Toolkit

Everything below lives in the article's folder. All of it uses synthetic data, and all of it is meant to be copied and adapted:

- **[Process Step Classification Worksheet](./templates/process_step_classification_worksheet.xlsx)** ([CSV](./templates/process_step_classification_worksheet.csv)): map each step's input, output, rule, failure mode, reviewer, evidence, and classification.
- **[Step Decision Tree card](./templates/step_decision_tree_card.md):** the six questions on one page, for the desk.
- **[Build-Time vs. Run-Time AI Record](./templates/build_time_vs_run_time_record.md):** for one workflow, what AI did while you built it, what data it saw, whether it has a run-time role, and who approved that choice.
- **[Deterministic Script Release Checklist](./templates/deterministic_script_release_checklist.md):** known-input tests, control totals, schema checks, pinned versions, a fixed as-of date, run logs, and sign-off before a script goes live.
- **["Control or Polite Request?" Boundary Audit](./templates/boundary_audit.md):** list every boundary in your skill and agent files and mark which ones the harness actually enforces.
- **[Duplicate-payment demo](./duplicate_payment_test.py):** the script above, its [synthetic data](./data/ap_payments.csv), the [expected result](./data/expected_exceptions.csv), and a [test file](./test_duplicate_payment_demo.py) that pins down every deliberate edge case, including the one it misses.

---

## Sources

Every provider-specific statement in Article 42 and this appendix was checked against the provider's own documentation in October 2026:

- Anthropic: [Messages API reference](https://platform.claude.com/docs/en/api/messages) (temperature: "even with `temperature` of `0.0`, the results will not be fully deterministic")
- OpenAI: [Advanced usage: reproducible outputs](https://developers.openai.com/api/docs/guides/advanced-usage) (determinism is not guaranteed)
- Anthropic: [Claude Code permissions](https://code.claude.com/docs/en/permissions) (deny rules, their scope, and the sandbox) and [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) (the `tools` allowlist)
- OpenAI: [Codex agent approvals and security](https://learn.chatgpt.com/codex/agent-approvals-security) (sandbox modes and approval policies)
- Microsoft: [VS Code agent approvals and permissions](https://code.visualstudio.com/docs/agents/run/approvals) and [VS Code agent tools](https://code.visualstudio.com/docs/copilot/agents/agent-tools)
- Microsoft: [Get started with Copilot in Excel](https://support.microsoft.com/en-us/copilot-excel) and [Clean up your data with Copilot in Excel](https://support.microsoft.com/en-us/excel/copilot/clean-up-your-data-with-copilot-in-excel)
- Microsoft: [Excel recalculation and volatile functions](https://learn.microsoft.com/en-us/office/client-developer/excel/excel-recalculation) and [ORDER BY clause (Transact-SQL)](https://learn.microsoft.com/en-us/sql/t-sql/queries/select-order-by-clause-transact-sql)
- pandas: [`DataFrame.merge`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html) ("If both key columns contain rows where the key is a null value, those rows will be matched against each other.")

Harness settings and product features change quickly. Re-check them before you rely on one.

---

*Back to the article: [AI Helped Me Build It. AI Does Not Have to Run It.](./README.md)*

*Related: [Python Libraries for Accountants](../28-python-libraries-for-accountants/README.md) | [Metadata Is the Label Maker Your AI Workflow Needs](../31-metadata-is-the-label-maker/README.md) | [When the Invoice Starts Giving Orders](../37-when-the-invoice-gives-orders/README.md)*

*© 2026 PythonMuse LLC. Content licensed under [CC BY-NC-SA 4.0](../../LICENSE); code licensed under [MIT](../../LICENSE-CODE).*
