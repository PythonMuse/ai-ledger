"""Duplicate-payment test -- companion demo for Article 42,
"AI Helped Me Build It. AI Does Not Have to Run It."

Simplified illustration -- not production-ready code. It leaves out the
schema checks, logging, and run evidence a production script needs (see
templates/deterministic_script_release_checklist.md).

Run from anywhere:
    python duplicate_payment_test.py

Reads data/ap_payments.csv (synthetic), writes
data/duplicate_payment_exceptions.csv, then compares that output with
data/expected_exceptions.csv -- a known-input test with a hand-calculated
expected result.

The sample data is seeded on purpose. One pair ("ABC Corp" vs.
"ABC Corporation") is deliberately MISSED by the approved rule. Do not
"fix" the data to make it disappear: it is the article's lesson that a
script can apply the wrong rule perfectly.
"""

from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data"

# --- core logic (this block is the excerpt shown in the article) ----------
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
# --- end of core logic -----------------------------------------------------


def _fmt_date(series):
    return series.dt.strftime("%Y-%m-%d")


def _fmt_amount(series):
    return series.map(lambda v: f"{v:.2f}")


# Build one exception report a reviewer can work from.
dup_report = pd.DataFrame({
    "exception_type": "possible_duplicate",
    "payment_id": duplicates["payment_id_a"],
    "vendor_name": duplicates["vendor_name_a"],
    "invoice_number": duplicates["invoice_number_a"],
    "amount": _fmt_amount(duplicates["amount_a"]),
    "payment_date": _fmt_date(duplicates["payment_date_a"]),
    "matched_payment_id": duplicates["payment_id_b"],
    "matched_vendor_name": duplicates["vendor_name_b"],
    "matched_invoice_number": duplicates["invoice_number_b"],
    "matched_payment_date": _fmt_date(duplicates["payment_date_b"]),
    "days_apart": duplicates["days_apart"].astype(str),
})
missing_report = pd.DataFrame({
    "exception_type": "missing_key",
    "payment_id": missing_keys["payment_id"],
    "vendor_name": missing_keys["vendor_name"],
    "invoice_number": missing_keys["invoice_number"],
    "amount": _fmt_amount(missing_keys["amount"]),
    "payment_date": _fmt_date(missing_keys["payment_date"]),
})
report = (pd.concat([dup_report, missing_report], ignore_index=True)
          .sort_values(["exception_type", "payment_id"], ascending=[False, True])
          .reset_index(drop=True))
report.to_csv(DATA / "duplicate_payment_exceptions.csv", index=False)

print(f"{len(ap)} payments tested. {len(duplicates)} pair(s) sent for review. "
      f"{len(missing_keys)} payment(s) missing a vendor or invoice number sent for manual review.")

# Known-input test: compare with the hand-calculated expected result.
expected = pd.read_csv(DATA / "expected_exceptions.csv", dtype=str).fillna("")
actual = pd.read_csv(DATA / "duplicate_payment_exceptions.csv", dtype=str).fillna("")
if actual.equals(expected):
    print("Known-input test PASSED: output matches data/expected_exceptions.csv.")
else:
    print("Known-input test FAILED: output does not match data/expected_exceptions.csv.")
    raise SystemExit(1)
