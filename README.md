CareFlow — Hospital Process Mining

Project Overview

CareFlow is a data-driven project focused on analyzing hospital workflows using event log data and process mining techniques. The project aims to understand patient journeys, identify workflow patterns, analyze activity durations, and explore potential bottlenecks to support improvements in hospital operational efficiency.

The project uses Python-based data processing, analysis, and visualization to transform synthetic hospital event logs into meaningful insights.

Objectives

- Generate and organize synthetic hospital event data.
- Clean and validate event logs.
- Perform exploratory data analysis.
- Summarize patient journeys and activity durations.
- Analyze transitions between consecutive hospital activities.
- Visualize hospital workflows and patient activity patterns.
- Develop dashboard-based representations of key performance indicators.
- Explore potential workflow improvements.

Dataset

The project uses synthetic hospital event data representing patient journeys through different hospital activities.

The current dataset contains 10 synthetic patient cases and 63 events. These values may change when the dataset is regenerated.

Dataset Fields

Column| Description
"Case_ID"| Unique identifier for each patient journey
"Activity_Name"| Hospital activity performed
"Timestamp"| Timestamp associated with the activity
"Activity_Start_Time"| Start time of the activity
"Activity_End_Time"| End time of the activity

Hospital Activities

- Registration
- Triage
- Doctor Consultation
- Lab Test
- X-Ray
- Treatment
- Discharge

Some patient journeys may include repeated activities to represent variations in workflow.

Work Completed

1. Synthetic Data Generation

- Developed a Python script to generate synthetic hospital event logs.
- Generated patient activity records with timestamps.
- Included variations in patient activity sequences.
- Saved the generated dataset in "data/hospital_events.csv".

2. Data Cleaning

- Developed a script to prepare event data for analysis.
- Processed timestamp fields and organized event records.
- Handled missing values and duplicate records according to the cleaning logic.
- Saved the cleaned dataset in "data/cleaned_hospital_events.csv".

3. Data Validation

- Developed a validation script to check data quality and consistency.
- Checked required columns, missing values, duplicate records, and timestamp validity.
- Validated event records before further analysis.

4. Data Quality Reporting

- Created a report containing important dataset statistics.
- Reported event counts, unique patient cases, activity counts, missing values, duplicates, and invalid durations.
- Saved the report in "data/data_quality_report.txt".

5. Patient-Level Summary

- Analyzed activity records for individual patient cases.
- Calculated activity counts and patient journey information.
- Exported results to "data/patient_summary.csv".

6. Activity Statistics

- Analyzed the frequency and duration of hospital activities.
- Calculated activity counts and average, minimum, and maximum durations.
- Exported results to "data/activity_statistics.csv".

7. Process Transition Analysis

- Developed "scripts/process_mining.py" to analyze transitions between consecutive hospital activities.
- Identified activity sequences within individual patient journeys.
- Calculated how frequently one activity follows another.
- Exported transition results to "data/process_mining_transitions.csv".

8. Hospital Workflow Visualization

- Created visual representations of hospital activity patterns.
- Developed a workflow visualization to understand activity sequences.
- Saved the workflow visualization in "data/hospital_workflow.png".

9. Patient Journey Analysis

- Analyzed individual patient activity sequences.
- Examined patient journey durations and activity patterns.
- Generated patient journey analysis results.
- Created patient journey visualizations.
- Developed a comparison analysis to compare patient journeys.

10. Activity Duration Analysis

- Analyzed the duration of hospital activities.
- Created visualizations to represent activity duration patterns.
- Used duration information to explore possible delays in the workflow.

11. Interactive Dashboard

- Developed a dashboard to present important project metrics and analysis results.
- Included key performance indicators such as patient count and event count.
- Added activity statistics, duration analysis, and patient journey information.
- Incorporated workflow and transition visualizations to support easier interpretation of results.

Current Analysis Results

The current generated dataset contains:

- Total Events: 63
- Patient Cases: 10
- Unique Activity Types: 7

The analysis provides information about patient activity sequences, transition frequencies, and activity durations. These results support further exploration of hospital workflow patterns.

These figures describe the current synthetic dataset and may change when the data is regenerated or processed differently.

Technology Stack

Technology| Purpose
Python| Programming and analysis
Pandas| Data cleaning and processing
Matplotlib / Plotly| Data visualization
CSV / TXT| Data storage and reports
Streamlit| Interactive dashboard
Visual Studio Code| Development environment
Git and GitHub| Version control and collaboration

Project Structure

project-1/
│
├── data/
│   ├── hospital_events.csv
│   ├── cleaned_hospital_events.csv
│   ├── data_quality_report.txt
│   ├── patient_summary.csv
│   ├── activity_statistics.csv
│   ├── process_mining_transitions.csv
│   ├── patient_journey_analysis.csv
│   ├── hospital_workflow.png
│   ├── patient_journey_chart.png
│   └── activity_duration_chart.png
│
├── scripts/
│   ├── generate_events.py
│   ├── clean_events.py
│   ├── validate_events.py
│   ├── data_quality_report.py
│   ├── patient_summary.py
│   ├── activity_statistics.py
│   ├── process_mining.py
│   ├── visualize_workflow.py
│   ├── patient_journey.py
│   ├── patient_journey_chart.py
│   ├── activity_duration.py
│   └── patient_journey_comparison.py
│
├── app.py
└── README.md

Note: The structure above represents the project files developed so far. Update it if filenames or folders change.

Current Status

CareFlow has progressed from synthetic event data generation to data cleaning, validation, statistical analysis, process transition analysis, patient journey analysis, visualizations, and dashboard development.

The project provides a structured foundation for understanding hospital workflow patterns using synthetic event logs.

Future Scope

- Advanced process discovery using process mining tools.
- Conformance checking against expected hospital workflows.
- More detailed bottleneck and waiting-time analysis.
- Integration with cloud data platforms.
- Additional dashboard features and interactive comparisons.

Expected Outcome

The project aims to transform hospital event logs into meaningful process insights that help reveal workflow patterns, activity sequences, delays, and opportunities for operational improvement.
