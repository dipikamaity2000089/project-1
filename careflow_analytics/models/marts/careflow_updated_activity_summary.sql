
SELECT
    activity,
    COUNT(*) AS total_occurrences,
    COUNT(DISTINCT case_id) AS distinct_cases,
    MIN(event_timestamp) AS first_event_timestamp,
    MAX(event_timestamp) AS last_event_timestamp,
    MIN(activity_start_time) AS first_activity_start_time,
    MAX(activity_end_time) AS last_activity_end_time
FROM {{ ref('stg_updated_hospital_events') }}
GROUP BY activity
