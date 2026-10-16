import pandas as pd
import matplotlib.pyplot as plt
df_duration = pd.read_csv("data/average_activity_duration.csv")
df_duration = df_duration.dropna()
plt.figure(figsize=(10, 6))
plt.bar(
    df_duration["Activity_Name"],
    df_duration["Activity_Duration_Minutes"]
)
plt.title("CareFlow: Average Activity Duration")
plt.xlabel("Hospital Activity")
plt.ylabel("Average Duration (Minutes)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("data/average_activity_duration_chart.png", dpi=300)
plt.show()
print("Activity Duration chart saved successfully!")
df_waiting = pd.read_csv("data/average_waiting_time.csv")
df_waiting = df_waiting.dropna()
plt.figure(figsize=(10, 6))
plt.bar(
    df_waiting["Activity_Name"],
    df_waiting["Waiting_Time_Minutes"]
)
plt.title("CareFlow: Average Waiting Time After Activity")
plt.xlabel("Hospital Activity")
plt.ylabel("Average Waiting Time (Minutes)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("data/average_waiting_time_chart.png", dpi=300)
plt.show()
print("Waiting Time chart saved successfully!")