import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
data_path = Path("Data/cleaned_hospital_events.csv")
output_dir = Path("Data")
output_dir.mkdir(exist_ok=True)
df = pd.read_csv(data_path)
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df = df.sort_values(["Case_ID", "Timestamp"])
df["Time_Interval_Minutes"] = (
    df.groupby("Case_ID")["Timestamp"]
    .diff()
    .dt.total_seconds() / 60
)
case_summary = df.groupby("Case_ID").agg(
    Total_Activities=("Activity_Name", "count"),
    First_Event=("Timestamp", "min"),
    Last_Event=("Timestamp", "max")
).reset_index()
case_summary["Total_Process_Time_Minutes"] = (
    case_summary["Last_Event"] - case_summary["First_Event"]
).dt.total_seconds() / 60
case_summary = case_summary.sort_values(
    "Total_Process_Time_Minutes",
    ascending=False
)

case_summary.to_csv(
    output_dir / "case_performance_summary.csv",
    index=False
)
print("\nCASE PERFORMANCE SUMMARY")
print(case_summary.to_string(index=False))
df["Next_Activity"] = (
    df.groupby("Case_ID")["Activity_Name"].shift(-1)
)
df["Next_Timestamp"] = (
    df.groupby("Case_ID")["Timestamp"].shift(-1)
)
transitions = df.dropna(subset=["Next_Activity"]).copy()
transitions["Transition_Time_Minutes"] = (
    transitions["Next_Timestamp"] - transitions["Timestamp"]
).dt.total_seconds() / 60
transition_summary = transitions.groupby(
    ["Activity_Name", "Next_Activity"]
).agg(
    Transition_Frequency=("Case_ID", "count"),
    Average_Interval_Minutes=("Transition_Time_Minutes", "mean"),
    Maximum_Interval_Minutes=("Transition_Time_Minutes", "max")
).reset_index()
transition_summary = transition_summary.sort_values(
    "Average_Interval_Minutes",
    ascending=False
)
transition_summary.to_csv(
    output_dir / "clinical_transition_analysis.csv",
    index=False
)
print("\nCLINICAL TRANSITION ANALYSIS")
print(transition_summary.to_string(index=False))
if not transition_summary.empty:
    chart_data = transition_summary.sort_values(
        "Average_Interval_Minutes",
        ascending=True
    )
    labels = (
        chart_data["Activity_Name"]
        + " -> "
        + chart_data["Next_Activity"]
    )
    plt.figure(figsize=(12, 7))
    plt.barh(labels, chart_data["Average_Interval_Minutes"])
    plt.xlabel("Average Time Interval (Minutes)")
    plt.ylabel("Activity Transition")
    plt.title("Average Time Interval Between Hospital Activities")
    plt.tight_layout()
    plt.savefig(
        output_dir / "clinical_transition_analysis_chart.png",
        dpi=300
    )
    plt.close()
    print("\nChart saved successfully.")
print("\nClinical performance analysis completed!")