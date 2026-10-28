import pandas as pd
import matplotlib.pyplot as plt

input_file = "data/process_mining_transitions.csv"
output_file = "data/hospital_workflow.png"

df = pd.read_csv(input_file)

df = df.sort_values("Frequency", ascending=True)

labels = (
    df["From_Activity"].astype(str)
    + " → "
    + df["To_Activity"].astype(str)
)

plt.figure(figsize=(12, 7))
plt.barh(labels, df["Frequency"])
plt.xlabel("Transition Frequency")
plt.ylabel("Hospital Activity Transition")
plt.title("CareFlow Hospital Workflow Transition Analysis")
plt.tight_layout()

plt.savefig(output_file, dpi=300, bbox_inches="tight")
plt.show()

print(f"Workflow visualization saved to: {output_file}")