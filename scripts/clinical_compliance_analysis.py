
import pandas as pd
from pathlib import Path
data_path = Path("Data/cleaned_hospital_events.csv")
output_path = Path("Data/clinical_compliance_report.csv")
df = pd.read_csv(data_path)
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df = df.sort_values(["Case_ID", "Timestamp"])
reference_workflow = [
    "Registration",
    "Triage",
    "Doctor Consultation",
    "Lab Test",
    "Treatment",
    "Discharge"
]
results = []
for case_id, group in df.groupby("Case_ID"):
    activities = group["Activity_Name"].tolist()
    matches_reference = activities == reference_workflow

    results.append({
        "Case_ID": case_id,
        "Observed_Activities": " -> ".join(activities),
        "Number_of_Activities": len(activities),
        "Matches_Reference_Workflow": matches_reference
    })
report = pd.DataFrame(results)
report.to_csv(output_path, index=False)
print("\nCLINICAL WORKFLOW COMPARISON")
print(report.to_string(index=False))
print("\nTotal cases analysed:", len(report))
print(
    "Cases matching reference workflow:",
    report["Matches_Reference_Workflow"].sum()
)
print("\nReport saved to:", output_path)
print("\nAnalysis completed successfully!")