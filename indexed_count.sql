SELECT indexed, count(1)
FROM (
    SELECT summary IS NOT NULL AND full_text IS NOT NULL AS indexed
    FROM articles
) GROUP BY indexed;