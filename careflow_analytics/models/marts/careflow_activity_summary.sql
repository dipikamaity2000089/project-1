
SELECT
    activity,
    COUNT(*) AS total_occurrences,
    COUNT(DISTINCT case_id) AS cases_involved,
    COUNT(DISTINCT department) AS departments_involved,
    MIN(event_timestamp) AS first_recorded_at,
    MAX(event_timestamp) AS last_recorded_at
FROM {{ ref('stg_careflow_events') }}
GROUP BY activity
