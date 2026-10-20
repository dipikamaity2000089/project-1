import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "cleaned_hospital_events.csv"
OUTPUT_FILE = BASE_DIR / "data" / "patient_summary.csv"

def main():
    if not INPUT_FILE.exists():
        print(f"Dataset not found: {INPUT_FILE}")
        return

    df = pd.read_csv(INPUT_FILE)

    required_columns = [
        "Case_ID",
        "Activity_Name",
        "Activity_Start_Time",
        "Activity_End_Time"
    ]

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

    if df[required_columns].isnull().any().any():
        print("Error: Missing or invalid required values found.")
        return

    if (df["Activity_End_Time"] < df["Activity_Start_Time"]).any():
        print("Error: Invalid activity durations found.")
        return

    summary = df.groupby("Case_ID").agg(
        Activity_Count=("Activity_Name", "count"),
        First_Activity_Start=("Activity_Start_Time", "min"),
        Last_Activity_End=("Activity_End_Time", "max")
    ).reset_index()

    summary["Total_Journey_Minutes"] = (
        summary["Last_Activity_End"] -
        summary["First_Activity_Start"]
    ).dt.total_seconds() / 60

    summary["Total_Journey_Minutes"] = (
        summary["Total_Journey_Minutes"].round(2)
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUTPUT_FILE, index=False)

    print("PATIENT SUMMARY REPORT")
    print("-" * 35)
    print("Patients summarized:", len(summary))
    print("Total events analyzed:", len(df))
    print("\nPatient summaries:")
    print(summary.to_string(index=False))
    print(f"\nReport saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()