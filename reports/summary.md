# Data Quality Report — Fisheries Landings ETL

**Author:** Mai Kie
**Date:** 2026-11-03
**Source:** `messy_landings_2026.csv` (20 rows)
**Target:** `dw.fact_landing`

## 1. Star Schema Diagram

```
                          +------------------+
                          |     dim_date     |
                          |------------------|
                          | date_key  (PK)   |
                          | full_date        |
                          | year / quarter   |
                          | month / day      |
                          | day_of_week      |
                          | is_weekend       |
                          +--------+---------+
                                   |
                                   | 1 : N
                                   |
+------------------+      +--------v---------+      +------------------+
|     dim_port     |      |   fact_landing   |      |   dim_species    |
|------------------|      |------------------|      |------------------|
| port_key  (PK)   +----->| landing_key (PK) |<-----+ species_key (PK) |
| port_name        |      | date_key    (FK) |      | species_code     |
+------------------+      | port_key    (FK) |      | species_name     |
                          | species_key (FK) |      | scientific_name  |
                          | vessel_key  (FK) |      +------------------+
                          | trip_id          |
                          | weight_kg        |
                          | value_php        |      +------------------+
                          +--------+---------+      |   dim_vessel     |
                                   ^                |------------------|
                                   |                | vessel_key  (PK) |
                                   +----------------+ vessel_name      |
                                                    | cooperative      |
                                                    | valid_from       |
                                                    | valid_to         |
                                                    | is_current       |
                                                    +------------------+
```

**Grain of `fact_landing`:** one row per landed trip.

## 2. Issues Found in Source CSV

| # | Issue | Row(s) |
|---|-------|--------|
| 1 | Missing `landing_date` | T007 |
| 2 | Missing `weight_kg` | T009 |
| 3 | Negative `weight_kg` / `value_php` | T010 |
| 4 | Extreme outlier `weight_kg = 99999` | T011 |
| 5 | Exact duplicate row | T006 (matches T005) |
| 6 | Inconsistent species naming (`YFT` vs `Yellowfin Tuna`, `SJK` vs `skipjack tuna`) | Multiple |

## 3. Rules Applied

- **Null-guard**: reject rows with blank `landing_date` or blank `weight_kg`.
- **Domain check**: reject `weight_kg <= 0`.
- **Outlier rule**: reject `weight_kg > 10000` kg (99999 kg is implausible for one trip).
- **Deduplication**: `ROW_NUMBER() OVER (PARTITION BY all business columns EXCEPT trip_id)` — keep `rn = 1`.
- **Standardization**: `LOWER(TRIM(species_name))` joined to `stg.species_mapping`.
- **SCD Type 2 lookup**: join `dim_vessel` on `landing_date BETWEEN valid_from AND valid_to`.

## 4. Rows Rejected

| Reason | Count |
|--------|-------|
| Missing date | 1 |
| Missing weight | 1 |
| Negative weight | 1 |
| Outlier (> 10000 kg) | 1 |
| Duplicate | 1 |
| **Total rejected** | **5** |
| **Rows loaded into `fact_landing`** | **15** |