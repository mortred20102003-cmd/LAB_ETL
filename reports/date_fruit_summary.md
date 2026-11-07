# Data Quality Report — Date Fruit Dataset ETL

**Author:** Mai Kie
**Date:** 2026-11-03
**Source:** `Date_Fruit_Datasets.xlsx` (898 rows)
**Target:** `dw.fact_date_fruit`

## 1. Star Schema Diagram

```text
                    +------------------+
                    |    dim_class     |
                    |------------------|
                    | class_key  (PK)  |
                    | class_name       |
                    +--------+---------+
                             |
                             | 1 : N
                             |
+------------------+      +--v---------------+
|   (No other      |      | fact_date_fruit  |
|   dimensions in  |      |------------------|
|   this design)   |<-----+ fruit_key  (PK)  |
|                  |      | class_key  (FK)  |
+------------------+      | area             |
                          | perimeter        |
                          | major_axis       |
                          | eccentricity     |
                          | meanrr / meanrg  |
                          | stddevrr / etc.  |
                          +------------------+

                          Grain of fact_date_fruit: one row per extracted image feature of a single date fruit.

2. Issues Found in Source
#	Issue	Details
1	File Format	Data was provided as an Excel file (.xlsx) rather than a CSV.
2	Formatting	Column names contained mixed casing (e.g., AREA, MeanRR, Class).
3	Wide Dataset	Dataset contained 34 columns, requiring careful mapping to the Fact table.
3. Rules Applied
Targeted Sheet: Used Pandas to read only the Date_Fruit_Datasets sheet from the Excel workbook.

Standardization: Converted all column names to lowercase for consistency.

Null Guard: Dropped any rows with missing values.

Export: Converted the Excel file to .csv for faster loading into PostgreSQL.

Upsert: Used ON CONFLICT (class_name) DO NOTHING when loading dim_class.

4. Rows Rejected
Reason	Count
Missing data	0
Total rejected	0
Rows loaded into fact_date_fruit	898