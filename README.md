# CareFlow: Clinical Pathway Process Mining

Hospital dashboards report one number, the average wait time, which hides *why* patients wait. CareFlow applies process mining to timestamped EHR event logs to reconstruct the path each patient actually takes through the Emergency Room, so administrators can see where patients get stuck.

## Pipeline
Python generator → Google BigQuery → dbt (event-log normalisation) → PM4Py (process discovery) → SQL/Python bottleneck and conformance logic → Power BI dashboard.

## Results on the simulated dataset (500 patients, 3,198 events)
| Measure | Result |
|---|---|
| Patients sent back to Triage after the doctor | 39.6% (198 of 500) |
| Followed the ideal pathway | 60.4% |
| Average length of stay | 198.8 min (215.2 with a loop, 188.0 without) |
| Doctor with the highest loop-back rate | D04, 60.4% (other doctors 26% to 44%) |
| Longest average waits | Triage → Doctor 24.7 min, X-Ray → Treatment 23.2 min, Lab Test → Treatment 21.5 min |

The data is simulated. The rework loop, the D04 effect, the lunchtime rush and the slow diagnostic handoffs were planted on purpose to check that the method finds them. The 60+ age group also shows a higher loop-back rate (53%), but no age effect was planted, so treat that as chance.

## Project structure
```
data/        careflow_event_log_large.csv   500 simulated patients (Case_ID, Activity_Name, Timestamp, start/end, Doctor_ID, Age_Group, Triage_Level)
generator/   generate_event_log.py          Week 1: EHR simulation (python generator/generate_event_log.py 500 42)
sql/         stg_event_log.sql              Week 2: dbt event normalisation
             bottlenecks.sql                Week 3: average wait between every pair of steps
             conformance.sql                Week 4: flags the rework loop per patient
             segment_breakdown.sql          Loop-back rate per doctor
analysis/    careflow_analysis.py           Process discovery (PM4Py), bottlenecks, conformance, process map
output/      process_map.png, transition_bottlenecks.csv, activity_stats.csv, conformance.csv, segment_breakdown.csv, kpis.csv
dashboard/   careflow_dashboard.html       Interactive preview dashboard (open in a browser)
docs/        PowerBI_Build_Guide.md         Tables, DAX measures and page layout for the Power BI report
```

## How to run
```bash
pip install pandas pm4py graphviz        # also install the Graphviz program
python generator/generate_event_log.py 500 42                      # optional: regenerate the data
python analysis/careflow_analysis.py data/careflow_event_log_large.csv
```
Warehouse side: load `data/careflow_event_log_large.csv` into BigQuery as `careflow_raw.ehr_events`, point the dbt `source()` in `sql/stg_event_log.sql` at it, and run `dbt run`.

## Tech stack
Python, PM4Py, pandas, Graphviz, Google BigQuery, dbt, SQL, Power BI
