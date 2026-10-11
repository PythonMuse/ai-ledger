# AI Helped Me Build It. AI Does Not Have to Run It.

*What one year of daily AI use taught me about deterministic automation, and where AI belongs in accounting*

---

**PythonMuse LLC**
*Published October 2026*

![Build time vs. run time: AI helps design and test the workflow, then the approved script runs every month without it](./visuals/42_hero.png)

---

## One Year, Every Day

It has been almost exactly one year since I made it my mission to use artificial intelligence (AI) in my work every day.

Not occasionally, and not only when an email needed polishing or a blank page needed staring down.

I wanted to know what AI in accounting looks like after the novelty wears off and the work still has to be accurate, repeatable, explainable, and ready for review.

So I tested tools, built workflows, led study groups, had countless conversations with accounting and finance professionals, gave presentations, and published more than 40 articles.

And every time something appeared to work, I tried to ask the second-level question:

> **What is the system actually doing, and would I trust it to do this again next month?**

One misconception followed me the entire year.

For many accountants, "using AI" still means uploading a spreadsheet into a chat window and asking the model to analyze it.

That is understandable. A chat window is the most visible and accessible place to begin, and it can be useful for exploration. But recurring accounting work has to meet a different standard. Many professionals still work this way today, despite real concerns about data privacy, data leakage, hallucinations, and the need to re-check everything the model says.

Uploading a file and asking questions is where experimentation begins.

It should not be where accounting's use of AI ends.

The choice is not "hand the work to a chatbot" or "keep doing everything by hand." There is a middle ground: use AI to help understand, document, and automate a process, and let defined rules do the recurring work.

That middle ground has a name. I didn't know it when I started.

**Deterministic.**

I arrived at the idea through practice before I learned the word. Once I learned it, a year of lessons clicked into place. I didn't want AI to analyze the same accounting data from scratch every month.

I wanted AI to help me build the process that does the analysis.

---

## The False Choice

Accountants keep getting offered two options:

1. Upload financial data to an AI model and accept the privacy and reliability concerns.
2. Or avoid AI and miss the efficiency.

Deterministic automation is option three.

AI can help an accountant translate an existing procedure into an Excel formula, a Power Query transformation, a Structured Query Language (SQL) query, or a Python script. It can explain unfamiliar code, suggest validation tests, spot edge cases, troubleshoot errors, and draft documentation.

Once the automation is tested and approved, the recurring process runs on defined logic.

**AI helped build it. AI does not have to run it.**

![Asking the chatbot every month vs. building it once](./visuals/42_chatbot_vs_build.png)

| Asking the chatbot every month | Building it once |
|---|---|
| Production data goes to the model every run | The model sees mock data during development |
| The approach may shift from run to run | The same rules run every time |
| You re-validate the model's math monthly | You test the logic before release, then control inputs, changes, and ongoing performance |
| "Why did it flag that?" | Read the rule |
| Evidence = a chat transcript | Evidence = run log, exception report, version history |

This matters in accounting because our work runs on consistent calculations, complete populations, defined source files, reviewable exceptions, change approval, and proof that a process ran as intended. We also handle payroll, customer information, bank activity, and acquisition data. None of it belongs in an unapproved chat window simply because that happens to be the most convenient place to work.

If a script can perform an exact calculation reliably, asking a generative model to recreate it every month adds variability without adding value.

The real payoff is not better technology. It is better use of an accountant's time: exceptions, explanations, and decisions, instead of checking, again, whether the system added the same columns correctly.

---

## Think of It Like Excel

Imagine telling Excel:

*"Go format this data the way I need it. I'll be at lunch."*

For years, that was a fantasy.

Now, with Copilot in Excel, you sort of can. Describe what you want in plain English, and it can help clean up the data, highlight, sort, and filter it, and add formula columns for you.

That is useful.

But next month you ask again. And Copilot works it out again. And you check it again.

Excel has quietly offered the other option for years: Power Query. You record the cleanup steps once (they show up, in order, as Applied Steps). Next month you drop in the new file and click Refresh. Same steps. Same order. Same result. Nobody re-interprets anything.

| Ask Copilot every month | Build it once in Power Query |
|---|---|
| Describe the cleanup each time | Record the steps once |
| AI works out the approach each run | The recorded steps replay |
| You re-check the output monthly | Test the recorded steps, then monitor source changes and outputs |
| Great for one-off requests | Built for recurring work |

