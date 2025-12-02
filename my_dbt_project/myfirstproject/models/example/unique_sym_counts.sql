{{ config(materialized='table') }}

SELECT
    SYMBOL,
    COUNT(*) AS symbol_count
FROM (
    SELECT SYMBOL FROM {{ ref('ygainers_normalized') }}
    UNION ALL
    SELECT SYMBOL FROM {{ ref('wsjgainers_normalized') }}
)
WHERE SYMBOL IS NOT NULL
GROUP BY SYMBOL
ORDER BY symbol_count DESC
