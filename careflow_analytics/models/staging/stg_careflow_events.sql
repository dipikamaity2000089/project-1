SELECT
    TRIM(case_id) AS case_id,
    TRIM(activity) AS activity,
    timestamp AS event_timestamp,
    TRIM(department) AS department
FROM {{ source('careflow', 'raw_event_log') }}
WHERE
    case_id IS NOT NULL
    AND TRIM(case_id) != ''
    AND activity IS NOT NULL
    AND TRIM(activity) != ''
