import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
data_path = Path("Data/cleaned_hospital_events.csv")
output_dir = Path("Data")
df = pd.read_csv(data_path)
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df = df.sort_values(["Case_ID", "Timestamp"])
case_sequences = (
    df.groupby("Case_ID")["Activity_Name"]
    .agg(lambda activities: " -> ".join(activities))
    .reset_index(name="Workflow_Sequence")
)
variant_summary=(
    case_sequences.groupby("Workflow_Sequence")
    .agg(Number_of_Cases=("Case_ID", "count"))
    .reset_index()
    .sort_values("Number_of_Cases", ascending=False)
)
total_cases = case_sequences["Case_ID"].nunique()
variant_summary["Percentage_of_Cases"] = (
    variant_summary["Number_of_Cases"] / total_cases * 100
).round(2)
case_sequences.to_csv(
    output_dir / "case_workflow_sequences.csv",
    index=False
)
variant_summary.to_csv(
    output_dir / "workflow_variant_summary.csv",
    index=False
)
print("\nCASE WORKFLOW SEQUENCES")
print(case_sequences.to_string(index=False))
print("\nWORKFLOW VARIANT SUMMARY")
print(variant_summary.to_string(index=False))
print(f"\nTotal cases analysed: {total_cases}")
print(f"Unique workflow variants: {len(variant_summary)}")
if not variant_summary.empty:
    chart_data = variant_summary.head(10).sort_values(
        "Number_of_Cases",
        ascending=True
    )
    plt.figure(figsize=(12, 7))
    plt.barh(
        chart_data["Workflow_Sequence"],
        chart_data["Number_of_Cases"]
    )
    plt.xlabel("Number of Cases")
    plt.ylabel("Workflow Sequence")
    plt.title("Most Frequent Clinical Workflow Variants")
    plt.tight_layout()
    plt.savefig(
        output_dir / "workflow_variant_chart.png",
        dpi=300
    )
    plt.close()
    print("\nWorkflow variant chart saved successfully.")
print("\nWorkflow variant analysis completed!")