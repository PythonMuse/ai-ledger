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
