import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
data_path = Path("Data/cleaned_hospital_events.csv")
output_dir = Path("Data")
output_dir.mkdir(exist_ok=True)
df = pd.read_csv(data_path)
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df = df.sort_values(["Case_ID", "Timestamp"])
df["Next_Activity"] = df.groupby("Case_ID")["Activity_Name"].shift(-1)
df["Next_Timestamp"] = df.groupby("Case_ID")["Timestamp"].shift(-1)
transitions = df.dropna(subset=["Next_Activity"]).copy()
transitions["Time_Interval_Minutes"] = (
    transitions["Next_Timestamp"] - transitions["Timestamp"]
).dt.total_seconds() / 60
performance = transitions.groupby(
    ["Activity_Name", "Next_Activity"]
).agg(
    Frequency=("Case_ID", "count"),
    Average_Time_Minutes=("Time_Interval_Minutes", "mean"),
    Maximum_Time_Minutes=("Time_Interval_Minutes", "max"),
    Minimum_Time_Minutes=("Time_Interval_Minutes", "min")
).reset_index()
performance = performance.sort_values(
    "Average_Time_Minutes",
    ascending=False
)
performance.to_csv(
    output_dir / "performance_dfg_analysis.csv",
    index=False
)
print("\nPERFORMANCE DFG ANALYSIS")
print(performance.to_string(index=False))
if not performance.empty:
    print("\nHighest Average Time Transition:")
    print(performance.iloc[0])
    print("\nLowest Average Time Transition:")
    print(performance.iloc[-1])
if not performance.empty:
    chart_data = performance.sort_values(
        "Average_Time_Minutes",
        ascending=True
    )
    labels = (
        chart_data["Activity_Name"]
        + " -> "
        + chart_data["Next_Activity"]
    )
    plt.figure(figsize=(12, 7))
    plt.barh(labels, chart_data["Average_Time_Minutes"])
    plt.xlabel("Average Time Interval (Minutes)")
    plt.ylabel("Activity Transitions")
    plt.title("Performance Directly-Follows Graph Analysis")
    plt.tight_layout()
    plt.savefig(
        output_dir / "performance_dfg_chart.png",
        dpi=300
    )
    plt.close()
print("\nPerformance DFG CSV and Chart saved successfully!")
print("\nAnalysis completed!")