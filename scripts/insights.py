import pandas as pd
from collections import Counter

df = pd.read_csv("data/cleaned_hospital_events.csv")

df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df = df.sort_values(["Case_ID", "Timestamp"])

activity_counts = df["Activity_Name"].value_counts()

transitions = []

for patient_id, group in df.groupby("Case_ID"):
    activities = group["Activity_Name"].tolist()
    transitions.extend(zip(activities, activities[1:]))

transition_counts = Counter(transitions)

journey_durations = (
    df.groupby("Case_ID")["Timestamp"]
    .agg(lambda x: (x.max() - x.min()).total_seconds() / 60)
)

most_common_activity = activity_counts.idxmax()
least_common_activity = activity_counts.idxmin()
most_common_transition = transition_counts.most_common(1)[0]
longest_patient = journey_durations.idxmax()

report = f"""
CARE­FLOW - HOSPITAL WORKFLOW INSIGHTS
======================================

Total Events: {len(df)}
Total Patients: {df["Case_ID"].nunique()}
Unique Activities: {df["Activity_Name"].nunique()}

MOST FREQUENT ACTIVITY
{most_common_activity}: {activity_counts.max()} times

LEAST FREQUENT ACTIVITY
{least_common_activity}: {activity_counts.min()} times

MOST COMMON ACTIVITY TRANSITION
{most_common_transition[0][0]} -> {most_common_transition[0][1]}
Count: {most_common_transition[1]}

LONGEST PATIENT JOURNEY
Patient: {longest_patient}
Duration: {journey_durations.max():.2f} minutes

======================================
Analysis based on synthetic hospital data.
"""

with open("data/hospital_workflow_insights.txt", "w") as file:
    file.write(report)

print(report)
print("Workflow insights report generated successfully!")