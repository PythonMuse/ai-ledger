import pandas as pd

INPUT_FILE = "ap_payments.csv"
OUTPUT_FILE = "duplicate_payment_exceptions.csv"
WINDOW_DAYS = 30

df = pd.read_csv(INPUT_FILE, dtype={"invoice_number": str})
df["payment_date"] = pd.to_datetime(df["payment_date"], errors="coerce")
df["amount"] = pd.to_numeric(df["amount"], errors="coerce").round(2)

# Normalized match keys so trivial formatting differences don't hide duplicates
df["_vendor_key"] = df["vendor_name"].astype(str).str.strip().str.casefold()
df["_invoice_key"] = df["invoice_number"].astype(str).str.strip().str.casefold()

df = df.dropna(subset=["payment_date", "amount"])
df = df.sort_values(["payment_date", "payment_id"]).reset_index(drop=True)
df["_row"] = df.index

keys = ["_vendor_key", "_invoice_key", "amount"]

# Self-join on vendor + invoice + amount to build every candidate pair
pairs = df.merge(df, on=keys, suffixes=("_1", "_2"))

# Keep each pair once (earlier payment first)
pairs = pairs[pairs["_row_1"] < pairs["_row_2"]]

pairs["days_apart"] = (pairs["payment_date_2"] - pairs["payment_date_1"]).dt.days
pairs = pairs[pairs["days_apart"] <= WINDOW_DAYS]

result = pairs.rename(columns={"amount": "amount"})[
    [
        "vendor_name_1",
        "invoice_number_1",
        "amount",
        "payment_id_1",
        "payment_date_1",
        "payment_id_2",
        "payment_date_2",
        "days_apart",
    ]
].rename(
    columns={
        "vendor_name_1": "vendor_name",
        "invoice_number_1": "invoice_number",
        "payment_id_1": "payment_id_first",
        "payment_date_1": "payment_date_first",
        "payment_id_2": "payment_id_second",
        "payment_date_2": "payment_date_second",
    }
)

result = result.sort_values(
    ["vendor_name", "invoice_number", "payment_date_first", "payment_date_second"]
)

result.to_csv(OUTPUT_FILE, index=False)
print(f"Found {len(result)} possible duplicate payment pair(s). Written to {OUTPUT_FILE}")
