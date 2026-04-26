"""
copy_legacy_data.py
-------------------
Copies source files from legacy folder locations into the workings/data/raw/
folder for the current period.

HOW TO USE
----------
1. Fill in the LEGACY_FILES list below with your actual file paths.
2. Set DESTINATION_FOLDER to the data/raw/ path inside your workings folder.
3. Run once per period. The script never modifies the source files.
4. A run log is written to the destination folder automatically.

IMPORTANT
---------
- Source files are NEVER modified, moved, or deleted.
- If a file already exists in the destination, you will be prompted before overwrite.
- Do not commit data/raw/ to git. Keep it in .gitignore.
"""

import shutil
import os
import logging
from datetime import datetime
from pathlib import Path

# =============================================================================
# CONFIGURATION -- Fill in these values before running
# =============================================================================

# List each legacy file you need for this period.
# Format: ("description", r"PASTE_FULL_PATH_HERE")
# Example: ("Bank export April", r"C:\Finance\Bank\2026\April_bank.csv")

LEGACY_FILES = [
    ("GL export",           r"LEGACY_PATH_PLACEHOLDER\gl_export.xlsx"),
    ("Bank statement",      r"LEGACY_PATH_PLACEHOLDER\bank_april.csv"),
    ("Payroll summary",     r"LEGACY_PATH_PLACEHOLDER\payroll_summary.xlsx"),
    # Add more files as needed
]

# Full path to your workings/data/raw/ folder.
# Example: r"C:\Finance\Budget\2026\workings\data\raw"
DESTINATION_FOLDER = r"DESTINATION_PATH_PLACEHOLDER\workings\data\raw"

# =============================================================================
# END CONFIGURATION
# =============================================================================


def setup_logging(destination: Path) -> None:
    log_path = destination / f"{datetime.today().strftime('%Y-%m-%d')}_import_log.txt"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    logging.info(f"Run log: {log_path}")


def validate_config() -> None:
    for desc, path in LEGACY_FILES:
        if "LEGACY_PATH_PLACEHOLDER" in path:
            raise ValueError(
                f"Placeholder path not filled in for: '{desc}'\n"
                f"  Edit LEGACY_FILES in this script before running."
            )
    if "DESTINATION_PATH_PLACEHOLDER" in DESTINATION_FOLDER:
        raise ValueError(
            "DESTINATION_FOLDER is still a placeholder.\n"
            "  Edit DESTINATION_FOLDER in this script before running."
        )


def copy_files(legacy_files: list, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    copied = 0
    skipped = 0

    for description, source_path in legacy_files:
        source = Path(source_path)

        if not source.exists():
            logging.warning(f"NOT FOUND   | {description} | {source}")
            skipped += 1
            continue

        dest_file = destination / source.name

        if dest_file.exists():
            answer = input(
                f"\n  File already exists: {dest_file.name}\n"
                f"  Overwrite? (y/n): "
            ).strip().lower()
            if answer != "y":
                logging.info(f"SKIPPED     | {description} | {source.name} (user skipped)")
                skipped += 1
                continue

        shutil.copy2(source, dest_file)
        logging.info(f"COPIED      | {description} | {source} -> {dest_file}")
        copied += 1

    logging.info(f"Done. Copied: {copied}  |  Skipped/not found: {skipped}")


def main() -> None:
    try:
        validate_config()
    except ValueError as e:
        print(f"\nConfiguration error:\n  {e}\n")
        return

    destination = Path(DESTINATION_FOLDER)
    setup_logging(destination)

    logging.info("=" * 60)
    logging.info("Legacy Data Import")
    logging.info(f"Destination: {destination}")
    logging.info(f"Files to import: {len(LEGACY_FILES)}")
    logging.info("=" * 60)

    copy_files(LEGACY_FILES, destination)


if __name__ == "__main__":
    main()
