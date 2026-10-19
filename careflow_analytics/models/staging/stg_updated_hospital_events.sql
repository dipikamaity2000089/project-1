SELECT
    TRIM(CAST(Case_ID AS STRING)) AS case_id,
    TRIM(CAST(Activity_Name AS STRING)) AS activity,
    SAFE_CAST(Timestamp AS TIMESTAMP) AS event_timestamp,
    SAFE_CAST(Activity_Start_Time AS TIMESTAMP) AS activity_start_time,
    SAFE_CAST(Activity_End_Time AS TIMESTAMP) AS activity_end_time
FROM {{ source('careflow_updated', 'raw_updated_hospital_events') }}
WHERE
    Case_ID IS NOT NULL
    AND TRIM(CAST(Case_ID AS STRING)) != ''
    AND Activity_Name IS NOT NULL
    AND TRIM(CAST(Activity_Name AS STRING)) != ''