{{ config(materialized='table') }}

SELECT DISTINCT SYMBOL
FROM (
    SELECT SYMBOL FROM {{ ref('ygainers_normalized') }}
    UNION ALL
    SELECT SYMBOL FROM {{ ref('wsjgainers_normalized') }}
)
WHERE SYMBOL IS NOT NULL
