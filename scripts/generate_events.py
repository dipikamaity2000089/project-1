import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

output_file = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "hospital_events.csv"
)

activities = [
    "Registration",
    "Triage",
    "Doctor Consultation",
    "Lab Test",
    "X-Ray",
    "Treatment",
    "Discharge"
]

all_events = []

for patient_number in range(1, 11):
    patient_id = f"P{patient_number:03d}"
    current_time = datetime(2026, 10, 13, 9, 0)
    current_time += timedelta(minutes=random.randint(0, 60))

    patient_activities = [
        "Registration",
        "Triage",
        "Doctor Consultation"
    ]

    if random.random() < 0.4:
        patient_activities.append("Triage")

    test_activity = random.choice(["Lab Test", "X-Ray"])

    patient_activities.extend([
        test_activity,
        "Treatment",
        "Discharge"
    ])

    for activity in patient_activities:
        all_events.append([
            patient_id,
            activity,
            current_time.strftime("%Y-%m-%d %H:%M:%S")
        ])

        current_time += timedelta(minutes=random.randint(5, 30))

output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Case_ID", "Activity_Name", "Timestamp"])
    writer.writerows(all_events)

print("Hospital event CSV created successfully!")
print("Number of patients:", 10)
print("Number of events:", len(all_events))
print("Saved to:", output_file)