-- dbt model: models/staging/stg_event_log.sql
-- Standardises raw EHR logs into the Event Log format (Case_ID, Activity_Name, Timestamp)
select
  upper(trim(Case_ID))                         as case_id,
  trim(Activity_Name)                          as activity_name,
  cast(Activity_Start_Time as timestamp)       as timestamp,
  cast(Activity_Start_Time as timestamp)       as activity_start,
  cast(Activity_End_Time   as timestamp)       as activity_end,
  row_number() over (partition by Case_ID order by Activity_Start_Time) as step_no
from {{ source('careflow_raw', 'ehr_events') }}
where Case_ID is not null
  and Activity_End_Time >= Activity_Start_Time
