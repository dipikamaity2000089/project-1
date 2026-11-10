-- dbt model: models/marts/segment_breakdown.sql  (loop-back rate per doctor)
select doctor_id,
       count(*) as cases,
       round(100 * avg(cast(looped_back_to_triage as int64)), 1) as loop_back_pct
from {{ ref('conformance') }}
group by doctor_id
order by loop_back_pct desc
