import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
data_path = Path("Data/cleaned_hospital_events.csv")
output_dir = Path("Data")
df = pd.read_csv(data_path)
activity_frequency = (
    df.groupby("Activity_Name")
    .size()
    .reset_index(name="Frequency")
    .sort_values("Frequency", ascending=False)
)
total_activities = activity_frequency["Frequency"].sum()

activity_frequency["Percentage"] = (
    activity_frequency["Frequency"] / total_activities * 100
).round(2)
activity_frequency.to_csv(
    output_dir / "clinical_activity_frequency.csv",
    index=False
)
print("\nCLINICAL ACTIVITY FREQUENCY ANALYSIS")
print(activity_frequency.to_string(index=False))
print("\nTotal activities:", total_activities)
print(
    "\nMost frequent activity:",
    activity_frequency.iloc[0]["Activity_Name"]
)
print(
    "\nLeast frequent activity:",
    activity_frequency.iloc[-1]["Activity_Name"]
)
plt.figure(figsize=(10, 6))
plt.bar(
    activity_frequency["Activity_Name"],
    activity_frequency["Frequency"]
)
plt.xlabel("Hospital Activities")
plt.ylabel("Frequency")
plt.title("Clinical Activity Frequency Analysis")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(
    output_dir / "clinical_activity_frequency_chart.png",
    dpi=300
)
plt.close()
print("\nCSV report and chart saved successfully!")
print("\nAnalysis completed successfully!")