That is the whole idea of this article, in a tool you already own.

AI can help build the query, formula, or script. Once tested and approved, the recorded logic performs the recurring work.

---

## What "Deterministic" Means in Plain English

"Deterministic" sounds more technical than it is. Accountants have used deterministic processes for decades.

**Same inputs + same rules (in the same environment) = same outputs.** That's it.

An aging calculation is deterministic. A SUM formula is deterministic. A rule that sends every transaction over $25,000 for extra approval is deterministic.

The system does not wake up on Tuesday and decide that $24,750 feels suspicious.

That small "in the same environment" matters. A script running on a different version of a library is, quietly, a slightly different script. [Python Libraries for Accountants](../28-python-libraries-for-accountants/README.md) explains why each project should have its own environment with the same library versions every time it runs.

> **Excel footnote:** `TODAY()`, `NOW()`, and `RAND()` are the exceptions. They recalculate on their own. If your aging schedule uses `TODAY()`, it will give you a different answer tomorrow. Very on brand for Excel. The fix is boring and effective: put the as-of date in a cell, label it, and point every formula at that cell. (Databases have a cousin of this problem: a SQL query without `ORDER BY` doesn't promise to return rows in the same order twice.)

A large language model (LLM) works differently. It generates a response based on probabilities. Give it substantially the same instructions and data twice, and the wording, reasoning, classification, or conclusion may change.

And before anyone asks: yes, there is a "temperature" setting, and no, turning it to zero does not make the problem go away. Even at the most conservative settings, providers don't guarantee identical output. Anthropic's API documentation says so in as many words, and OpenAI describes its own reproducibility controls as best effort.

That flexibility is why LLMs are good at interpreting language and messy requests.

It is also why their output needs validation.

Neither approach is universally better. They are built for different kinds of work.

So the question is not:

*"Can we use AI for this process?"*

The better question is: **what kind of work happens inside each step of this process?**

---

## AI Can Build the Workflow Without Living Inside It

Take duplicate-payment testing.

**Option one:** upload the accounts payable (AP) data to a large language model every month and ask, "Which of these look like duplicates?"

The model might find useful items. It might also read the request differently next month, skip a relevant record, or confidently flag two payments that merely look alike.

**Option two:** ask AI to help build a Python script that follows criteria the accounting team approved.

> **Simplified illustration, not production-ready code.** It leaves out the schema checks, logging, and run evidence a production script needs. This is the core of [`duplicate_payment_test.py`](./duplicate_payment_test.py), which you can run yourself (more on that below).

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

A confession, because it proves the point: the first draft of this snippet, written with AI help, had exactly the kind of bug that disclaimer warns about. If the invoice column held only numbers plus one blank, 1043 became "1043.0", the punctuation strip turned it into "10430", and the two blank-invoice payments were reported as a duplicate of each other. We caught it the boring way: by running the code against seeded test data with a known answer. Which is rather the point of this whole article.

Notice what the script does not do.

It does not decide that anything is a duplicate. It consistently finds transactions that meet the approved criteria and hands them to an accountant.

During development, AI might write that code, explain each line, generate mock data, suggest test cases, and draft the documentation. When the test runs next month, production data does not need to go anywhere near the model.

Then the model goes home.

The script keeps working.

This is the difference between **build-time AI** and **run-time AI**. At build time, AI assists the person designing the workflow. At run time, the approved process does the work. AI can still have a run-time role, but that should be a design decision, not a default.

> **Run it yourself:** The article folder includes the full [`duplicate_payment_test.py`](./duplicate_payment_test.py), a synthetic [`ap_payments.csv`](./data/ap_payments.csv), and a hand-calculated [`expected_exceptions.csv`](./data/expected_exceptions.csv). The sample data is seeded on purpose: "INV-1043" vs. "inv 1043", a blank invoice number, payments 29 days apart (flagged) and 31 days apart (not flagged), and one pair the script deliberately misses. Run `python duplicate_payment_test.py` and it checks its own output against the expected answer. We will come back to the one it misses.

If you are new to scripts altogether, [What the Heck Is a Script?](../25-what-the-heck-is-a-script/README.md) is the gentle on-ramp, and [From One-Time Analysis to Repeatable Workflows](../11-one-time-to-repeatable-workflows/README.md) walks through turning a one-off analysis into something you can run again.

---

## Don't Classify the Whole Process at Once

Technology decisions get confusing when we label an entire process an "AI use case."

A bank reconciliation, a variance analysis, or a journal-entry process is rarely one kind of work. It might contain a calculation, a matching exercise, a pattern search, some language interpretation, an investigation, and an approval.

Those pieces should not automatically use the same technology.

Break the process into steps. Then classify the work inside each step. Four categories are a good start: **rules, patterns, language, and judgment.**

![Four kinds of work: rules, patterns, language, and judgment, with example tools for each](./visuals/42_four_kinds_of_work.png)

### Rules

*Can we state exactly how the result should be calculated or classified?*

Known rules are strong candidates for deterministic automation: aging buckets, allocation percentages, account-number cleanup, approved matching criteria, variance math, approval thresholds, missing-field checks.

Excel, Power Query, SQL, robotic process automation, and Python can all do this. AI can help build it. The automation follows the rules.

A cousin of this idea runs through [Don't Trust the Model to Find What You Already Know Is There](../23-schema-driven-sanitization/README.md): when you already know the structure of your data, a boring deterministic script is the right primary control, not a model's best guess.

### Patterns

*Do we have historical examples that contain a relationship we can't easily write down as rules?*

That may be a machine-learning opportunity. An organization might use past payment history to estimate which receivables are likely to go delinquent. The model learns statistical relationships from prior examples instead of following an accountant-written rule like "flag every balance over 60 days."

One clarification, because it trips people up. Once a predictive model is trained, fixed, and run under the same conditions, it will generally produce the same score for the same input. The difference is where the logic came from: a person wrote the rule, or the data taught it.

> **A note on terms:** Technically, a large language model is also a machine-learning model. In this article, "machine learning" means predictive models trained on your own historical data.

Machine learning deserves its own article. For now: a pattern learned from data is not the same as a rule written by a person.

### Language

*Does the work require interpreting or producing unstructured language?*

This is where an LLM earns its keep: summarizing contract provisions, organizing explanations from department leaders, extracting details from narrative documents, drafting preliminary variance commentary.

The flexibility is the feature. It is also the reason for validation. If the output touches financial reporting, compliance, a customer commitment, or another material decision, supporting evidence and human review matter even more. [From AI Answers to Audit Trails](../32-from-ai-answers-to-audit-trails/README.md) covers what that validation looks like in practice.

### Judgment

*Does the step require professional accountability, authorization, or a facts-and-circumstances conclusion?*

That stays with a qualified person.

AI may gather information, apply approved rules, prepare an exception list, or draft a recommendation. It should not quietly inherit approval authority because it helped automate the steps leading up to the decision.

---

## A Decision Tree for Each Step

Ask these questions of **each step**, not once for the whole process.

First: is the step still necessary? Automation does not cure a process that exists only because "we've always done it this way."

Automating a process nobody understands is just an efficient way to produce confusion on schedule.

![A decision tree for each process step: four questions to choose an approach, then two control questions for every option](./visuals/42_decision_tree.png)

**Choose the starting approach:**

1. **Is the step necessary and understood?** No → simplify, document, or redesign first.
2. **Can we write the rule, and should the same input always give the same result?** Yes → start with deterministic automation.
3. **Does it require interpreting language or context?** Yes → consider an LLM, subject to data restrictions, validation, and review.
4. **Do reliable historical examples hold a pattern we can't write as rules?** Yes → consider machine learning. No → keep it human-led or redesign.

**Then apply two control questions to every option**, whether you chose deterministic automation, an LLM, machine learning, or a human-led process:

5. **Does the step involve judgment, approval, restricted data, or contractual limitations?** Yes → a qualified person stays responsible, whatever technology prepared the work.
6. **What evidence will show that it worked as intended?** Define validation, logging, exception handling, and sign-off before you build.

> **Framework reminder:** None of this depends on a particular tool. The same six questions work whether the deterministic part ends up as an Excel formula, a Power Query, a SQL view, or a Python script, and whether the co-pilot helping you build it is Claude Code, OpenAI Codex, GitHub Copilot, or Copilot in Excel. The tool changes; the classification does not. This series teaches the framework, not the vendor.

There is a printable one-page version of this tree in the templates folder: [Step Decision Tree card](./templates/step_decision_tree_card.md).

---

## What This Looks Like in a Real Workflow

Take year-over-year variance analysis. It's tempting to call the whole thing an AI use case. Break it down and a better design appears.

| Process step | Nature of the work | Likely approach |
|---|---|---|
| Confirm expected files and fields are present | Known rules | Deterministic automation |
| Validate reporting periods and control totals | Known rules | Deterministic automation |
| Calculate dollar and percentage changes | Known calculations | Deterministic automation |
| Apply materiality thresholds | Approved policy rules | Deterministic automation |
| Retrieve supporting transaction detail | Defined retrieval | Query, script, or approved tool |
| Draft preliminary commentary | Language and context | LLM, if permitted |
| Determine the actual business explanation | Evidence and judgment | Accountant |
| Approve the final analysis | Accountability | Human reviewer |

![Variance analysis as three lanes: the script calculates, an LLM drafts questions if permitted, and the accountant explains and approves](./visuals/42_variance_swimlane.png)

The deterministic part reads current- and prior-year files, validates the structure, calculates variances, applies thresholds, ranks exceptions, and produces a review-ready report. An LLM might help organize supporting information or draft questions for the account owner.

But the model should not invent the reason travel expense went up 27 percent.

**Python calculates the 27 percent. AI suggests questions. The accountant finds, supports, and owns the explanation.**

Bank reconciliation works the same way. A script standardizes dates and amounts, applies approved matching rules, keeps source-row references, and separates matched items from exceptions. The accountant investigates what's left and approves the rec.

Recurring journal entries too. A script reads approved allocation drivers, calculates the entry, confirms debits equal credits, compares the result to an expected range, and prepares the upload file. The system prepares the entry. It does not approve or post it just because the math worked.

The process is neither "AI-driven" nor "deterministic."

It is a controlled workflow containing different kinds of work.

---

## Scripts, Skills, and Agents Play Different Roles

As more accountants start working in AI harness environments (tools like Claude Code, in the terminal or inside Visual Studio Code, OpenAI Codex, or GitHub Copilot's agent mode, where AI works with your files, tools, and saved instructions), another distinction matters. Scripts, skills, and agent files are related. They are not interchangeable.

A **script** encodes defined logic: exactly how to clean a field, calculate a variance, test a threshold, or build an exception report. Designed well and run under the same conditions, it applies the same rules every time.

A **skill** gives AI reusable instructions for a type of work. A variance-analysis skill might tell the model which files to expect, which approved script to run, how to organize commentary, which validations are required, and when to stop for human review. A skill makes the model more consistent. It does not make a probabilistic model deterministic.

An **agent file** defines a broader role and its boundaries: which tools it may use, where outputs go, what is prohibited, which decisions need a human. An agent can coordinate a workflow and call approved deterministic tools without doing every calculation itself. [The Power of Skills and Agents](../17-skills-and-agents-for-accountants/README.md) introduces both.

### Control, or polite request?

Here's the part people miss.

*"It says right there in the agent file: do not touch the payroll folder."*

That sentence is an instruction. The model is asked to follow it. A hard boundary is enforced by the harness itself: tool allowlists, permission settings, folder access, sandboxing.

Some fields in an agent file *are* enforced. In Claude Code, a subagent's `tools:` line is an allowlist: the subagent simply doesn't get tools that aren't on it. The sentences are not. Know which of your boundaries are controls and which are polite requests.

![Control or polite request? A sentence in an agent file asks; a harness permission enforces](./visuals/42_control_or_request.png)

In Claude Code, turning "please don't touch payroll" into a control is a few lines in the project's `.claude/settings.json`:

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

> **A note on tools:** I build in Claude Code inside Visual Studio Code, because that is what our environment uses. Other harnesses have the same idea under different names. In **OpenAI Codex**, the `sandbox_mode` setting (`read-only`, `workspace-write`, or `danger-full-access`) is enforced by the operating system, and `approval_policy` decides when Codex must stop and ask. In **GitHub Copilot's agent mode in VS Code**, you choose which tools the agent can use from the tools picker, and tool calls and terminal commands wait for your approval unless you have auto-approved them (agent sandboxing there is still in preview). If your organization has no harness at all, the Excel version of this lesson is folder permissions and workbook protection rather than a "please don't edit" note on the tab: the control lives in the system, not in the instructions. Settings like these change often, so check your provider's current documentation before you rely on one.

| Accounting world | Harness world |
|---|---|
| Calculation template | Script |
| Desk procedure / standard operating procedure (SOP) | Skill |
| Role description + delegation of authority | Agent file |
| System access rights | Harness permissions |
| Reviewer sign-off | Still you |

A simple division of labor:

- **The script** applies the rule.
- **The skill** explains the approved procedure.
- **The agent** coordinates the permitted steps and tools.
- **The accountant** handles judgment, validation, and approval.

This layered design usually beats asking a model to do the whole process in one prompt. If the idea of a boundary that only *asks* makes you uneasy, it should: [When the Invoice Starts Giving Orders](../37-when-the-invoice-gives-orders/README.md) shows what happens when the text a model reads starts issuing its own instructions, and [Metadata Is the Label Maker Your AI Workflow Needs](../31-metadata-is-the-label-maker/README.md) shows scripts and hooks doing the enforcing.

<!-- TODO: Add a link to the MCP article here once it is published (planned as Article 41 in the approved plan; check the final number before linking). MCP servers are where "approved tools an agent can call" becomes concrete. -->

---

## Deterministic Does Not Mean Correct

Deterministic automation has real control advantages. The logic can be inspected. Known inputs can be tested against expected results. Changes can be version-controlled and approved. Input and output locations can be restricted. Run logs show which files were processed and what came out. Exceptions and review evidence can be kept.

Deterministic does not mean correct.

**A script can apply the wrong rule perfectly. Every month. Forever.**

Remember the pair the demo deliberately misses? "ABC Corp" and "ABC Corporation," same invoice number, same $2,100.00, paid a week apart. A person would spot it in a second. The script compares exact vendor keys, "ABCCORP" is not "ABCCORPORATION," and so it misses the pair. Consistently. Every run. The test file even checks that it keeps missing it, so nobody "fixes" the lesson out of the sample data.

The rule isn't broken. It is exactly what was approved. The rule is just incomplete, and the consistency of the script makes that incompleteness invisible until someone tests for it. (A vendor master ID instead of a vendor name would close this particular gap. Finding gaps like this is what testing with deliberately awkward data is for.)

A script can also consistently process an incomplete file, exclude a valid transaction, misread a date, or use last year's threshold. It can change behavior without anyone touching the code: a library update, a new column in the bank export, a vendor renaming a field.

Consistency makes the process testable. It does not make testing optional.

That is why organization, boundaries, and validation stay central:

- **Organization:** know what the process is supposed to do.
- **Boundaries:** limit the data, tools, outputs, and actions the workflow can touch.
- **Validation:** check results against known examples, control totals, expected ranges, and documented exceptions.

Treat changes to the logic with the same seriousness as changes to an important spreadsheet or a financial system configuration. Because that is what they are. [Pull Requests Are Internal Controls](../20e-pull-requests-are-controls/README.md) shows what that review looks like for code, and [You Built an AI Workflow. What Happens If You Win the Lottery?](../40-builder-to-production/README.md) covers what happens once a workflow becomes something the business depends on. And if "a library update" made you think "or a model update," [Model Selection Is an Accounting Control](../36-model-selection-is-a-control/README.md) is the same lesson for the LLM steps.

---

## The Rule of Thumb

- **If the rule is known,** encode the rule.
- **If language must be interpreted,** consider an LLM, and validate it.
- **If historical examples hold a pattern you can't write down,** machine learning may fit.
- **If the decision needs professional accountability,** keep a person responsible.

---

## Try This Week

Pick one recurring process, but not the hardest one in the department. Month-end close does not need to be your first science project.

Pick something narrow, repetitive, and familiar: a variance calculation, a recurring data transformation, a duplicate-payment test, a missing-field check, a reconciliation prep step.

1. Write down each step in order.
2. For each step, note the input, expected output, rule, possible failure, reviewer, and evidence kept.
3. Classify it: rule, pattern, language, or judgment.
4. Then ask AI to help you *examine* the process, not automate it. Where are the rules clear? Where is undocumented judgment hiding? Where does language matter? What could a script do? Where must a person stay responsible?

You may find that a "manual" process already contains several automatable pieces.

You may also find that your "AI workflow" doesn't need AI in every step.

> **Use the worksheet:** Download the [Process Step Classification Worksheet](./templates/process_step_classification_worksheet.xlsx) (also available as [CSV](./templates/process_step_classification_worksheet.csv)) and use it to map one process step by step. It comes pre-filled with the variance-analysis example above, so you can see a finished row before you write your own. If your process lives in Excel files, [AI Can't Work With Our Excel Files... or Can It?](../15-ai-and-excel-files/README.md) is a useful companion.

---

## Take It With You

Everything below lives in this article's folder. All of it uses synthetic data, and all of it is meant to be copied and adapted:

- **[Process Step Classification Worksheet](./templates/process_step_classification_worksheet.xlsx)** ([CSV](./templates/process_step_classification_worksheet.csv)): map each step's input, output, rule, failure mode, reviewer, evidence, and classification.
- **[Step Decision Tree card](./templates/step_decision_tree_card.md):** the six questions on one page, for the desk.
- **[Build-Time vs. Run-Time AI Record](./templates/build_time_vs_run_time_record.md):** for one workflow, what AI did while you built it, what data it saw, whether it has a run-time role, and who approved that choice.
- **[Deterministic Script Release Checklist](./templates/deterministic_script_release_checklist.md):** known-input tests, control totals, schema checks, pinned versions, a fixed as-of date, run logs, and sign-off before a script goes live.
- **["Control or Polite Request?" Boundary Audit](./templates/boundary_audit.md):** list every boundary in your skill and agent files and mark which ones the harness actually enforces.
- **[Duplicate-payment demo](./duplicate_payment_test.py):** the script from this article, its [synthetic data](./data/ap_payments.csv), the [expected result](./data/expected_exceptions.csv), and a [test file](./test_duplicate_payment_demo.py) that pins down every deliberate edge case, including the one it misses.

---

## The Lesson After One Year

At first I thought AI maturity meant asking better questions.

Then I learned the environment mattered as much as the prompt. Moving into a harness gave me a way to organize files, write reusable instructions, set boundaries, use approved tools, keep documentation, and validate outputs.

About 40 articles later, most of what I've learned still fits in three words: **organization, boundaries, and validation.**

Now I'd add a fourth: **placement.**

Where does AI belong in the process?

Sometimes it helps build the automation. Sometimes it interprets language. Sometimes it coordinates approved tools. Sometimes it prepares information for a decision.

And sometimes it steps out of the production workflow entirely.

AI maturity is not putting AI into more decisions. It is being deliberate about which method belongs in each step.

Once the process is broken into rules, patterns, language, and judgment, the next question is: which decision model belongs in each step? That is a question for a future article in this series.

---

## Sources

Every provider-specific statement in this article was checked against the provider's own documentation in October 2026:

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

**A note on how this article was made.** This article started with me. The year of daily AI use behind it, and the word I learned only after I had been practicing it for months, are mine. This article was written in collaboration with Patrick Toohey. ChatGPT (5.5 Sol) helped us shape our notes into a first structured draft. Claude Sonnet and Claude Opus reviewed that draft and co-built the practice files this article points to. Claude Code (Claude Opus 5.5) then built the final article, the visuals, the templates, the tested duplicate-payment demo, and the site wiring, working from our direction and feedback at each step. That review is where the bug in the original code snippet was found and fixed, and where every Claude Code, Codex, Copilot, and Excel claim was checked against the provider's own documentation. I reviewed every output, pushed back on things I didn't like, and made all final content decisions together with Patrick. That process — bringing your own experience, using AI to build and iterate, and staying in the editorial seat throughout — is exactly what this series is about.

---

*Related: [From One-Time Analysis to Repeatable Workflows](../11-one-time-to-repeatable-workflows/README.md) | [The Power of Skills and Agents](../17-skills-and-agents-for-accountants/README.md) | [Don't Trust the Model to Find What You Already Know Is There](../23-schema-driven-sanitization/README.md) | [What the Heck Is a Script?](../25-what-the-heck-is-a-script/README.md) | [Metadata Is the Label Maker Your AI Workflow Needs](../31-metadata-is-the-label-maker/README.md) | [You Built an AI Workflow. What Happens If You Win the Lottery?](../40-builder-to-production/README.md)*

*© 2026 PythonMuse LLC. Content licensed under [CC BY-NC-SA 4.0](../../LICENSE); code licensed under [MIT](../../LICENSE-CODE).*
