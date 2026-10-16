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

durations = {
    "Registration": (5, 10),
    "Triage": (5, 15),
    "Doctor Consultation": (10, 25),
    "Lab Test": (15, 30),
    "X-Ray": (10, 20),
    "Treatment": (15, 30),
    "Discharge": (5, 10)
}

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
        start_time = current_time

        duration_minutes = random.randint(
            durations[activity][0],
            durations[activity][1]
        )

        end_time = start_time + timedelta(
            minutes=duration_minutes
        )

        all_events.append([
            patient_id,
            activity,
            start_time.strftime("%Y-%m-%d %H:%M:%S"),
            start_time.strftime("%Y-%m-%d %H:%M:%S"),
            end_time.strftime("%Y-%m-%d %H:%M:%S")
        ])

        waiting_minutes = random.randint(5, 30)
        current_time = end_time + timedelta(
            minutes=waiting_minutes
        )

output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Case_ID",
        "Activity_Name",
        "Timestamp",
        "Activity_Start_Time",
        "Activity_End_Time"
    ])
    writer.writerows(all_events)

print("Hospital event CSV created successfully!")
print("Number of patients:", 10)
print("Number of events:", len(all_events))
print("Saved to:", output_file)