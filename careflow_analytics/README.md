# CareFlow — Healthcare Process Analytics

## Project Overview

CareFlow is a healthcare process analytics project that uses hospital event data to analyse patient-care workflows. This dbt component transforms raw hospital events into structured staging data and analytical summaries for case-level and activity-level analysis.

## My Contribution — BigQuery & dbt

This component uses Google BigQuery as the data warehouse and dbt to transform, organise, and test hospital event data.

### Data Source

- **Google Cloud project:** `careflow-analytics-511805`
- **Raw dataset:** `careflow_raw`
- **Raw table:** `raw_updated_hospital_events`
- **Input records:** 63 events, covering 10 distinct cases and 7 distinct activities (verified during data validation).

The input dataset contains case IDs, activity names, event timestamps, activity start times, and activity end times.

### dbt Models

| Model | Purpose | Materialisation |
|---|---|---|
| `stg_updated_hospital_events` | Standardises column names, trims text values, converts timestamps, and filters invalid case IDs and activity names. | View |
| `careflow_updated_case_summary` | Summarises each case with activity counts, start/end timestamps, duration in minutes, unique activity count, and activity time boundaries. | Table |
| `careflow_updated_activity_summary` | Summarises each activity with occurrence counts, distinct case counts, and first/last event timestamps. | Table |

### Data Quality Tests

The models have configured dbt data quality tests, including:

- Not-null checks for required fields.
- Unique case IDs in the case summary.
- Unique activity names in the activity summary.

**Latest combined verification:** 3 models ran successfully and all 18 configured tests passed.

### How to Run

Run these commands from the `careflow_analytics` dbt project directory after configuring the BigQuery connection in `~/.dbt/profiles.yml`.

Run all three models:

```bash
dbt run --select stg_updated_hospital_events careflow_updated_case_summary careflow_updated_activity_summary
```

Run the configured tests:

```bash
dbt test --select stg_updated_hospital_events careflow_updated_case_summary careflow_updated_activity_summary
```

### Project Status

The updated staging model, case summary, and activity summary have been implemented and successfully tested. Documentation and final repository review are part of the remaining handoff work.

### Notes

This component performs data transformation and analytics. Its outputs support healthcare process analysis; they do not independently establish clinical correctness or make clinical decisions.