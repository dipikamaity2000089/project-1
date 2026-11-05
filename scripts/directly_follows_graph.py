import pandas as pd
import pm4py
from pathlib import Path
data_path = Path("Data/cleaned_hospital_events.csv")
output_dir = Path("Data")
output_dir.mkdir(exist_ok=True)
df = pd.read_csv(data_path)
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
event_log = pm4py.format_dataframe(
    df,
    case_id="Case_ID",
    activity_key="Activity_Name",
    timestamp_key="Timestamp"
)
dfg, start_activities, end_activities = (
    pm4py.discover_dfg(event_log)
)
print("\nDIRECTLY-FOLLOWS GRAPH ANALYSIS")
print("\nActivity Transitions and Frequencies:")
for transition, frequency in sorted(
    dfg.items(),
    key=lambda item: item[1],
    reverse=True
):
    print(
        f"{transition[0]} -> {transition[1]} : {frequency}"
    )
print("\nStart Activities:")
print(start_activities)
print("\nEnd Activities:")
print(end_activities)
gviz = pm4py.visualization.dfg.visualizer.apply(
    dfg,
    log=event_log,
    variant=pm4py.visualization.dfg.visualizer.Variants.FREQUENCY
)
pm4py.visualization.dfg.visualizer.save(
    gviz,
    str(output_dir / "directly_follows_graph.png")
)
transition_data = [
    {
        "From_Activity": transition[0],
        "To_Activity": transition[1],
        "Frequency": frequency
    }
    for transition, frequency in dfg.items()
]
transition_df = pd.DataFrame(transition_data)
transition_df.to_csv(
    output_dir / "directly_follows_graph.csv",
    index=False
)
print("\nDFG Chart and CSV Report saved successfully!")
print("\nDFG Discovery completed!")