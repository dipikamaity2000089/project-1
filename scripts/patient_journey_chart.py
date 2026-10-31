import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

input_file = "data/cleaned_hospital_events.csv"
output_file = "data/patient_journey_chart.png"

df = pd.read_csv(input_file)

df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df = df.sort_values(["Case_ID", "Timestamp"])

patients = sorted(df["Case_ID"].unique())
activities = sorted(df["Activity_Name"].unique())

activity_colors = {
    activity: plt.cm.tab10(i % 10)
    for i, activity in enumerate(activities)
}

fig, ax = plt.subplots(figsize=(15, 8))

for patient_index, patient in enumerate(patients):
    patient_data = df[df["Case_ID"] == patient]

    for _, row in patient_data.iterrows():
        ax.scatter(
            row["Timestamp"],
            patient_index,
            color=activity_colors[row["Activity_Name"]],
            s=100,
            label=row["Activity_Name"]
        )

    timestamps = patient_data["Timestamp"].tolist()

    if len(timestamps) > 1:
        ax.plot(
            timestamps,
            [patient_index] * len(timestamps),
            color="gray",
            alpha=0.35,
            linewidth=1
        )

ax.set_yticks(range(len(patients)))
ax.set_yticklabels(patients)
ax.set_xlabel("Activity Timestamp")
ax.set_ylabel("Patient Case ID")
ax.set_title("CareFlow - Patient Journey Timeline")

ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax.grid(axis="x", linestyle="--", alpha=0.4)

handles = [
    plt.Line2D(
        [0], [0],
        marker="o",
        color="w",
        markerfacecolor=activity_colors[activity],
        markersize=8,
        label=activity
    )
    for activity in activities
]

ax.legend(
    handles=handles,
    title="Hospital Activities",
    bbox_to_anchor=(1.02, 1),
    loc="upper left"
)

plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches="tight")
plt.show()

print(f"Patient journey visualization saved to {output_file}")