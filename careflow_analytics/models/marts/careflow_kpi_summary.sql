
WITH case_metrics AS (

    SELECT
        case_id,
        total_activities,
        case_duration_minutes
    FROM {{ ref('careflow_updated_case_summary') }}

),

compliance_metrics AS (

    SELECT
        case_id,
        is_compliant
    FROM {{ ref('careflow_process_compliance') }}

),

combined_metrics AS (

    SELECT
        c.case_id,
        c.total_activities,
        c.case_duration_minutes,
        p.is_compliant
    FROM case_metrics c
    INNER JOIN compliance_metrics p
        ON c.case_id = p.case_id

)

SELECT
    COUNT(*) AS total_cases,

    SUM(total_activities) AS total_activities,

    COUNTIF(is_compliant = TRUE) AS compliant_cases,

    COUNTIF(is_compliant = FALSE) AS non_compliant_cases,

    ROUND(
        SAFE_DIVIDE(
            COUNTIF(is_compliant = TRUE) * 100.0,
            COUNT(*)
        ),
        2
    ) AS compliance_rate_percentage,

    ROUND(
        AVG(case_duration_minutes),
        2
    ) AS average_case_duration_minutes,

    ROUND(
        AVG(total_activities),
        2
    ) AS average_activities_per_case

FROM combined_metrics
