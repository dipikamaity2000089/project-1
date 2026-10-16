
SELECT
    case_id,
    COUNT(*) AS total_activities,
    MIN(event_timestamp) AS process_start_time,
    MAX(event_timestamp) AS process_end_time,
    TIMESTAMP_DIFF(
        MAX(event_timestamp),
        MIN(event_timestamp),
        MINUTE
    ) AS process_duration_minutes,
    COUNT(DISTINCT activity) AS unique_activities,
    COUNT(DISTINCT department) AS departments_involved
FROM {{ ref('stg_careflow_events') }}
GROUP BY case_id
