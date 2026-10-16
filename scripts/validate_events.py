
import pandas as pd
from pathlib import Path

file_path = Path("data/cleaned_hospital_events.csv")

df = pd.read_csv(file_path)

required_columns = ["Case_ID", "Activity_Name", "Timestamp"]

print("CARE­FLOW DATA VALIDATION")
print("-" * 30)

print("Total events:", len(df))
print("Unique patients:", df["Case_ID"].nunique())

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    print("Missing columns:", missing_columns)
else:
    print("Required columns: PASS")

print("Missing values:", df.isnull().sum().sum())
print("Duplicate rows:", df.duplicated().sum())

timestamps = pd.to_datetime(df["Timestamp"], errors="coerce")

print("Invalid timestamps:", timestamps.isnull().sum())

if timestamps.isnull().sum() == 0:
    print("Timestamp validation: PASS")
else:
    print("Timestamp validation: FAIL")

print("-" * 30)
print("Validation completed.")
