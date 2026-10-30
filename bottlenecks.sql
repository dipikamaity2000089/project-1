-- dbt model: models/marts/transition_bottlenecks.sql
with seq as (
  select case_id, activity_name, activity_start, activity_end,
         lead(activity_name)  over w as next_activity,
         lead(activity_start) over w as next_start
  from {{ ref('stg_event_log') }}
  window w as (partition by case_id order by activity_start)
)
select
  activity_name as from_activity,
  next_activity as to_activity,
  count(*)      as frequency,
  round(avg(timestamp_diff(next_start, activity_end, minute)), 1) as avg_wait_min,
  max(timestamp_diff(next_start, activity_end, minute))           as max_wait_min
from seq
where next_activity is not null
group by 1, 2
order by avg_wait_min desc
