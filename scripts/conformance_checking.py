import pandas as pd
import pm4py
from pathlib import Path
data_path = Path("Data/cleaned_hospital_events.csv")
output_path = Path("Data/conformance_results.csv")
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
replay_results = pm4py.conformance_diagnostics_token_based_replay(
    event_log,
    net,
    initial_marking,
    final_marking
)
results = []
for index, result in enumerate(replay_results):
    results.append({
        "Case_ID": event_log["case:concept:name"].iloc[
            event_log["case:concept:name"].drop_duplicates().index[index]
        ],
        "Is_Fit": result["trace_is_fit"],
        "Trace_Fitness": result["trace_fitness"],
        "Missing_Tokens": result["missing_tokens"],
        "Remaining_Tokens": result["remaining_tokens"]
    })
report = pd.DataFrame(results)
report.to_csv(output_path, index=False)
print("\nCONFORMANCE CHECKING RESULTS")
print(report.to_string(index=False))
print("\nTotal Cases:", len(report))
print("Fitting Cases:", report["Is_Fit"].sum())
print(
    "Average Trace Fitness:",
    round(report["Trace_Fitness"].mean(), 2)
)
print("\nReport saved successfully!")