"""Run both AI-generated scripts on the article's synthetic data and compare
what each one did with every seeded edge case against the hand-checked answer.

Run from anywhere:
    python compare.py

Each script runs in its own temporary folder on a copy of ../../data/ap_payments.csv,
exactly as written by its session (see prompt.md). Nothing here edits them.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
DATA = HERE.parent.parent / "data"
SESSIONS = {"Session A": HERE / "session_a.py", "Session B": HERE / "session_b.py"}

# Each seeded edge case, and what the approved answer (data/expected_exceptions.csv) says.
CASES = [
    ("'INV-1043' vs. 'inv 1043', 10 days apart", ("P001", "P002"), "pair", "Flagged"),
    ("Same invoice, 29 days apart", ("P003", "P004"), "pair", "Flagged"),
    ("Same invoice, 31 days apart", ("P005", "P006"), "pair", "Not flagged"),
    ("Blank invoice number (two payments)", ("P007", "P008"), "missing", "Sent to a person"),
    ("Blank vendor name", ("P015",), "missing", "Sent to a person"),
    ("'ABC Corp' vs. 'ABC Corporation'", ("P009", "P010"), "pair", "Not flagged (missed by design)"),
]


def run(script):
    """Run one script on a fresh copy of the data; return the IDs it paired."""
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(DATA / "ap_payments.csv", tmp)
        shutil.copy(script, tmp)
        subprocess.run([sys.executable, script.name], cwd=tmp, check=True,
                       capture_output=True, text=True)
        out = pd.read_csv(Path(tmp) / "duplicate_payment_exceptions.csv", dtype=str)
    id_cols = [c for c in out.columns if c.startswith("payment_id")]
    pairs = {frozenset(row) for row in out[id_cols].itertuples(index=False)}
    mentioned = {pid for pair in pairs for pid in pair}
    return pairs, mentioned


def describe(case, pairs, mentioned):
    _, ids, kind, _ = case
    if kind == "pair":
        return "Flagged" if frozenset(ids) in pairs else "Not flagged"
    if frozenset(ids) in pairs:
        return "Flagged as a duplicate of each other"
    if set(ids) & mentioned:
        return "Mentioned"
    return "Not in the output (never reported)"


def main():
    results = {name: run(path) for name, path in SESSIONS.items()}
    rows = []
    for case in CASES:
        row = {"Edge case": case[0], "Approved answer": case[3]}
        for name, (pairs, mentioned) in results.items():
            row[name] = describe(case, pairs, mentioned)
        rows.append(row)
    table = pd.DataFrame(rows)
    with pd.option_context("display.max_colwidth", None, "display.width", 200):
        print(table.to_string(index=False))
    for name, (pairs, _) in results.items():
        print(f"{name}: {len(pairs)} pair(s) flagged.")


if __name__ == "__main__":
    main()
