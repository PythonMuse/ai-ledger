# Logs and Telemetry for an Accounting Workflow: The Technical Appendix

*The technical appendix for _Your AI Workflow Is Running. Who Is Watching It?_: a fictional bank reconciliation that writes an activity log, run metrics, and an OpenTelemetry trace, plus native AI observability, a monitoring control, and five experiments*

---

**PythonMuse LLC**
*Published November 2026*

---

This page is for readers who want to see how a workflow records what it did, try it on a fictional bank reconciliation, or review a monitoring design someone else built. [The article](./README.md) stands on its own; nothing here changes its argument. Think of this as the workpapers behind the memo.

> **Part of a PythonMuse Lab.** [The article](./README.md) is the *Understand* layer. This appendix is *Implement*. There's no separate companion demo for this Lab: the two scripts below are small enough to run straight from here, and every output shown on this page came from actually running them.

**Who this is for:** accountants who build small workflows with an AI co-pilot, reviewers deciding what evidence a workflow should leave behind, and IT partners asked to support one.

**What you need:** Python 3.10 or later, Visual Studio Code (or any terminal), and, for Part 4, Git. We ran everything on Windows 11 in PowerShell with Python 3.14 and the OpenTelemetry Python SDK 1.45.2. The first exercise needs no AI model, no subscription, and no monitoring platform.

**Demo-only versus production:** the scripts show the *mechanics* of logging and telemetry with fictional data on one machine. They are not a production reconciliation, an audit log, or a validated financial reporting control. Part 10 lists what a production version would need, and which parts belong to your organization.

A few terms used throughout:

- **Log:** a record of an event (the run started, an exception was found, the run failed).
- **Metric:** a measurement (transactions processed, exceptions, exception rate). Like a KPI.
- **Trace:** the connected steps of one run, each step being a **span**. Like a transaction walk-through.
- **Telemetry:** the umbrella term for the logs, metrics, and traces a system sends out about how it operates.
- **Run ID:** a unique identifier stamped on every record from one execution, so the records can be tied together. Think of it as the batch number.
- **OpenTelemetry:** an open-source, vendor-neutral standard, maintained under the Cloud Native Computing Foundation, for producing and sending telemetry so that most monitoring tools can read it.

---

## 1. Understand What We Are Recording

Before writing code, think about the records an ordinary accounting system produces. An ERP keeps transaction histories, user activity, posting timestamps, and approval status. Separately, the accounting team keeps reconciliations, exception reports, and review evidence.

We can create similar categories of evidence for an automated workflow:

- An **activity log** records significant events: the run started, an input was loaded, an exception was found, an error occurred, the run completed.
- A **metrics file** summarizes each run: counts, exception rate, duration, status.
- A **trace** connects the operations inside a run, which helps locate where a delay or failure happened.

None of these proves the accounting is right. A system can execute flawlessly while applying the wrong business rule. That's why the example records both execution information and a few accounting validation results, such as a completeness check.

---

## 2. Create the Project in Visual Studio Code

