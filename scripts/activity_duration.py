import pandas as pd
import matplotlib.pyplot as plt

input_file = "data/cleaned_hospital_events.csv"
output_file = "data/activity_duration_chart.png"

df = pd.read_csv(input_file)

df["Activity_Start_Time"] = pd.to_datetime(df["Activity_Start_Time"])
df["Activity_End_Time"] = pd.to_datetime(df["Activity_End_Time"])

df["Duration_Minutes"] = (
    df["Activity_End_Time"] - df["Activity_Start_Time"]
).dt.total_seconds() / 60

activity_duration = (
    df.groupby("Activity_Name")["Duration_Minutes"]
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))

activity_duration.plot(kind="bar", edgecolor="black")

plt.title("Average Duration by Hospital Activity")
plt.xlabel("Hospital Activity")
plt.ylabel("Average Duration (Minutes)")
plt.xticks(rotation=35, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig(output_file, dpi=300)
plt.show()

print("Activity duration visualization completed!")
print(activity_duration)