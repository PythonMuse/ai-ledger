"""
Verify that a CSV file has been properly masked before AI processing.

Checks that vendor names follow the masked pattern (Vendor_NN).
Raises ValueError if unmasked data is detected.

Usage:
    python verify_masking.py
"""

import pandas as pd
import re

def verify_file_is_masked(file_path):
    df = pd.read_csv(file_path)

    vendor_pattern = r"^Vendor_\d+$"
    for v in df["Vendor"]:
        if not re.match(vendor_pattern, str(v)):
            raise ValueError(f"Unmasked vendor name detected: {v}")

    print("File passed masking validation.")

if __name__ == "__main__":
    verify_file_is_masked("qb_masked_export.csv")
