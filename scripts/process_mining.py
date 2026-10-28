import pandas as pd
import pm4py
df = pd.read_csv("data/updated_hospital_events.csv")
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df["Activity_Start_Time"] = pd.to_datetime(
    df["Activity_Start_Time"]
)
df["Activity_End_Time"] = pd.to_datetime(
    df["Activity_End_Time"]
)
df = df.sort_values(
    by=["Case_ID", "Activity_Start_Time"]
)
event_log = pm4py.format_dataframe(
    df,
    case_id="Case_ID",
    activity_key="Activity_Name",
    timestamp_key="Timestamp"
)
process_tree = pm4py.discover_process_tree_inductive(
    event_log
)
print("Process mining completed successfully!")
print(process_tree)
pm4py.view_process_tree(process_tree)
pm4py.view_process_tree(process_tree)
pm4py.save_vis_process_tree(
    process_tree,
    "Data/process_tree.png"
)