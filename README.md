CareFlow — Hospital Process Mining

Project Overview

CareFlow is a data-driven project focused on analyzing hospital workflows using event log data and process mining techniques. The project aims to understand patient journeys, identify workflow patterns, and explore potential bottlenecks to support improvements in hospital operational efficiency.

The project uses Python-based data processing and analysis to transform synthetic hospital event logs into structured information that can support further process analysis and visualization.

Objectives

- Generate and organize synthetic hospital event data.
- Clean and validate event logs to improve data quality.
- Prepare structured datasets for process analysis.
- Summarize patient journeys and activity durations.
- Analyze transitions between consecutive hospital activities.
- Explore workflow patterns and potential bottlenecks.
- Prepare analysis results for future visualization and dashboard development.

Dataset

The project currently uses synthetic hospital event data representing patient journeys through different hospital activities.

The generated dataset contains 10 synthetic patient cases. The number of events may change when the dataset is regenerated.

Dataset Fields

Column| Description
"Case_ID"| Unique identifier for each patient journey
"Activity_Name"| Hospital activity performed
"Timestamp"| Timestamp associated with the activity
"Activity_Start_Time"| Start time of the activity
"Activity_End_Time"| End time of the activity

Hospital Activities

The dataset includes the following activities:

- Registration
- Triage
- Doctor Consultation
- Lab Test
- X-Ray
- Treatment
- Discharge

Some patient journeys may include repeated activities to represent variations in the workflow.

Work Completed

1. Synthetic Data Generation

- Developed a Python script to generate synthetic hospital event logs.
- Generated patient activity records with timestamps and activity durations.
- Included variations in patient activity sequences.
- Saved the generated data in "data/hospital_events.csv".

2. Data Cleaning

- Developed a Python script to prepare event data for analysis.
- Processed timestamp fields and organized event records.
- Handled missing values and duplicate records according to the cleaning logic.
- Saved the cleaned dataset in "data/cleaned_hospital_events.csv".

3. Data Validation

- Developed a validation script to check the quality and consistency of the event data.
- Checked required columns, missing values, duplicate records, timestamp validity, and activity durations.
- Used validation results to identify potential data quality issues.

4. Data Quality Reporting

- Created a Python script to summarize important dataset statistics.
- Reported event counts, unique patient cases, activity counts, missing values, duplicates, and invalid durations.
- Saved the report in "data/data_quality_report.txt".

5. Patient-Level Summary

- Developed a script to summarize activity records for each patient case.
- Calculated activity counts and patient journey time information.
- Exported the results to "data/patient_summary.csv".

6. Activity Statistics

- Developed a script to analyze the frequency and duration of hospital activities.
- Calculated activity counts and average, minimum, and maximum durations.
- Exported the results to "data/activity_statistics.csv".

7. Process Analysis

- Developed "scripts/process_mining.py" to analyze transitions between consecutive hospital activities.
- Counted the number of events, patient cases, and unique activities.
- Summarized the number of activities recorded for each patient.
- Identified consecutive activity transitions within individual patient journeys.
- Calculated the frequency of each transition.
- Exported the transition results to "data/process_mining_transitions.csv".

Current Analysis Results

The current process analysis processed the cleaned synthetic dataset and reported:

- Total events: 63
- Patient cases: 10
- Unique activity types: 7

The transition analysis identifies how frequently one activity follows another across the recorded patient journeys. These results provide a foundation for exploring workflow patterns and preparing future visualizations.

These results describe the current generated dataset and may change if the data is regenerated or cleaned differently.

Technology Stack

- Programming Language: Python
- Data Processing: Pandas
- Data Storage: CSV and TXT files
- Development Environment: Visual Studio Code
- Version Control: Git and GitHub

Project Structure

project-1/
├── data/
│   ├── hospital_events.csv
│   ├── cleaned_hospital_events.csv
│   ├── data_quality_report.txt
│   ├── patient_summary.csv
│   ├── activity_statistics.csv
│   └── process_mining_transitions.csv
├── scripts/
│   ├── generate_events.py
│   ├── clean_events.py
│   ├── validate_events.py
│   ├── data_quality_report.py
│   ├── patient_summary.py
│   ├── activity_statistics.py
│   └── process_mining.py
└── README.md

Current Status

The project currently includes synthetic event data generation, data cleaning, data validation, data quality reporting, patient-level summaries, activity statistics, and activity transition analysis.

The generated outputs provide a structured foundation for further workflow analysis. More advanced process discovery, bottleneck analysis, and dashboard development remain potential next steps.

Expected Outcome

The project aims to transform hospital event logs into meaningful process insights that help reveal workflow patterns, activity sequences, delays, and opportunities for operational improvement.

