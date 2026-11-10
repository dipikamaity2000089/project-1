# CareFlow: Power BI Build Guide

## 1. Load the data
Home > Get Data > Text/CSV (or the Google BigQuery connector). Import these 5 tables:

| Table | Source | Use |
|---|---|---|
| event_log | event_log.csv | Raw events (feeds the process visual) |
| transitions | output/transition_bottlenecks.csv | Wait times between steps |
| activities | output/activity_stats.csv | Service time per activity |
| conformance | output/conformance.csv | One row per patient |
| kpis | output/kpis.csv | Headline numbers |

In Power Query, set `Timestamp`, `Activity_Start_Time`, `Activity_End_Time` to Date/Time, and `compliant` to True/False.

**Relationship:** `event_log[Case_ID]` → `conformance[case]` (many-to-one, single direction). Leave the other tables unrelated.

## 2. DAX measures (Modeling > New measure)
```DAX
Total Patients   = DISTINCTCOUNT(event_log[Case_ID])
Avg Stay (min)   = AVERAGE(conformance[total_los_min])
Loop-back %      = DIVIDE(COUNTROWS(FILTER(conformance, CONTAINSSTRING(conformance[issues],"Rework"))), COUNTROWS(conformance))
Conformance %    = DIVIDE(COUNTROWS(FILTER(conformance, conformance[compliant]=TRUE())), COUNTROWS(conformance))
Avg Wait (min)   = AVERAGE(transitions[avg_wait_min])
Worst Handoff    = MAXX(TOPN(1, transitions, transitions[avg_wait_min], DESC), transitions[from] & " → " & transitions[to])
Avg Service Time = AVERAGE(activities[avg_service_min])
```
Add a calculated column on `transitions`: `Transition = [from] & " → " & [to]`, and `Hot = IF([avg_wait_min]>=20,"Bottleneck","Normal")`.

## 3. Page 1: Overview
- **Top row, 4 Card visuals:** Total Patients, Avg Stay (min), Loop-back %, Conformance %.
- **Left (large): Process Mining visual.** Visualizations pane > Get more visuals > search "Power Automate Process Mining" > add it. Fields: Case ID = `event_log[Case_ID]`, Activity = `event_log[Activity_Name]`, Timestamp = `event_log[Activity_Start_Time]`. The visual will draw the process map directly from the event log.
- **Right: Clustered bar chart.** Axis = `transitions[Transition]`, Values = `avg_wait_min`. Conditional formatting > Bar colour > Rules: `avg_wait_min >= 20` = red.
- **Bottom: Table.** Case, path, total_los_min, compliant, with a slicer on `compliant`.

## 4. Page 2: Bottlenecks and conformance (Week 4 polish)
- Matrix: rows = `transitions[from]`, columns = `transitions[to]`, values = `avg_wait_min`, with a colour-scale background.
- Column chart: `activities[Activity_Name]` vs `avg_service_min`.
- Donut: conformant vs non-compliant patients.
- Slicers: `conformance[compliant]`, `event_log[Activity_Name]`.
- Right-click any visual > Drill through, so users can jump to a single patient's path.

## 5. Finishing
- Theme: View > Themes. Title: "CareFlow: ER Pathway Analysis".
- Add a text box under the map: "30% of patients are sent back to Triage after consultation."
- Save as `CareFlow.pbix` and add a screenshot to your GitHub README.

Note: the Power Automate Process Mining visual may need a Power BI Pro licence or a work/school account. If you can't use it, import `process_map.png` as an image and keep the rest of the page.

## 6. Large dataset update (500 patients): doctor, age and triage slicers
- Import `data/careflow_event_log_large.csv` as `event_log` (it now has `Doctor_ID`, `Age_Group`, `Triage_Level`) and `output/segment_breakdown.csv` as `segments`.
- `output/conformance.csv` now also has `Doctor_ID`, `Age_Group`, `Triage_Level` and `looped_back` (True/False). Keep the relationship `event_log[Case_ID]` → `conformance[case]`.
- Add three slicers on Page 1 and Page 2: `conformance[Doctor_ID]`, `conformance[Age_Group]`, `conformance[Triage_Level]`. Because they filter `conformance`, which filters `event_log`, the cards and the process map both react.
- New measure: `Loop-back % by selection = DIVIDE(COUNTROWS(FILTER(conformance, conformance[looped_back]=TRUE())), COUNTROWS(conformance))`. Put `Doctor_ID` on a bar chart axis with this measure to show that D04 is the outlier.
- Expected card values with no filter applied: 500 patients, about 199 min average stay, 39.6% looping back, 60.4% following the ideal path.
