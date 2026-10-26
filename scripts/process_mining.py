import pandas as pd

input_file = "data/cleaned_hospital_events.csv"
output_file = "data/process_mining_transitions.csv"

df = pd.read_csv(input_file)

df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
df = df.dropna(subset=["Case_ID", "Activity_Name", "Timestamp"])
df = df.sort_values(["Case_ID", "Timestamp"])

print("\n===== CAREFLOW PROCESS ANALYSIS =====")
print(f"Total events: {len(df)}")
print(f"Total patients: {df['Case_ID'].nunique()}")
print(f"Unique activities: {df['Activity_Name'].nunique()}")

print("\n===== ACTIVITIES PER PATIENT =====")
print(df.groupby("Case_ID")["Activity_Name"].count().to_string())

df["Next_Activity"] = df.groupby("Case_ID")["Activity_Name"].shift(-1)

transitions = (
    df.dropna(subset=["Next_Activity"])
    .groupby(["Activity_Name", "Next_Activity"])
    .size()
    .reset_index(name="Frequency")
    .rename(columns={
        "Activity_Name": "From_Activity",
        "Next_Activity": "To_Activity"
    })
    .sort_values("Frequency", ascending=False)
)

print("\n===== MOST COMMON ACTIVITY TRANSITIONS =====")
print(transitions.to_string(index=False))

transitions.to_csv(output_file, index=False)
print(f"\nResults saved to: {output_file}")