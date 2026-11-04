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
net, initial_marking, final_marking = (
    pm4py.discover_petri_net_inductive(event_log)
)
print("Petri Net discovered successfully!")
print("\nPetri Net Details")
print("Places:", len(net.places))
print("Transitions:", len(net.transitions))
print("Arcs:", len(net.arcs))
print("\nInitial Marking:")
print(initial_marking)
print("\nFinal Marking:")
print(final_marking)
pm4py.save_vis_petri_net(
    net,
    initial_marking,
    final_marking,
    str(output_dir / "petri_net_model.png")
)
print("\nPetri Net visualization saved successfully!")
print("\nProcess Mining completed!")