# DS 5111 / DS 2508 – UNIQUE_SYMS dbt Model Report

**Student:** Chelsey Blowe  
**UVA ID:** qck2qg  
**Date:** 2025-12-02

## (a) Data Collection and Table Locations

For this project, I collected stock “gainers” data from two different web sources (Yahoo Finance and Wall Street Journal). The raw data files were first saved locally as CSV files, then uploaded into Snowflake where they became tables.

All of the tables live in:

- **Database:** `DS2508`
- **Schema:** `QCK2QG`

Each CSV upload creates a timestamped table, e.g.:

- `YGAINERS_20251023_160116`
- `WSJGGAINERS_20251024_093108`
- `YGAINERS_20251027_093118`

I also created normalized tables:

- `DS2508.QCK2QG.YGAINERS_NORMALIZED`
- `DS2508.QCK2QG.WSJGAINERS_NORMALIZED`

In total, there are approximately **43** Snowflake tables for this dataset.

## (b) Simple ERD for the UNIQUE_SYMS Model

```text
DS2508.QCK2QG.YGAINERS_NORMALIZED      DS2508.QCK2QG.WSJGAINERS_NORMALIZED
                \                                   /
                 \                                 /
                  \                               /
                   \                             /
                    \                           /
                     v                         v
                 DS2508.QCK2QG.UNIQUE_SYMS

