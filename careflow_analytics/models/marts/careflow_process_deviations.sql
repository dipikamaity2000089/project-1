
WITH compliance AS (

    SELECT
        case_id,
        registration_first,
        has_triage,
        has_doctor_consultation,
        has_investigation,
        has_treatment,
        discharge_last,
        investigation_before_treatment
    FROM {{ ref('careflow_process_compliance') }}

),

deviations AS (

    SELECT
        case_id,
        'REGISTRATION_NOT_FIRST' AS deviation_type,
        'Registration is missing or is not the first activity' AS deviation_description
    FROM compliance
    WHERE registration_first = FALSE

    UNION ALL

    SELECT
        case_id,
        'MISSING_TRIAGE',
        'Required Triage activity is missing'
    FROM compliance
    WHERE has_triage = FALSE

    UNION ALL

    SELECT
        case_id,
        'MISSING_DOCTOR_CONSULTATION',
        'Required Doctor Consultation activity is missing'
    FROM compliance
    WHERE has_doctor_consultation = FALSE

    UNION ALL

    SELECT
        case_id,
        'MISSING_INVESTIGATION',
        'Neither Lab Test nor X-Ray was recorded'
    FROM compliance
    WHERE has_investigation = FALSE

    UNION ALL

    SELECT
        case_id,
        'MISSING_TREATMENT',
        'Required Treatment activity is missing'
    FROM compliance
    WHERE has_treatment = FALSE

    UNION ALL

    SELECT
        case_id,
        'DISCHARGE_NOT_LAST',
        'Discharge is missing or is not the last activity'
    FROM compliance
    WHERE discharge_last = FALSE

    UNION ALL

    SELECT
        case_id,
        'INVESTIGATION_AFTER_TREATMENT',
        'Investigation was not recorded before Treatment'
    FROM compliance
    WHERE has_investigation = TRUE
      AND has_treatment = TRUE
      AND investigation_before_treatment = FALSE

)

SELECT *
FROM deviations
