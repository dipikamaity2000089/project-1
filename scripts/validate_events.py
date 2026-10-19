import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_DIR / "data" / "cleaned_hospital_events.csv"

REQUIRED_COLUMNS = [
    "Case_ID",
    "Activity_Name",
    "Timestamp",
    "Activity_Start_Time",
    "Activity_End_Time"
]

def main():
    print("CAREFLOW DATA VALIDATION")
    print("-" * 35)

    if not FILE_PATH.exists():
        print(f"Dataset not found: {FILE_PATH}")
        return

    df = pd.read_csv(FILE_PATH)

    print("Total events:", len(df))

    missing_columns = [
        col for col in REQUIRED_COLUMNS if col not in df.columns
    ]

    if missing_columns:
        print("Missing columns:", missing_columns)
        return

    print("Required columns: PASS")
    print("Unique patients:", df["Case_ID"].nunique())
    print("Missing values:", int(df[REQUIRED_COLUMNS].isnull().sum().sum()))
    print("Duplicate rows:", int(df.duplicated().sum()))

    timestamp_columns = [
        "Timestamp",
        "Activity_Start_Time",
        "Activity_End_Time"
    ]

    invalid_timestamps = {}

    for column in timestamp_columns:
        parsed = pd.to_datetime(df[column], errors="coerce")
        invalid_timestamps[column] = int(parsed.isnull().sum())

    total_invalid = sum(invalid_timestamps.values())

    print("Invalid timestamps:", total_invalid)

    for column, count in invalid_timestamps.items():
        print(f"  {column}: {count} invalid")

    start_times = pd.to_datetime(
        df["Activity_Start_Time"], errors="coerce"
    )
    end_times = pd.to_datetime(
        df["Activity_End_Time"], errors="coerce"
    )

    invalid_durations = int((end_times < start_times).sum())

    print("Invalid durations:", invalid_durations)

    passed = (
        df[REQUIRED_COLUMNS].notnull().all().all()
        and df["Case_ID"].astype(str).str.strip().ne("").all()
        and df["Activity_Name"].astype(str).str.strip().ne("").all()
        and total_invalid == 0
        and invalid_durations == 0
        and df.duplicated().sum() == 0
    )

    print("-" * 35)
    print("Overall validation:", "PASS" if passed else "FAIL")
    print("Validation completed.")

if __name__ == "__main__":
    main()