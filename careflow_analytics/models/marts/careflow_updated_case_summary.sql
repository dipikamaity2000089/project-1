
SELECT
    case_id,
    COUNT(*) AS total_activities,
    MIN(event_timestamp) AS case_start_time,
    MAX(event_timestamp) AS case_end_time,
    TIMESTAMP_DIFF(
        MAX(event_timestamp),
        MIN(event_timestamp),
        MINUTE
    ) AS case_duration_minutes,
    COUNT(DISTINCT activity) AS unique_activities,
    MIN(activity_start_time) AS first_activity_start_time,
    MAX(activity_end_time) AS last_activity_end_time
FROM {{ ref('stg_updated_hospital_events') }}
GROUP BY case_id
