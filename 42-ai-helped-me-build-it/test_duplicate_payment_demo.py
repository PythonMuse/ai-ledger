"""Tests for the Article 42 duplicate-payment demo.

Run from the article folder:
    python -m pytest test_duplicate_payment_demo.py -q

Every expected figure below was worked out by hand from data/ap_payments.csv
before these assertions were written:

  P001 / P002  Northwind Supply, INV-1043 vs. "inv 1043", $1,250.10,
               Sep 2 -> Sep 12 = 10 days            -> flagged
  P003 / P004  Contoso Freight, 88017, $640.00,
               Sep 3 -> Oct 2 = 29 days             -> flagged
  P005 / P006  Fabrikam Office, F-2207, $315.45,
               Aug 5 -> Sep 5 = 31 days             -> NOT flagged (outside 30)
  P007 / P008  Tailspin Catering, blank invoice     -> missing_key, never paired
  P009 / P010  "ABC Corp" vs. "ABC Corporation"     -> MISSED on purpose
  P011 / P012  Litware, LC-900 vs. LC-901           -> NOT flagged (different invoice)
  P013         Northwind, INV-1044, same amount     -> NOT flagged (different invoice)
  P015         blank vendor                         -> missing_key
"""

import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

HERE = Path(__file__).parent
SCRIPT = HERE / "duplicate_payment_test.py"
OUTPUT = HERE / "data" / "duplicate_payment_exceptions.csv"


@pytest.fixture(scope="module")
def run_result():
    result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True,
                            text=True, cwd=str(HERE.parent))
    report = pd.read_csv(OUTPUT, dtype=str).fillna("")
    return result, report


def _pairs(report):
    dups = report[report["exception_type"] == "possible_duplicate"]
    return {(a, b) for a, b in zip(dups["payment_id"], dups["matched_payment_id"])}


def test_script_runs_and_matches_expected(run_result):
    result, _ = run_result
    assert result.returncode == 0, result.stdout + result.stderr
    assert "15 payments tested. 2 pair(s) sent for review. 3 payment(s)" in result.stdout
    assert "Known-input test PASSED" in result.stdout


def test_formatting_differences_still_match(run_result):
    _, report = run_result
    assert ("P001", "P002") in _pairs(report)


def test_date_tolerance_boundary(run_result):
    _, report = run_result
    pairs = _pairs(report)
    assert ("P003", "P004") in pairs        # 29 days: inside tolerance
    assert ("P005", "P006") not in pairs    # 31 days: outside tolerance


def test_blank_keys_are_never_paired(run_result):
    _, report = run_result
    pairs = _pairs(report)
    assert ("P007", "P008") not in pairs
    missing = set(report.loc[report["exception_type"] == "missing_key", "payment_id"])
    assert missing == {"P007", "P008", "P015"}


def test_abc_corporation_is_deliberately_missed(run_result):
    """The approved rule matches on exact vendor key. "ABCCORP" != "ABCCORPORATION",
    so this likely duplicate is missed -- consistently, every run. That is the
    article's point: deterministic does not mean correct."""
    _, report = run_result
    assert ("P009", "P010") not in _pairs(report)
    assert not set(report["payment_id"]) & {"P009", "P010"}


def test_different_invoices_are_not_flagged(run_result):
    _, report = run_result
    flagged = set(report["payment_id"]) | set(report["matched_payment_id"])
    assert not flagged & {"P011", "P012", "P013", "P014"}


def test_reading_invoice_numbers_as_text_preserves_them(tmp_path):
    """Why the script passes dtype=str: an all-numeric column with one blank
    is read as floats, so 1043 becomes 1043.0 and the punctuation strip turns
    it into "10430" -- and 001043 collapses into the same key."""
    csv = tmp_path / "numeric.csv"
    csv.write_text("invoice_number\n1043\n\n001043\n")
    as_float = pd.read_csv(csv, skip_blank_lines=False)["invoice_number"]
    as_text = pd.read_csv(csv, skip_blank_lines=False, dtype={"invoice_number": str})["invoice_number"]
    assert str(as_float.iloc[0]) == "1043.0"
    assert as_text.iloc[0] == "1043"
    assert as_text.iloc[2] == "001043"
