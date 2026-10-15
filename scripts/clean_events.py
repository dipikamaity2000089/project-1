import csv
from datetime import datetime
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent

input_file = project_folder / "data" / "hospital_events.csv"
output_file = project_folder / "data" / "cleaned_hospital_events.csv"

cleaned_events = []
seen_events = set()
removed_duplicates = 0
removed_invalid = 0

with open(input_file, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    required_columns = ["Case_ID", "Activity_Name", "Timestamp"]

    if reader.fieldnames != required_columns:
        raise ValueError("CSV columns do not match the expected format.")

    for row in reader:
        case_id = row["Case_ID"].strip()
        activity = row["Activity_Name"].strip()
        timestamp = row["Timestamp"].strip()

        if not case_id or not activity or not timestamp:
            removed_invalid += 1
            continue

        try:
            datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            removed_invalid += 1
            continue

        event = (case_id, activity, timestamp)

        if event in seen_events:
            removed_duplicates += 1
            continue

        seen_events.add(event)

        cleaned_events.append({
            "Case_ID": case_id,
            "Activity_Name": activity,
            "Timestamp": timestamp
        })

cleaned_events.sort(
    key=lambda row: (row["Case_ID"], row["Timestamp"])
)

with open(output_file, "w", newline="", encoding="utf-8") as file:
    columns = ["Case_ID", "Activity_Name", "Timestamp"]
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(cleaned_events)

print("Data cleaning completed!")
print("Original file:", input_file.name)
print("Cleaned file:", output_file.name)
print("Valid events:", len(cleaned_events))
print("Duplicates removed:", removed_duplicates)
print("Invalid rows removed:", removed_invalid)
print("Output saved to:", output_file)