Download the two scripts, [bank_rec.py](./code/bank_rec.py) and [otel_demo.py](./code/otel_demo.py), or copy them from the sections below. The complete set, including a `.gitignore`, is in the [article's GitHub folder](https://github.com/PythonMuse/ai-ledger/tree/main/articles/47-ai-workflow-monitoring/code). Put them in a new folder, for example `pythonmuse-ai-monitoring-lab`:

```text
pythonmuse-ai-monitoring-lab/
├── bank_rec.py
├── otel_demo.py
├── .gitignore
└── logs/          (created by the script on its first run)
```

The `.gitignore` file keeps generated logs, the local Python environment, and anything secret out of Git:

```gitignore
logs/
__pycache__/
.venv/
.env
```

Open the folder in Visual Studio Code, open the integrated terminal, and create a virtual environment (a private copy of Python for this project, so nothing you install affects anything else):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux, activate it with `source .venv/bin/activate` instead. Part 3 needs nothing beyond Python's standard library.

---

## 3. Build a Bank Reconciliation With Activity Logging

Here is `bank_rec.py`. It compares six fictional bank amounts with the general ledger (GL), writes every exception to an activity log, appends one row per run to a metrics file, and records a `workflow_failed` event if anything goes wrong mid-run.

```python
"""A fictional bank reconciliation that leaves evidence behind.

PythonMuse Lab: "Your AI Workflow Is Running. Who Is Watching It?"
(technical appendix, Part 3). Code licensed under MIT; see LICENSE-CODE.

What it does:
  - compares six fictional bank amounts with the general ledger (GL),
  - writes a JSON Lines activity log   -> logs/activity.jsonl
  - appends one row per run            -> logs/run_metrics.csv
  - records a workflow_failed event if something goes wrong mid-run.

Demo only. It is not a production reconciliation, an audit log, or a
validated financial reporting control. All data is fictional.

Optional environment variables:
  GIT_COMMIT        a version identifier to stamp on the run (not verified)
  SIMULATE_FAILURE  set to "1" to raise an error before the run completes
"""

import csv
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

# ---------------------------------------------------------------------------
# The approved matching rule
# ---------------------------------------------------------------------------
# Amounts that differ by no more than this are treated as matched.
# Experiment 2 changes it to Decimal("0.00") (exact match only) and compares
# the runs. Changing this line is a change to an accounting rule: commit it,
# and get it approved, like any other.
MATCH_TOLERANCE = Decimal("1.00")

# Currency note: amounts are Decimal, built from strings, not floats.
# Floats store most cents approximately (0.1 + 0.2 != 0.3 in Python), which
# makes exact comparisons and tolerances unreliable. Decimal("170.00") is
# exactly 170.00. If you must use floats, round both sides to 2 places before
# comparing.

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

run_id = uuid4().hex          # one identifier shared by every record of this run
start_time = time.perf_counter()


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


logger = logging.getLogger("bank_reconciliation")
logger.setLevel(logging.INFO)
logger.propagate = False
handler = logging.FileHandler(LOG_DIR / "activity.jsonl", encoding="utf-8")
handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(handler)


def record_event(event_name, level="info", **details):
    """Write one structured event (one JSON object per line)."""
    event = {"timestamp": utc_now(), "run_id": run_id, "event": event_name,
             **details}
    getattr(logger, level)(json.dumps(event))


def append_metrics(processed, matched, exceptions, status):
    """Append one row per run to the metrics file (a KPI dataset).

    For a run that failed part-way, pass None for the counts: they are left
    blank rather than written as zeros, because zero would be a false number.
    """
    if processed:
        exception_rate = round(exceptions / processed, 4)
    else:
        exception_rate = None
    metrics = {
        "timestamp": utc_now(),
        "run_id": run_id,
        "match_tolerance": str(MATCH_TOLERANCE),
        "processed": processed,
        "matched": matched,
        "exceptions": exceptions,
        "exception_rate": exception_rate,
        "duration_seconds": round(time.perf_counter() - start_time, 4),
        "status": status,
    }
    metrics_file = LOG_DIR / "run_metrics.csv"
    with metrics_file.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=metrics.keys())
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow(metrics)


# ---------------------------------------------------------------------------
# Fictional bank and GL data: (transaction ID, bank amount, GL amount)
# ---------------------------------------------------------------------------
# TX003 differs by 5.00: an exception under any sensible tolerance.
# TX006 differs by 0.75: matched at a 1.00 tolerance, an exception at 0.00.
# Both differences are deliberate. Please don't "fix" them.
TRANSACTIONS = [
    ("TX001", Decimal("100.00"), Decimal("100.00")),
    ("TX002", Decimal("250.00"), Decimal("250.00")),
    ("TX003", Decimal("175.00"), Decimal("170.00")),
    ("TX004", Decimal("400.00"), Decimal("400.00")),
    ("TX005", Decimal("125.00"), Decimal("125.00")),
    ("TX006", Decimal("60.00"), Decimal("60.75")),
]

# A demonstration expectation, not independent evidence. In production this
# would come from the source: the bank statement's item count and totals.
EXPECTED_COUNT = 6


def reconcile(transactions):
    """Compare each pair; log every exception. Returns the counts."""
    processed = matched = exceptions = 0
    for transaction_id, bank_amount, gl_amount in transactions:
        processed += 1
        difference = bank_amount - gl_amount
        if abs(difference) <= MATCH_TOLERANCE:
            matched += 1
        else:
            exceptions += 1
            record_event("matching_exception", level="warning",
                         transaction_id=transaction_id,
                         reason="amount_mismatch",
                         difference=str(difference))
    if os.getenv("SIMULATE_FAILURE") == "1":
        raise RuntimeError("Simulated failure before the run completed")
    return processed, matched, exceptions


# ---------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------
record_event("workflow_started", workflow="bank_reconciliation",
             expected_count=EXPECTED_COUNT,
             match_tolerance=str(MATCH_TOLERANCE),
             version=os.getenv("GIT_COMMIT", "unverified"))

try:
    processed, matched, exceptions = reconcile(TRANSACTIONS)
except Exception as err:  # record the failure, then stop
    record_event("workflow_failed", level="error",
                 error_type=type(err).__name__, error=str(err))
    append_metrics(None, None, None, "failed")
    print("Run ID:", run_id)
    print("Status: failed -", err)
    print("See logs/activity.jsonl for the workflow_failed event.")
    sys.exit(1)

completeness_check = processed == EXPECTED_COUNT
# "incomplete": the run finished but did not process the expected population.
# "failed" is reserved for a run that stopped part-way.
status = ("incomplete" if not completeness_check
          else "review_required" if exceptions > 0
          else "ready_for_review")

record_event("workflow_completed", processed=processed, matched=matched,
             exceptions=exceptions, completeness_check=completeness_check,
             status=status)
append_metrics(processed, matched, exceptions, status)

print("Run ID:", run_id)
print("Match tolerance:", MATCH_TOLERANCE)
print("Transactions processed:", processed)
print("Exceptions:", exceptions)
print("Status:", status)
```

Three design choices are worth pointing out, because each one is an accounting decision dressed up as code:

- **`MATCH_TOLERANCE` is the approved matching rule.** Amounts within 1.00 count as matched. Changing that line changes an accounting rule, so it belongs under change control, and the value is stamped on every run record so a reviewer can see which rule produced which result.
- **Amounts are `Decimal`, not floating-point numbers.** Ordinary Python floats store most cents approximately (`0.1 + 0.2` is `0.30000000000000004`), which makes exact comparisons and tolerances unreliable. `Decimal("170.00")` is exactly 170.00. If a source gives you floats, round both sides to two places before comparing.
- **The two differences in the data are deliberate.** TX003 is off by 5.00 and is an exception under any sensible tolerance. TX006 is off by 0.75: matched at a 1.00 tolerance, an exception at 0.00. That's what makes Experiment 2 work. Please don't "fix" them.

Download or clone the folder, then run from inside it:

```powershell
python bank_rec.py
```

Output (the run ID will differ on your machine):

```text
Run ID: c6a1167ae84647de9d5b92b35b11033c
Match tolerance: 1.00
Transactions processed: 6
Exceptions: 1
Status: review_required
```

By hand: six transactions, five within 1.00, one (TX003) outside it. Exception rate 1 / 6 = 0.1667. Status `review_required`, because a person has to look at TX003 before anyone calls this reconciled.

### Reading the activity log

Open `logs/activity.jsonl`. JSON (JavaScript Object Notation) is a plain-text way of writing a record as labeled fields, such as `"transaction_id": "TX003"`, so that people and programs can both read it. Think of a row in a spreadsheet where every value carries its own column heading. JSONL means JSON Lines: one such record per line, each readable on its own. From that run:

```json
{"timestamp": "2026-11-23T17:40:09+00:00", "run_id": "c6a1167ae84647de9d5b92b35b11033c", "event": "workflow_started", "workflow": "bank_reconciliation", "expected_count": 6, "match_tolerance": "1.00", "version": "unverified"}
{"timestamp": "2026-11-23T17:40:09+00:00", "run_id": "c6a1167ae84647de9d5b92b35b11033c", "event": "matching_exception", "transaction_id": "TX003", "reason": "amount_mismatch", "difference": "5.00"}
{"timestamp": "2026-11-23T17:40:09+00:00", "run_id": "c6a1167ae84647de9d5b92b35b11033c", "event": "workflow_completed", "processed": 6, "matched": 5, "exceptions": 1, "completeness_check": true, "status": "review_required"}
```

The program doesn't just say it finished. It records when it started, under which rule and version, which transaction produced an exception and by how much, and what it concluded. The run ID ties the three lines together.

**Accounting comparison:** this is an activity history, like the one your ERP keeps, except our own workflow writes it.

### Reading the metrics file

Open `logs/run_metrics.csv` (it opens in Excel). Each run appends one row:

```text
timestamp,run_id,match_tolerance,processed,matched,exceptions,exception_rate,duration_seconds,status
2026-11-23T17:40:09+00:00,c6a1167ae84647de9d5b92b35b11033c,1.00,6,5,1,0.1667,0.0028,review_required
```

Run the script a few times and you have a dataset you can chart by date, rule, or status in Excel or Power BI, for example to see whether exceptions rose after a rule change.

**Accounting comparison:** a control monitoring report, or a KPI dataset.

### What this example does not do

The expected count of 6 is typed into the code. That shows how a completeness check works, but it isn't independent evidence about the source population. A production reconciliation would take its expected count and control totals from the source itself (the bank statement), reconcile balances, and have some way to notice a run that never produced a completion record at all. Experiments 3 and 4 make both gaps visible.

---

## 4. Connect the Run to Git

Git records changes to tracked files, so it can tell you which version of the workflow was committed and what changed between versions. The script stamps a version identifier on each run:

```python
os.getenv("GIT_COMMIT", "unverified")
```

This reads a value from an environment variable. It does not check it. For a local test, if your folder is a Git repository with at least one commit, set the variable to the current commit just before running:

```powershell
$env:GIT_COMMIT = git rev-parse HEAD
python bank_rec.py
```

On macOS or Linux: `GIT_COMMIT=$(git rev-parse HEAD) python bank_rec.py`. The `workflow_started` record now carries a real commit identifier instead of `unverified`.

Two cautions. First, in production the environment that runs the workflow should confirm that the deployed code and settings match the approved version; otherwise the identifier in the log may not describe the code that actually ran. Second, a commit is not an approval. [Pull Requests Are Internal Controls](../20e-pull-requests-are-controls/README.md) covers how review and approval attach to a change.

**Accounting comparison:** Git preserves versions of a documented procedure. The execution log records activity under that procedure. Approval records show who authorized a change and when it took effect. Three records, three purposes.

---

## 5. Add OpenTelemetry

OpenTelemetry gives you a standard way to produce traces, metrics, and logs, so that instead of inventing a format for every workflow, you use common instrumentation that most monitoring tools can receive. We'll use it for a trace and two metrics, printing everything to the terminal so nothing leaves your machine.

Install the two core packages into your virtual environment:

```powershell
python -m pip install opentelemetry-api opentelemetry-sdk
```

Here is `otel_demo.py`, the same fictional reconciliation with instrumentation added:

```python
"""The same fictional reconciliation, instrumented with OpenTelemetry.

PythonMuse Lab: "Your AI Workflow Is Running. Who Is Watching It?"
(technical appendix, Part 5). Code licensed under MIT; see LICENSE-CODE.

Prints one trace (four spans) and two counters to the terminal. Nothing is
sent anywhere: the console exporters only print. Demo only; all data is
fictional.

Requires:  python -m pip install opentelemetry-api opentelemetry-sdk
"""

from decimal import Decimal

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

# Same approved rule as bank_rec.py. Amounts are Decimal, not float, so that
# cents compare exactly (see the currency note in bank_rec.py).
MATCH_TOLERANCE = Decimal("1.00")

# Name the workflow, so its telemetry is labeled with something better than
# "unknown_service".
resource = Resource.create({"service.name": "bank-reconciliation-demo"})

# Traces: print each span to the terminal as soon as it ends.
trace_provider = TracerProvider(resource=resource)
trace_provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
tracer = trace_provider.get_tracer("bank_rec_lab")

# Metrics: the reader exports every 60 seconds, and once more at shutdown,
# so this short script prints its metrics when it finishes.
metric_reader = PeriodicExportingMetricReader(
    ConsoleMetricExporter(), export_interval_millis=60000
)
metric_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
meter = metric_provider.get_meter("bank_rec_lab")

processed_counter = meter.create_counter(
    "bankrec.transactions.processed", description="Transactions compared"
)
exception_counter = meter.create_counter(
    "bankrec.exceptions", description="Transactions outside the tolerance"
)

with tracer.start_as_current_span("bank_reconciliation") as main_span:
    main_span.set_attribute("accounting.match_tolerance", str(MATCH_TOLERANCE))

    with tracer.start_as_current_span("load_transactions"):
        transactions = [
            (Decimal("100.00"), Decimal("100.00")),
            (Decimal("250.00"), Decimal("250.00")),
            (Decimal("175.00"), Decimal("170.00")),
            (Decimal("400.00"), Decimal("400.00")),
            (Decimal("125.00"), Decimal("125.00")),
            (Decimal("60.00"), Decimal("60.75")),
        ]

    with tracer.start_as_current_span("compare_transactions"):
        exceptions = sum(
            abs(bank - ledger) > MATCH_TOLERANCE for bank, ledger in transactions
        )
        processed_counter.add(len(transactions))
        exception_counter.add(exceptions)
        main_span.set_attribute("accounting.exception_count", exceptions)

    with tracer.start_as_current_span("prepare_review"):
        review_status = "review_required" if exceptions else "ready_for_review"
        main_span.set_attribute("accounting.review_status", review_status)

trace_provider.shutdown()
metric_provider.shutdown()
```

Run it:

```powershell
python otel_demo.py
```

The script prints four spans and then the metrics. The exact layout depends on your OpenTelemetry version. Here is the top-level span from our run, exactly as printed:

```json
{
    "name": "bank_reconciliation",
    "context": {
        "trace_id": "0x7f92699d52b4faadb728668305e0ff5d",
        "span_id": "0xb27429e11ebde53e",
        "trace_state": "[]"
    },
    "kind": "SpanKind.INTERNAL",
    "parent_id": null,
    "start_time": "2026-11-23T17:36:10.901700Z",
    "end_time": "2026-11-23T17:36:10.902400Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {
        "accounting.match_tolerance": "1.00",
        "accounting.exception_count": 1,
        "accounting.review_status": "review_required"
    },
    "events": [],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.45.2",
            "service.instance.id": "802260a0-2948-4242-89d6-237e3f4a0da4",
            "service.name": "bank-reconciliation-demo"
        },
        "schema_url": ""
    }
}
```

and the heart of the metrics output, also trimmed:

```json
{
    "name": "bankrec.transactions.processed",
    "description": "Transactions compared",
    "data": { "data_points": [ { "value": 6 } ], "is_monotonic": true }
},
{
    "name": "bankrec.exceptions",
    "description": "Transactions outside the tolerance",
    "data": { "data_points": [ { "value": 1 } ], "is_monotonic": true }
}
```

### What is a span?

A span is one operation inside a run, with a name, a start and end time, and its relationship to other spans. Our script creates a parent span, `bank_reconciliation`, with three children: `load_transactions`, `compare_transactions`, and `prepare_review`. Each child carries the parent's `span_id` as its `parent_id`, and all four share one `trace_id`. That shared ID is what turns four separate records into one trace. (The parent prints last because it finishes last.)

For an accountant, it's the walk-through: not just "the process ended," but which steps happened, in what order, and how long each took. A trace only covers what someone chose to instrument, though. If a required accounting step has no span, the trace is silent about it.

### What is a counter?

The script also creates two metrics, `bankrec.transactions.processed` and `bankrec.exceptions`. Counters only go up, and a monitoring system collects them across many runs, which is where they become useful: rising exception rates, unusual volumes, or a workflow that keeps failing. Other instruments, such as histograms, record distributions, for example of processing times.

In real use, OpenTelemetry would *export* this to a monitoring system instead of printing it. For learning how instrumentation works, the terminal is enough, and it has the considerable advantage of sending your data nowhere.

---

## 6. What Happens When an AI Agent Is Involved

Both examples so far use deterministic Python logic: the same input and rules produce the same output every time, and no AI model is needed to *run* them. That's deliberate. It lets you see the monitoring mechanics without model calls in the way. (An AI co-pilot can still help you build, test, and maintain the scripts, which is the theme of [AI Helped Me Build It. AI Does Not Have to Run It.](../42-ai-helped-me-build-it/README.md))

Now imagine an AI agent coordinating the reconciliation. It retrieves the bank activity, runs the Python matching script, inspects the unmatched items, drafts explanations, and prepares an exception report. Some steps are the agent's; others are the script's. That creates two monitoring needs:

1. **What did the agent do?** Which model was called, which tools were used, did a tool fail, was anything retried, how long did it take?
2. **Did the accounting process meet its requirements?** Were the right transactions included, did the matching agree, were exceptions resolved, did someone approve the result?

Native agent observability helps with the first. Accounting-specific instrumentation, like the logging in `bank_rec.py`, and control records answer the second.

### Native tracing on the Claude Platform

On October 14, 2026, Anthropic announced OpenTelemetry trace export for the Claude Platform, in **public beta**. It covers Claude Managed Agents (Anthropic's hosted service for running agents), the Messages API (the interface software uses to call Claude models), and the Anthropic SDKs (the code libraries developers use to call that API). According to the announcement and the documentation:

- Every agent turn, model call, and tool use arrives in your observability tool as a standard OpenTelemetry trace, with latency, token counts, and identifiers.
- Managed Agents and Messages API tracing is configured as a destination in the Claude Console, which needs an admin; the SDKs export traces from your own code.
- Spans follow the OpenTelemetry generative AI semantic conventions (shared naming rules for AI telemetry), so tools that support those conventions recognize them without extra setup. Anthropic lists partner platforms including Datadog, Grafana Cloud, Honeycomb, New Relic, Splunk, and others.
- **Content mode** defaults to metadata only: identifiers, timing, status, and token counts, but not prompts or responses. Full content is an opt-in setting per destination or SDK client.
- Exported spans are delivered on a best-effort basis and aren't guaranteed to be a complete record of API usage. For counting usage, Anthropic points to its separate usage and cost reporting.

The announcement included FloQast, an accounting workflow automation company, describing how it sees each model call in the same trace as the reconciliation or journal-entry workflow it ran inside, with prompt version, tool calls, latency, and token spend together.

This means developers may not need to write custom instrumentation for every model interaction on supported products. It doesn't mean every operation is covered. Claude Platform tracing, Claude Code monitoring, and the Agent SDK's observability are related but separate capabilities, each documented separately, and turning on one doesn't capture what happens in the others.

### Trying Claude Code telemetry locally

If you use Claude Code from the Visual Studio Code integrated terminal, you can watch its own telemetry with console output only, so nothing is sent to a monitoring service. In PowerShell:

```powershell
$env:CLAUDE_CODE_ENABLE_TELEMETRY = "1"
$env:OTEL_METRICS_EXPORTER = "console"
$env:OTEL_LOGS_EXPORTER = "console"
$env:OTEL_METRIC_EXPORT_INTERVAL = "10000"   # 10 seconds; the default is 60
claude
```

According to Claude Code's monitoring documentation, `console` is a valid exporter for both metrics and logs, and logging of your prompt text (`OTEL_LOG_USER_PROMPTS`) and of tool details (`OTEL_LOG_TOOL_DETAILS`) is off unless you enable it. Tracing is a separate beta that needs its own settings. Leave those content settings off, use fictional data, and expect the console output to be noisy: it's meant for debugging, not reading over coffee. We verified these settings against the documentation; your installed version may differ, so check the current page before you rely on it.

Two details matter for control design:

- **Administrators can set telemetry for everyone** through Claude Code's managed settings file, and a repository's own `.claude/settings.json` can't turn telemetry on, choose where it goes, or switch on content capture. That's a useful property: the people being monitored can't quietly redirect the monitoring.
- **Claude Code's telemetry won't include the accounting results of a Python script it launches.** To capture those, the script must write its own records, as `bank_rec.py` does. A real monitoring design usually combines native agent telemetry, the workflow's own instrumentation, and independent review evidence.

### Equivalents in other ecosystems

The same idea exists across the major providers. Each was checked against its own documentation in November 2026:

- **OpenAI:** the Agents SDK traces model generations, tool calls, handoffs, and guardrails by default, viewable in OpenAI's Traces dashboard. By default it includes inputs and outputs (`trace_include_sensitive_data` is `True`), and tracing is unavailable for organizations under OpenAI's Zero Data Retention policy.
- **Microsoft:** Microsoft Foundry tracing uses OpenTelemetry conventions and stores traces in Azure Monitor Application Insights. It's generally available for prompt, hosted, and external agents (workflow agents are in preview), and it can capture inputs, outputs, and tool arguments, so Microsoft advises redacting sensitive content. Copilot Studio agents can also send telemetry to Application Insights; logging of conversation details is an optional setting.
- **Google:** in Gemini Enterprise Agent Platform (Google's successor to Vertex AI), agents deployed to its Agent Runtime can export OpenTelemetry traces to Cloud Trace. Capturing prompts and responses is a separate setting that you turn on explicitly.

Whichever tool records the run, the accounting questions stay the same.

---

## 7. Design an Accounting Monitoring Control

Now apply accounting judgment to the information. Suppose the bank reconciliation runs each business day. We want to establish that the expected run happened, the input population was complete, the matching rule was applied, and unresolved exceptions were investigated. A basic control design:

| Part of the control | What it looks like for a daily bank reconciliation |
|---|---|
| Control objective | Reconciliation processing is complete, and every exception is reviewed |
| Control owner | Accounting manager |
| Frequency | Daily, after the run |
| Expectation | One run per business day; processed count equals the bank statement's item count |
| Threshold for investigation | Missing run, `failed` or `incomplete` status, exception rate above the level the owner set from operating history, or a change in match tolerance |
| Required evidence | Run record (run ID, version, tolerance, counts, status), source population check, exception report, reviewer sign-off |
| Required action | Investigate and document the resolution before approval; escalate a missing or failed run the same day |
| Evidence retention | An approved location with access and retention controls |

Set thresholds from the process's risk and operating history, not because a number was easy to program. That's the difference between collecting a metric and designing a control: the metric says 15 transactions are unmatched; the control decides whether that needs investigating, who does it, and what evidence is needed before the reconciliation is approved.

### Monitoring the monitoring

Then ask whether the logs and metrics themselves can be relied on:

- What happens if the workflow crashes before writing its final record? (Experiment 4.)
- Can someone delete or edit the logs?
- Could logging be disabled, or a threshold raised, without anyone noticing?
- Are all expected runs represented in the monitoring report?
- Who can read the collected information, and how long is it kept?

A local CSV or JSONL file is fine for learning, but it's editable and proves little about its own integrity. A production setup may need central storage, restricted access, protected retention, alerts on configuration changes, and a way to spot missing or altered records. How much of that you need depends on the risk and importance of the workflow.

---

## 8. Be Careful What You Capture

Observability tools can record prompts, model responses, tool arguments, and other execution details, and in an accounting workflow those may contain confidential financial information. It's entirely possible to lock down access to the accounting documents and then publish their contents to everyone who can open the monitoring dashboard.

The defaults differ by tool, so read them:

| Tool | Does it capture prompts and responses by default? |
|---|---|
| Claude Platform OpenTelemetry export | No. Metadata only unless you choose Full content. |
| Claude Code monitoring | No. Prompt text and tool details are logged only if you enable them. |
| OpenAI Agents SDK tracing | Yes. Inputs and outputs are included unless you turn off `trace_include_sensitive_data`. |
| Microsoft Foundry agent tracing | It can capture inputs, outputs, and tool arguments; Microsoft recommends redacting sensitive content before it reaches telemetry. |
| Google agent tracing to Cloud Trace | No. Prompt and response capture is a separate setting you turn on. |

Before enabling detailed content logging, decide:

1. Which fields are actually needed for investigation and audit evidence?
2. Where will the telemetry be sent, and is that service approved for this data?
3. Who can access it?
4. How long is it kept, and who can delete it?

Operational identifiers, counts, status, and references to approved documents are often enough, without copying the source documents into the log. Logging something doesn't make it safe to keep forever. Put the monitoring environment through the same data classification, access control, and vendor review as the workflow itself; [How to Use AI in Accounting Without Sending the Wrong Data](../06-safe-ai-data-workflows/README.md) is the starting point.

---

## 9. Suggested Experiments

Once both scripts run, try changing the fictional workflow. Each experiment takes a few minutes, and each one teaches a control lesson.

**Experiment 1: Increase the exceptions.** Change another GL amount in `TRANSACTIONS`, say TX004 to `Decimal("390.00")`, and run again. Compare the new rows in `activity.jsonl` and `run_metrics.csv`. How would a monitoring report flag a rising exception rate, and who would look at it?

**Experiment 2: Change the matching rule, and the version.** This is the article's Git example in miniature. If the folder isn't a Git repository yet, make it one and commit the original script (`git init`, `git add .`, `git commit -m "Bank rec v1"`). Then change `MATCH_TOLERANCE` to `Decimal("0.00")` (exact match only), commit that change, and run with the new version identifier:

```powershell
git commit -am "Exact match only"
$env:GIT_COMMIT = git rev-parse HEAD
python bank_rec.py
```

Our result:

```text
Run ID: a13ac4e493a548e7a33a6c7cec9ff2b7
Match tolerance: 0.00
Transactions processed: 6
Exceptions: 2
Status: review_required
```

By hand: TX006's 0.75 difference is now outside the tolerance, so exceptions rise from 1 to 2 and the exception rate from 0.1667 to 0.3333. The metrics file shows the jump; the run record carries the tolerance and the commit identifier that explain it; Git shows exactly what changed. What it doesn't show is who approved the change. The script records an identifier; it doesn't establish approval or verify what was deployed. Change the tolerance back to `Decimal("1.00")` when you're done.

**Experiment 3: Simulate incomplete processing.** Delete the TX005 line from `TRANSACTIONS`, leave `EXPECTED_COUNT` at 6, and run. The completeness check fails and the status is `incomplete`: five processed against six expected. Then ask the real question: where would an independent expected count come from in production? (The bank statement, not the script.) Restore the line afterwards.

**Experiment 4: Introduce a processing failure.** Set the switch that makes the script raise an error before it finishes:

```powershell
$env:SIMULATE_FAILURE = "1"
python bank_rec.py
Remove-Item Env:SIMULATE_FAILURE
```

Our result:

```text
Run ID: 5005c89f523d4408acda8a1046b2a7ec
Status: failed - Simulated failure before the run completed
See logs/activity.jsonl for the workflow_failed event.
```

The activity log gets a `workflow_failed` record with the error, the metrics file gets a row with status `failed` and blank counts (blank, not zero, because zero would be a false number), and the script exits with an error code a scheduler can see:

```json
{"timestamp": "2026-11-23T17:40:10+00:00", "run_id": "5005c89f523d4408acda8a1046b2a7ec", "event": "workflow_failed", "error_type": "RuntimeError", "error": "Simulated failure before the run completed"}
```

That's the good case: the failure was caught and recorded. Now consider what this can't catch. If the machine loses power, the process is killed, or the scheduled job never starts, nothing is written at all. No `workflow_failed`, no row, no complaint. The only evidence is an absence, and you'll see it only if something independent compares the runs that happened against the runs that should have happened. That's why monitoring has to check for missing runs, not just read the records of successful ones.

**Experiment 5: Compare logging with tracing.** Run both scripts and put their outputs side by side. The activity log records selected events and accounting exceptions. The OpenTelemetry output records instrumented operations, timings, and measurements. Which would a controller want to review each morning? Which would a developer want when diagnosing a slow or failing run? (Usually: the controller wants the first, the developer the second, and the auditor wants to know the two agree.)

---

## 10. What a Production Implementation Would Require

This Lab shows the foundation, not a production control environment. Before relying on a similar workflow, an organization would need, at a minimum:

- **Input integrity:** an identified source population, with completeness evidenced against the source (item counts and control totals from the bank statement), not a number typed into the script.
- **Calculation integrity:** validated matching logic and calculations, tested against independently calculated expected results.
- **Change control:** changes to code, rules, and instructions approved before they take effect, and evidence that the deployed version is the approved one.
- **Access:** permissions that match responsibilities, for the workflow and for its logs.
- **Operations:** detection of failed, missing, and unexpected runs; defined owners, review frequency, escalation, and evidence retention for the monitoring itself.
- **AI-specific items, if a model takes part:** model and instruction versions, tool permissions, data handling, evaluation results, and changes that could alter previously approved behavior. [Model Selection Is an Accounting Control](../36-model-selection-is-a-control/README.md) covers the model side.

For financial reporting workflows, align all of this with your organization's internal control and audit requirements. None of it is satisfied merely by installing OpenTelemetry or saving a log file.

The developer can configure the logs, metrics, and traces, and an AI platform can generate observability data on its own. Someone who understands the accounting still has to decide which activities matter, what counts as an exception, and whether the evidence is sufficient. **A workflow that produces an answer is useful. A workflow that produces an answer together with reliable evidence of how it operated is much easier to govern, investigate, and trust.**

*Disclaimer: this exercise uses fictional data and simplified logic for educational purposes. It is not a production-ready bank reconciliation, an audit logging system, or a validated financial reporting control.*

---

## Sources

Every link below was checked in November 2026. Product features and release stages change quickly, so re-check them before you rely on any of them.

- Anthropic: [Trace agents with OpenTelemetry on the Claude Platform](https://claude.com/resources/articles/agent-observability-on-the-claude-platform), October 14, 2026: public beta; Managed Agents, the Messages API, and Anthropic SDKs; agent turns, model calls, and tool uses with latency, tokens, and IDs; the FloQast example
- Anthropic: [OpenTelemetry tracing for the Claude API](https://platform.claude.com/docs/en/manage-claude/opentelemetry): beta status; SDK versus API tracing; content modes (metadata only by default); best-effort delivery
- Anthropic: [Claude Code monitoring](https://code.claude.com/docs/en/monitoring-usage): `CLAUDE_CODE_ENABLE_TELEMETRY`; `console` exporters for metrics and logs; default export intervals; `OTEL_LOG_USER_PROMPTS` and `OTEL_LOG_TOOL_DETAILS` off by default; traces in beta; managed settings; repository settings can't enable telemetry
- OpenTelemetry: [Python documentation](https://opentelemetry.io/docs/languages/python/) and [Python instrumentation](https://opentelemetry.io/docs/languages/python/instrumentation/): the `opentelemetry-api` and `opentelemetry-sdk` packages, tracer and meter providers, console exporters
- OpenTelemetry: [GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai): the shared naming rules for AI telemetry used by the Claude Platform and Microsoft Foundry
- OpenAI: [Tracing in the Agents SDK](https://openai.github.io/openai-agents-python/tracing/): on by default; generations, tool calls, handoffs, guardrails; `trace_include_sensitive_data` defaults to `True`; unavailable under Zero Data Retention
- Microsoft: [Agent tracing overview, Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/observability/concepts/trace-agent-concept): OpenTelemetry conventions; traces stored in Application Insights; GA for prompt, hosted, and external agents, workflow agents in preview; security and privacy guidance
- Microsoft: [Agent-level telemetry with Application Insights, Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-bot-framework-composer-capture-telemetry): connecting an agent to Application Insights; optional conversation-detail logging
- Google Cloud: [Set up tracing, Gemini Enterprise Agent Platform](https://docs.cloud.google.com/agent-builder/agent-engine/manage/tracing): OpenTelemetry traces to Cloud Trace; prompt and response capture as a separate setting
- Google Cloud: [Introducing Gemini Enterprise Agent Platform](https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-agent-platform), April 22, 2026: "the evolution of Vertex AI"
- Anthropic: [Use Claude Code in VS Code](https://code.claude.com/docs/en/vs-code): the Claude extension for Visual Studio Code
- Python Software Foundation: [logging](https://docs.python.org/3/library/logging.html) and [decimal](https://docs.python.org/3/library/decimal.html)
- Git: [Documentation](https://git-scm.com/doc)

---

*Back to the article: [Your AI Workflow Is Running. Who Is Watching It?](./README.md)*

*Related: [From AI Answers to Audit Trails](../32-from-ai-answers-to-audit-trails/README.md) | [Pull Requests Are Internal Controls](../20e-pull-requests-are-controls/README.md) | [You Built an AI Workflow. What Happens If You Win the Lottery?](../40-builder-to-production/README.md) | [AI Helped Me Build It. AI Does Not Have to Run It.](../42-ai-helped-me-build-it/README.md)*

*© 2026 PythonMuse LLC. Content licensed under [CC BY-NC-SA 4.0](../../LICENSE); code licensed under [MIT](../../LICENSE-CODE).*
