import pandas as pd
import pm4py
from pathlib import Path
data_path = Path("Data/cleaned_hospital_events.csv")
output_path = Path("Data/process_model_evaluation.csv")
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
fitness = pm4py.fitness_token_based_replay(
    event_log,
    net,
    initial_marking,
    final_marking
)
precision = pm4py.precision_token_based_replay(
    event_log,
    net,
    initial_marking,
    final_marking
)
evaluation = pd.DataFrame([
    {
        "Metric": "Average Trace Fitness",
        "Score": fitness["average_trace_fitness"]
    },
    {
        "Metric": "Log Fitness",
        "Score": fitness["log_fitness"]
    },
    {
        "Metric": "Precision",
        "Score": precision
    }
])
evaluation.to_csv(output_path, index=False)
print("\nPROCESS MODEL QUALITY EVALUATION")
print(evaluation.to_string(index=False))
print("\nEvaluation report saved successfully!")
print("\nProcess Model Evaluation Completed!")