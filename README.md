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