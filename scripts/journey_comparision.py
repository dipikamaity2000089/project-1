import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/cleaned_hospital_events.csv")

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

df = df.sort_values(["Case_ID", "Timestamp"])

patients = sorted(df["Case_ID"].unique())

if len(patients) < 2:
    raise ValueError("At least two patients are required.")

patient1 = patients[0]
patient2 = patients[1]

def get_patient_details(patient_id):
    patient_data = df[df["Case_ID"] == patient_id]

    activities = patient_data["Activity_Name"].tolist()

    start = patient_data["Timestamp"].min()
    end = patient_data["Timestamp"].max()

    duration = (end - start).total_seconds() / 60

    return activities, duration

activities1, duration1 = get_patient_details(patient1)
activities2, duration2 = get_patient_details(patient2)

print("PATIENT JOURNEY COMPARISON")
print("-" * 40)

print(f"\nPatient 1: {patient1}")
print("Activities:", " -> ".join(activities1))
print(f"Journey Duration: {duration1:.2f} minutes")

print(f"\nPatient 2: {patient2}")
print("Activities:", " -> ".join(activities2))
print(f"Journey Duration: {duration2:.2f} minutes")

print("\nDuration Difference:",
      f"{abs(duration1 - duration2):.2f} minutes")

comparison = pd.DataFrame({
    "Patient": [patient1, patient2],
    "Activity_Count": [len(activities1), len(activities2)],
    "Journey_Minutes": [duration1, duration2]
})

comparison.to_csv(
    "data/patient_journey_comparison.csv",
    index=False
)

plt.figure(figsize=(8, 5))

plt.bar(
    comparison["Patient"],
    comparison["Journey_Minutes"]
)

plt.title("Patient Journey Duration Comparison")
plt.xlabel("Patient ID")
plt.ylabel("Journey Duration (Minutes)")
plt.tight_layout()

plt.savefig("data/patient_journey_comparison.png")
plt.show()

print("\nComparison report generated successfully.")