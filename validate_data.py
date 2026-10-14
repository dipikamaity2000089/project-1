import csv
from datetime import datetime
from pathlib import Path

# Always locate the CSV relative to this Python script
project_dir = Path(__file__).resolve().parent
file_path = project_dir / "data" / "sample_event_log.csv"

required_columns = {
    "case_id",
    "activity",
    "timestamp",
    "department",
}

print("Reading CSV:", file_path)

if not file_path.is_file():
    print("ERROR: Sample event log file not found.")
    raise SystemExit(1)

with file_path.open("r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    if not reader.fieldnames:
        print("ERROR: CSV file is empty or has no header.")
        raise SystemExit(1)

    # Remove accidental spaces from column names
    reader.fieldnames = [name.strip() for name in reader.fieldnames]

    missing_columns = required_columns - set(reader.fieldnames)

    if missing_columns:
        print("ERROR: Missing columns:", sorted(missing_columns))
        print("Found columns:", reader.fieldnames)
        raise SystemExit(1)

    rows = list(reader)

errors = []

for row_number, row in enumerate(rows, start=2):
    for column in required_columns:
        value = row.get(column)

        if value is None or not value.strip():
            errors.append(f"Row {row_number}: {column} is empty")

    timestamp = (row.get("timestamp") or "").strip()

    try:
        datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
    except ValueError:
        errors.append(f"Row {row_number}: Invalid timestamp")

if not rows:
    errors.append("No event records found")

if errors:
    print("\nVALIDATION FAILED")

    for error in errors:
        print("-", error)

    raise SystemExit(1)

case_ids = {row["case_id"].strip() for row in rows}

print("\nVALIDATION PASSED")
print("Total events:", len(rows))
print("Total cases:", len(case_ids))
print("Required columns: OK")
print("Missing values: None")
print("Timestamps: Valid")
