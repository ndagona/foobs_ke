SELECT *,
--------------------------------------------------------------------
    'Gender : ' || 
        CASE WHEN gender IS NULL THEN '❌' ELSE '✅' END AS gender_check,

    'DOB : ' ||
        CASE 
            WHEN date_of_birth IS NULL THEN '❌ Missing DOB'
            WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)) < 18 THEN '❌ Too young'
            WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)) > 99 THEN '❌ Too old'
            ELSE '✅'
        END AS dob_check,

    'Document Type : ' ||
        CASE WHEN inferred_document_type IS NULL THEN '❌' ELSE '✅' END AS document_type_check,

    'Mobile Number : ' ||
        CASE 
            WHEN LENGTH(mobile_no) > 11 THEN '❌ More Digits'
            WHEN LENGTH(mobile_no) < 8 THEN '❌ Less Digits'
            ELSE '✅'
        END AS mobile_check,

    'Email : ' ||
        CASE 
            WHEN email IS NULL OR NOT (email ~* '^[A-Za-z0-9._%+-]{3,}@[A-Za-z0-9.-]{2,}\.[A-Za-z]{2,}$') THEN '❌'
            WHEN LOWER(SPLIT_PART(SPLIT_PART(TRIM(LOWER(REGEXP_REPLACE(email, '\s+', '', 'g'))), '@', 2), '.', 1)) 
                IN ('afroint','gmsil','africell','central','gmal','gmai','gamil','gmsil','null')
                THEN '⚠️ Possibly bad email'
            ELSE '✅'
        END AS email_check,

    'Display Name : ' ||
        CASE 
            WHEN display_name ILIKE '%Missing%' THEN '❌'
            WHEN display_name ~ '[^A-Za-z\s]' THEN '❌'
            ELSE '✅'
        END AS display_name_check

FROM core_clean
WHERE TRUE;