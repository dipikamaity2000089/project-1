WITH case_paths AS (

    SELECT
        case_id,

        STRING_AGG(
            activity,
            ' -> '
            ORDER BY activity_start_time ASC
        ) AS process_variant

    FROM {{ ref('stg_updated_hospital_events') }}

    GROUP BY case_id

),

variant_counts AS (

    SELECT
        process_variant,
        COUNT(*) AS case_count

    FROM case_paths

    GROUP BY process_variant

),

total_cases AS (

    SELECT COUNT(*) AS total_cases
    FROM case_paths

)

SELECT
    v.process_variant,
    v.case_count,
    t.total_cases,

    ROUND(
        SAFE_DIVIDE(v.case_count * 100.0, t.total_cases),
        2
    ) AS percentage_of_cases

FROM variant_counts v
CROSS JOIN total_cases t
ORDER BY v.case_count DESC