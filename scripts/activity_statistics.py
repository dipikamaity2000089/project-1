import pandas as pd
from pathlib import Path

input_file = Path("data/cleaned_hospital_events.csv")
output_file = Path("data/activity_statistics.csv")

df = pd.read_csv(input_file)
df.columns = df.columns.str.strip()  # Remove leading/trailing whitespace from column names

required_columns = [
"Activity_Name",
"Activity_Start_Time",
"Activity_End_Time"
]

missing_columns = [
column for column in required_columns
if column not in df.columns
]

if missing_columns:
 raise ValueError(f"Missing required columns: {missing_columns}")

df["Activity_Start_Time"] = pd.to_datetime(
df["Activity_Start_Time"], errors="coerce"
)

df["Activity_End_Time"] = pd.to_datetime(
df["Activity_End_Time"], errors="coerce"
)

df = df.dropna(subset=required_columns)

df["Duration_Minutes"] = (
df["Activity_End_Time"] - df["Activity_Start_Time"]
).dt.total_seconds() / 60

df = df[df["Duration_Minutes"] >= 0]

if df.empty:
 raise ValueError("No valid activity records are available.")

summary = df.groupby("Activity_Name").agg(
Event_Count=("Activity_Name", "size"),
Average_Duration_Minutes=("Duration_Minutes", "mean"),
Minimum_Duration_Minutes=("Duration_Minutes", "min"),
Maximum_Duration_Minutes=("Duration_Minutes", "max")
).reset_index()

summary["Average_Duration_Minutes"] = (
summary["Average_Duration_Minutes"].round(2)
)

summary.to_csv(output_file, index=False)

print("CAREFLOW ACTIVITY STATISTICS")
print("-" * 35)
print("Total valid events:", len(df))
print("Unique activities:", df["Activity_Name"].nunique())
print()
print(summary.to_string(index=False))
print()
print("Report saved to:", output_file)