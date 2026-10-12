import pandas as pd

INPUT_FILE = "ap_payments.csv"
OUTPUT_FILE = "duplicate_payment_exceptions.csv"
WINDOW_DAYS = 30

df = pd.read_csv(INPUT_FILE, dtype={"invoice_number": str})
df["payment_date"] = pd.to_datetime(df["payment_date"], errors="coerce")
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
df = df.dropna(subset=["vendor_name", "invoice_number", "amount", "payment_date"]).copy()

# Normalized match keys (original values are preserved in the output)
df["_vendor"] = df["vendor_name"].str.strip().str.casefold()
df["_invoice"] = df["invoice_number"].str.strip().str.casefold()
df["_amount"] = df["amount"].round(2)

keys = ["_vendor", "_invoice", "_amount"]
df["_row"] = range(len(df))

# Self-join on the match keys, keeping each pair once
pairs = df.merge(df, on=keys, suffixes=("_1", "_2"))
pairs = pairs[pairs["_row_1"] < pairs["_row_2"]]

pairs["days_apart"] = (pairs["payment_date_2"] - pairs["payment_date_1"]).abs().dt.days
pairs = pairs[pairs["days_apart"] <= WINDOW_DAYS]

result = pairs[
    [
        "vendor_name_1",
        "invoice_number_1",
        "amount_1",
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
        "amount_1": "amount",
    }
)

result = result.sort_values(
    ["vendor_name", "invoice_number", "payment_date_1", "payment_date_2"]
).reset_index(drop=True)

result.to_csv(OUTPUT_FILE, index=False)
print(f"Found {len(result)} possible duplicate payment pair(s). Written to {OUTPUT_FILE}")
