    CASE
        WHEN trim(upper("ID Number")) ~ '^[0-9]{6,9}$' THEN 'National ID No'
        WHEN trim(upper("ID Number")) ~ '^[0-9]{9}$' THEN 'Maisha Card'
        ELSE NULL
    END AS inferred_document_type