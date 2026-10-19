CareFlow — Hospital Process Mining

Project Overview

CareFlow is a data-driven project focused on analyzing hospital workflows using event log data and process mining techniques. The project aims to understand patient journeys, identify workflow bottlenecks, and support improvements in hospital operational efficiency.

Objectives

- Generate and organize synthetic hospital event data.
- Clean and validate event logs for reliable analysis.
- Prepare structured data for process mining.
- Analyze patient workflows and identify potential bottlenecks.
- Develop visualizations to communicate process insights.

Dataset

The current dataset contains synthetic hospital event data representing patient journeys through different hospital activities.

Dataset fields:

Column| Description
"Case_ID"| Unique identifier for each patient journey
"Activity_Name"| Hospital activity performed
"Timestamp"| Activity start timestamp
"Activity_Start_Time"| Start time of the activity
"Activity_End_Time"| End time of the activity

The generated dataset currently contains 10 patient cases. The event count may change when the dataset is regenerated.

Hospital Activities

The dataset represents activities such as:

- Registration
- Triage
- Doctor Consultation
- Lab Test
- X-Ray
- Treatment
- Discharge

Some patient journeys may include repeated activities to represent variations in the workflow.

Work Completed

- Created a Python script to generate synthetic hospital event logs.
- Generated patient activity records with timestamps and activity durations.
- Developed a data-cleaning script to prepare the event log.
- Created a validation script to check event data quality.
- Prepared a cleaned dataset for further analysis.
- Developed a data quality reporting script to summarize dataset statistics and potential data issues.

Technology Stack

- Programming Language: Python
- Data Processing: Pandas
- Data Storage: CSV
- Version Control: Git and GitHub

Additional analytics, process mining, data warehousing, and visualization tools may be incorporated as the project progresses.

Project Structure

project-1/
├── data/
│   ├── hospital_events.csv
│   ├── cleaned_hospital_events.csv
│   └── data_quality_report.txt
├── scripts/
│   ├── generate_events.py
│   ├── clean_events.py
│   ├── validate_events.py
│   └── data_quality_report.py
└── README.md

Current Status

The synthetic event data generation, cleaning, and initial validation workflow has been developed. A data quality report is being prepared to summarize the current dataset.

Process discovery, bottleneck analysis, and dashboard development remain subsequent project activities.

Expected Outcome

The project aims to transform hospital event logs into meaningful process insights that can help reveal workflow patterns, delays, and opportunities for operational improvement.

Disclaimer

This project currently uses synthetic data for educational and analytical purposes. It does not represent real patient records or provide clinical recommendations.

