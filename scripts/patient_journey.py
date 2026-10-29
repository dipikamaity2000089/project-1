import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
input_file = base_dir / "data" / "cleaned_hospital_events.csv"
output_file = base_dir / "data" / "patient_journey_analysis.csv"

df = pd.read_csv(input_file)

df["Activity_Start_Time"] = pd.to_datetime(
    df["Activity_Start_Time"], errors="coerce"
)

df["Activity_End_Time"] = pd.to_datetime(
    df["Activity_End_Time"], errors="coerce"
)

df = df.dropna(
    subset=["Case_ID", "Activity_Start_Time", "Activity_End_Time"]
)

df["Activity_Duration_Minutes"] = (
    df["Activity_End_Time"] - df["Activity_Start_Time"]
).dt.total_seconds() / 60

valid_events = df[df["Activity_Duration_Minutes"] >= 0]

summary = valid_events.groupby("Case_ID").agg(
    Activity_Count=("Activity_Name", "count"),
    First_Activity_Start=("Activity_Start_Time", "min"),
    Last_Activity_End=("Activity_End_Time", "max"),
    Total_Activity_Minutes=("Activity_Duration_Minutes", "sum")
).reset_index()

summary["Total_Journey_Minutes"] = (
    summary["Last_Activity_End"] - summary["First_Activity_Start"]
).dt.total_seconds() / 60

summary = summary.sort_values(
    "Total_Journey_Minutes", ascending=False
)

summary.to_csv(output_file, index=False)

print("===== PATIENT JOURNEY ANALYSIS =====")
print(f"Patients analyzed: {len(summary)}")
print("\nLongest patient journeys:")
print(summary[["Case_ID", "Total_Journey_Minutes"]].head(5).to_string(index=False))
print(f"\nResults saved to: {output_file}")