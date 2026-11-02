# project-1
Infotact Internship Project
project 1 CAREFLOW 
CareFlow: Clinical Pathway Process Mining

Hospital dashboards usually report one number: the average wait time. That hides the real cause of delays, which is the path each patient actually takes through the hospital. CareFlow applies process mining to timestamped Electronic Health Record (EHR) event logs and reconstructs those paths, so administrators can see where patients get stuck instead of just how long they wait.

How it works

The pipeline ingests raw event logs (Case_ID, Activity_Name, Timestamp) into Google BigQuery and standardises them with dbt models. A Python engine built on PM4Py then discovers the “as-is” process map as a directly-follows graph and Petri net. SQL and Python logic calculates the average wait between every pair of steps (for example, Triage to Doctor Consultation), and conformance checking compares each patient’s journey against the mandated pathway: Registration → Triage → Doctor Consultation → Lab Test or X-Ray → Treatment → Discharge. The results feed a Power BI dashboard with a process-flow visual, operational KPIs, and drill-downs.

Results on the simulated dataset (10 patients, 63 events)

30% of patients were sent back from Doctor Consultation to Triage, a rework loop that no average-wait metric would reveal.
Only 70% of cases followed the ideal pathway.
The longest handoff delays, around 18 to 20 minutes on average, sat between Doctor Consultation and re-Triage, between Lab Test and Treatment, and between Treatment and Discharge.
Average length of stay was 182 minutes.

Tech stack: Python, PM4Py, pandas, Graphviz, Google BigQuery, dbt, SQL, Microsoft Power BI

Key takeaway: Event-log architecture, which treats data as chronological sequences of events instead of flat tables, exposes hidden operational friction and points to specific, fixable bottlenecks such as the intake rework loop.
