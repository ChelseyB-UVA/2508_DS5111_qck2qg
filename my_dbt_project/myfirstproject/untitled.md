# DS 5111 / DS 2508 – UNIQUE_SYMS dbt Model Report

**Student:** Chelsey Blowe 
**UVA ID:** qck2qg 
**Date:** 2025-12-02

## Data Collection and Table Locations

For this project, I collected stock “gainers” data from two different web sources (Yahoo Finance and Wall Street Journal). The raw data files were first saved locally as CSV files, and then uploaded / loaded into Snowflake, where they became tables.

All of the tables for this project live in the following location:

- **Database:** `DS2508`  
- **Schema:** `QCK2QG`  

In Snowflake, each daily CSV load creates a table whose name encodes the date and time, for example:

- `YGAINERS_20251023_160116`  
- `WSJGAINERS_20251024_093108`  
- `YGAINERS_20251027_093118`  
- …and many similar tables for other dates.

On top of these, I created **normalized tables** to clean and standardize the data:

- `DS2508.QCK2QG.YGAINERS_NORMALIZED`  
- `DS2508.QCK2QG.WSJGAINERS_NORMALIZED`

These are clean versions of the raw files.

In total, I have approximately **43** Snowflake tables related to gainers data (all the timestamped raw tables plus the two normalized tables). The dbt model `unique_syms` uses the two normalized tables as its inputs.

## Simple ERD for the UNIQUE_SYMS Model

The `unique_syms` model takes all symbols from both normalized source tables and produces one table of unique ticker symbols.

A simple ERD (many-to-one) view:

```text
DS2508.QCK2QG.YGAINERS_NORMALIZED      DS2508.QCK2QG.WSJGAINERS_NORMALIZED
                \                                   /
                 \                                 /
                  \                               /
                   \                             /
                    \                           /
                     v                         v
                      DS2508.QCK2QG.UNIQUE_SYMS


---

## Cell 4 — Markdown (this is where your broken bit was)

```markdown
## (c) GitHub Link and Model SQL

**GitHub link to the dbt model:**

`https://github.com/ChelseyB-UVA/2508_DS5111_qck2qg/blob/mo10_dbt_model/models/example/unique_syms.sql`

**SQL that generates the `UNIQUE_SYMS` table (`models/example/unique_syms.sql`):**

```sql
{{ config(materialized='table') }}

SELECT DISTINCT SYMBOL
FROM (
    SELECT SYMBOL FROM {{ ref('ygainers_normalized') }}
    UNION ALL
    SELECT SYMBOL FROM {{ ref('wsjgainers_normalized') }}
)
WHERE SYMBOL IS NOT NULL

---

## Cell 5 — Code cell (SQL, using ipython-sql)

Make this a **Code** cell in Jupyter, not Markdown:

```sql
%sql
SELECT * FROM DS2508.QCK2QG.UNIQUE_SYMS;

---

To download the CSV for part (e):

Use the Snowflake UI on the query above and choose:  
**Download Results → CSV**

Save the file as `UNIQUE_SYMS.csv` in the same directory as this notebook.

## (d) Full Path to the Result Table

The dbt model `unique_syms` materializes to this Snowflake table:

```text
DS2508.QCK2QG.UNIQUE_SYMS


---

## Cell 8 — Code cell (Part e: pandas)

Make this a **Code** cell:

```python
import pandas as pd

# Update this path if the CSV is in a different folder
csv_path = "UNIQUE_SYMS.csv"

df = pd.read_csv(csv_path)

print("Shape of UNIQUE_SYMS dataframe:", df.shape)
print("\nTop 10 symbols:")
df.head(10)
