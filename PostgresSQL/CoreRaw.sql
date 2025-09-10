WITH CORE AS (
    SELECT
    CAST("Timestamp" AS DATE) AS timestamp,
    INITCAP(CONCAT_WS(' ', "First Name", "Last Name")) AS display_name,
    "Status",
    "Gender",
    LOWER(TRIM(REGEXP_REPLACE("Email Address", '\s+', '', 'g'))) AS email,
    CASE
        WHEN LENGTH(REGEXP_REPLACE(TRIM(SPLIT_PART("Mobile no", '/', 1)), '\D', '', 'g')) = 8
            THEN CONCAT(
                '254',
                REGEXP_REPLACE(TRIM(SPLIT_PART("Mobile no", '/', 1)), '\D', '', 'g')
            )
        ELSE
            REGEXP_REPLACE(TRIM(SPLIT_PART("Mobile no", '/', 1)), '\D', '', 'g')
    END AS mobile_no,
    CAST("Date of Birth" AS DATE) AS date_of_birth,
    "Photo of the Front Officer",
    "Front ID Picture",
	"ID Number",
    CASE
        WHEN trim(upper("ID Number")) ~ '^[0-9]{6,9}$' THEN 'National ID No'
        WHEN trim(upper("ID Number")) ~ '^[0-9]{9}$' THEN 'Maisha Card'
        ELSE NULL
    END AS inferred_document_type
	
FROM
    foobs_data_ke_001
WHERE 1 = 1
)

,CORE_PARTITION AS (
SELECT *,
ROW_NUMBER() OVER( PARTITION BY email ORDER BY COALESCE(timestamp, '1738-01-01') DESC) AS rowNum
FROM CORE
WHERE 1 = 1
)

,CORE_CLEAN AS (
SELECT * FROM CORE_PARTITION
WHERE 1 = 1
AND LOWER("Status") = 'account created'
AND rowNum = 1
)

,CORE_CHECKSUM AS (
SELECT *,
    'Gender : ' || 
        CASE WHEN "Gender" IS NULL THEN '❌' ELSE '✅' END AS gender_check,

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
            WHEN LENGTH("mobile_no") > 11 THEN '❌ More Digits'
            WHEN LENGTH("mobile_no") < 8 THEN '❌ Less Digits'
            ELSE '✅'
        END AS mobile_check,

    'Display_Name : ' ||
        CASE 
            WHEN display_name ILIKE '%Missing%' THEN '❌'
            WHEN display_name ~ '[^A-Za-z\s]' THEN '❌'
            ELSE '✅'
        END AS display_name_check		

FROM CORE_CLEAN
WHERE 1 = 1
)

SELECT 
    *,
    CASE 
        WHEN CONCAT( mobile_check, dob_check, document_type_check) ILIKE '%❌%' 
            THEN 'Incorrect Data' 
        ELSE NULL
    END AS errorStatus
FROM CORE_CHECKSUM
WHERE 1 = 1