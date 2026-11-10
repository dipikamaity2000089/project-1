-- dbt model: models/marts/conformance.sql  (flags rework loops back to Triage, per patient)
with seq as (
  select case_id, doctor_id, age_group, triage_level, activity_name,
         lag(activity_name) over (partition by case_id order by activity_start) as prev_activity
  from {{ ref('stg_event_log') }}
)
select case_id,
       any_value(doctor_id)    as doctor_id,
       any_value(age_group)    as age_group,
       any_value(triage_level) as triage_level,
       countif(activity_name = 'Triage' and prev_activity = 'Doctor Consultation') > 0 as looped_back_to_triage
from seq
group by case_id
