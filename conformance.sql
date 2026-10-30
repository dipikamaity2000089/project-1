-- dbt model: models/marts/conformance.sql  (flags rework loops back to Triage)
with seq as (
  select case_id, activity_name,
         lag(activity_name) over (partition by case_id order by activity_start) as prev_activity
  from {{ ref('stg_event_log') }}
)
select case_id,
       countif(activity_name = 'Triage' and prev_activity = 'Doctor Consultation') > 0 as looped_back_to_triage
from seq
group by case_id
