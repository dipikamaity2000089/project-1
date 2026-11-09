
WITH case_activity_summary AS (

    SELECT
        case_id,

        ARRAY_AGG(
            activity ORDER BY activity_start_time ASC
            LIMIT 1
        )[SAFE_OFFSET(0)] AS first_activity,

        ARRAY_AGG(
            activity ORDER BY activity_start_time DESC
            LIMIT 1
        )[SAFE_OFFSET(0)] AS last_activity,

        COUNTIF(activity = 'Triage') > 0 AS has_triage,

        COUNTIF(activity = 'Doctor Consultation') > 0
            AS has_doctor_consultation,

        COUNTIF(activity IN ('Lab Test', 'X-Ray')) > 0
            AS has_investigation,

        COUNTIF(activity = 'Treatment') > 0 AS has_treatment,

        MIN(
            IF(
                activity IN ('Lab Test', 'X-Ray'),
                activity_start_time,
                NULL
            )
        ) AS first_investigation_time,

        MIN(
            IF(
                activity = 'Treatment',
                activity_start_time,
                NULL
            )
        ) AS treatment_time

    FROM {{ ref('stg_updated_hospital_events') }}

    GROUP BY case_id
),

compliance_checks AS (

    SELECT
        case_id,

        first_activity = 'Registration'
            AS registration_first,

        has_triage,

        has_doctor_consultation,

        has_investigation,

        has_treatment,

        last_activity = 'Discharge'
            AS discharge_last,

        (
            first_investigation_time IS NOT NULL
            AND treatment_time IS NOT NULL
            AND first_investigation_time < treatment_time
        ) AS investigation_before_treatment

    FROM case_activity_summary
)

SELECT
    *,

    (
        registration_first
        AND has_triage
        AND has_doctor_consultation
        AND has_investigation
        AND has_treatment
        AND discharge_last
        AND investigation_before_treatment
    ) AS is_compliant

FROM compliance_checks
