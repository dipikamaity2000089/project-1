# CareFlow: Clinical Pathway Process Mining

## Project Overview
CareFlow is an internship project focused on analysing hospital clinical pathways using Process Mining and Bottleneck Analysis.

## Objectives
- Analyse hospital event-log data.
- Discover clinical process flows using PM4Py.
- Calculate average activity duration.
- Analyse time intervals between consecutive events.
- Visualise results using charts.
- Identify potential bottlenecks for further investigation.

## Dataset
The dataset contains:
- Case_ID
- Activity_Name
- Timestamp

The project uses cleaned hospital event-log data for analysis.

## Technologies Used
- Python
- Pandas
- PM4Py
- Matplotlib
- Git and GitHub

## Work Completed
- Checked the dataset structure and missing values.
- Analysed activity frequencies.
- Discovered a process model using PM4Py.
- Calculated activity-duration estimates and time intervals.
- Created visualisations for analysis.

## Project Structure
- Data: Dataset files, analysis results, and charts.
- scripts: Python scripts for data checking, process mining, and analysis.
- main.py: Main project file.
## Process Tree Visualisation
- Discovered a process tree using PM4Py.
- Generated and saved the process tree diagram as `Data/process_tree.png`.
- The diagram helps visualise the clinical process model discovered from the available event log.

## Activity Sequence Analysis
- Analysed consecutive hospital activities for each case.
- Counted the frequency of transitions between activities.
- Saved the results in `Data/activity_sequence_summary.csv`.

## Analysis Notes
- The analysis is based on the available hospital event-log dataset.
- Time differences between consecutive events are estimates of intervals, not confirmed waiting times or activity durations.
- Potential bottlenecks require further investigation and validation.
Process Mining Analysis

- Converted the hospital dataset into an event log using PM4Py.
- Discovered a process tree using the Inductive Miner algorithm.
- Generated and visualised a Petri Net model.
- Performed Token-Based Replay for conformance checking.
- Discovered a Directly-Follows Graph (DFG) to identify activity transitions.
- Analysed process model fitness and precision.

Petri Net Discovery

- Discovered a Petri Net model from the hospital event log.
- Identified places, transitions, and arcs.
- Saved the Petri Net visualisation as "Data/petri_net_model.png".

Conformance Checking

- Performed Token-Based Replay using PM4Py.
- Evaluated trace fitness, missing tokens, and remaining tokens.
- Saved the results in "Data/conformance_results.csv".

Directly-Follows Graph Analysis

- Identified directly-following activity relationships.
- Calculated transition frequencies.
- Generated a DFG visualisation as "Data/directly_follows_graph.png".
- Saved transition details in "Data/directly_follows_graph.csv".

Performance DFG Analysis

- Calculated average, maximum, and minimum time intervals between consecutive activities.
- Analysed transition frequencies.
- Generated a performance chart.
- Saved results in "Data/performance_dfg_analysis.csv".

Process Model Evaluation

- Evaluated the discovered Petri Net using token-based fitness and precision metrics.
- Saved evaluation results in "Data/process_model_evaluation.csv".
Advanced Data Analysis

- Clinical Performance Analysis
- Clinical Transition Analysis
- Workflow Variant Analysis
- Clinical Compliance Comparison
- Clinical Activity Frequency Analysis
- Case Performance Summary
- Activity Sequence Analysis

Generated CSV reports and charts to support the analysis.
Project Limitations

- The analysis is based on the available hospital event-log dataset.
- Actual activity duration cannot be confirmed without activity start-time and end-time information.
- Time differences between consecutive events represent observed event intervals, not confirmed patient waiting times.
- Process model conformance results reflect the discovered model and available event log; they do not establish clinical compliance or treatment correctness.
- Potential bottlenecks require further investigation and validation.