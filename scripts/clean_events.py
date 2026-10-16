import pandas as pd
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent

input_file = project_dir / "data" / "hospital_events.csv"
output_file = project_dir / "data" / "cleaned_hospital_events.csv"

df = pd.read_csv(input_file)

required_columns = [
    "Case_ID",
    "Activity_Name",
    "Timestamp",
    "Activity_Start_Time",
    "Activity_End_Time"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")

df = df[required_columns].copy()

for column in [
    "Timestamp",
    "Activity_Start_Time",
    "Activity_End_Time"
]:
    df[column] = pd.to_datetime(df[column], errors="coerce")

df = df.dropna(subset=required_columns)

df = df.drop_duplicates()

df = df.sort_values(
    ["Case_ID", "Activity_Start_Time"]
).reset_index(drop=True)

invalid_durations = (
    df["Activity_End_Time"] < df["Activity_Start_Time"]
)

if invalid_durations.any():
    raise ValueError("Some activities end before they start.")

df.to_csv(output_file, index=False)

print("Data cleaning completed successfully!")
print("Total cleaned events:", len(df))
print("Unique patients:", df["Case_ID"].nunique())
print("Columns:", list(df.columns))
print("Missing values:", df.isnull().sum().sum())
print("Saved to:", output_file)