"""
Mask sensitive fields in an accounting data export.

Replaces real vendor names with generic placeholders and randomizes
financial amounts while preserving the file structure.

Usage:
    python mask_finance_data.py
"""

import pandas as pd
import random

def mask_finance_file(input_file, output_file):
    df = pd.read_csv(input_file)

    vendor_map = {v: f"Vendor_{i:02d}"
                  for i, v in enumerate(df["Vendor"].unique(), start=1)}
    df["Vendor"] = df["Vendor"].map(vendor_map)

    df["Amount"] = df["Amount"].apply(lambda x: round(random.uniform(100, 10000), 2))

    df.to_csv(output_file, index=False)
    print(f"Masked file created: {output_file}")

if __name__ == "__main__":
    mask_finance_file("qb_raw_export.csv", "qb_masked_export.csv")
