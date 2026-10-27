import pandas as pd
from pathlib import Path
data_path = Path("Data/cleaned_hospital_events.csv")
df = pd.read_csv(data_path)
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df = df.sort_values(["Case_ID", "Timestamp"])
df["Next_Activity"] = (
    df.groupby("Case_ID")["Activity_Name"].shift(-1)
)
sequence_df = df.dropna(subset=["Next_Activity"]).copy()
sequence_summary = (
    sequence_df.groupby(["Activity_Name", "Next_Activity"])
    .size()
    .reset_index(name="Frequency")
    .sort_values("Frequency", ascending=False)
)
output_path = Path("Data/activity_sequence_summary.csv")
sequence_summary.to_csv(output_path, index=False)
print("\nActivity Sequence Analysis")
print(sequence_summary.to_string(index=False))
print(f"\nAnalysis completed successfully!")
print(f"Results saved to: {output_path}")