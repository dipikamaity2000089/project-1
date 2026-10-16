import pandas as pd
df = pd.read_csv("data/updated_hospital_events.csv")
df["Activity_Start_Time"] = pd.to_datetime(
    df["Activity_Start_Time"], errors="coerce"
)
df["Activity_End_Time"] = pd.to_datetime(
    df["Activity_End_Time"], errors="coerce"
)
df["Activity_Duration_Minutes"] = (
    df["Activity_End_Time"] - df["Activity_Start_Time"]
).dt.total_seconds() / 60
df = df.sort_values(["Case_ID", "Activity_Start_Time"])
df["Next_Activity_Start"] = (
    df.groupby("Case_ID")["Activity_Start_Time"].shift(-1)
)
df["Waiting_Time_Minutes"] = (
    df["Next_Activity_Start"] - df["Activity_End_Time"]
).dt.total_seconds() / 60
avg_duration = df.groupby("Activity_Name")[
    "Activity_Duration_Minutes"
].mean().sort_values(ascending=False)
avg_waiting = df.groupby("Activity_Name")[
    "Waiting_Time_Minutes"
].mean().sort_values(ascending=False)
print("\nAverage Activity Duration (Minutes):")
print(avg_duration.round(2))
print("\nAverage Waiting Time After Activity (Minutes):")
print(avg_waiting.round(2))
avg_duration.to_csv("data/average_activity_duration.csv")
avg_waiting.to_csv("data/average_waiting_time.csv")
print("\nAnalysis completed successfully!")