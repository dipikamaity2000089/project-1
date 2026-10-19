import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "cleaned_hospital_events.csv"
REPORT_FILE = BASE_DIR / "data" / "data_quality_report.txt"

def main():
    if not DATA_FILE.exists():
        print(f"Error: Dataset not found at {DATA_FILE}")
        return

    df = pd.read_csv(DATA_FILE)

    required_columns = [
        "Case_ID",
        "Activity_Name",
        "Timestamp",
        "Activity_Start_Time",
        "Activity_End_Time"
    ]

    print("\nCARE FLOW - DATA QUALITY REPORT")
    print("=" * 35)

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("Missing columns:", missing_columns)
        return

    df["Activity_Start_Time"] = pd.to_datetime(
        df["Activity_Start_Time"], errors="coerce"
    )
    df["Activity_End_Time"] = pd.to_datetime(
        df["Activity_End_Time"], errors="coerce"
    )

    missing_values = int(df[required_columns].isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    invalid_durations = int(
        (
            df["Activity_End_Time"] < df["Activity_Start_Time"]
        ).sum()
    )

    print(f"Total events: {len(df)}")
    print(f"Unique patients: {df['Case_ID'].nunique()}")
    print(f"Unique activities: {df['Activity_Name'].nunique()}")
    print(f"Missing values: {missing_values}")
    print(f"Duplicate rows: {duplicate_rows}")
    print(f"Invalid durations: {invalid_durations}")

    print("\nEVENT COUNT BY ACTIVITY")
    activity_counts = df["Activity_Name"].value_counts().sort_index()

    for activity, count in activity_counts.items():
        print(f"{activity}: {count}")

    report_lines = [
        "CARE FLOW - DATA QUALITY REPORT",
        "=" * 35,
        f"Total events: {len(df)}",
        f"Unique patients: {df['Case_ID'].nunique()}",
        f"Unique activities: {df['Activity_Name'].nunique()}",
        f"Missing values: {missing_values}",
        f"Duplicate rows: {duplicate_rows}",
        f"Invalid durations: {invalid_durations}",
        "",
        "EVENT COUNT BY ACTIVITY"
    ]

    for activity, count in activity_counts.items():
        report_lines.append(f"{activity}: {count}")

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8"
    )

    print(f"\nReport saved to: {REPORT_FILE}")

if __name__ == "__main__":
    main()