# Data Quality Report — Cars Dataset ETL

**Author:** Mai Kie
**Date:** 2026-11-03
**Source:** `cars_data.csv` (1218 rows)
**Target:** `dw.fact_cars`

## 1. Star Schema Diagram

```text
                    +------------------+
                    |   dim_company    |
                    |------------------|
                    | company_key (PK) |
                    | company_name     |
                    +--------+---------+
                             |
                             | 1 : N
                             |
+------------------+      +--v---------------+
|   fact_cars      |      |     dim_car      |
|------------------|      |------------------|
| car_key     (FK) +----->| car_key     (PK) |
| horsepower       |      | car_name         |
| top_speed_kmh    |      | company_key (FK) |
| acceleration_sec |      | fuel_type        |
| price_usd        |      | seats            |
+------------------+      | engine           |
                          +------------------+

                          Grain of fact_cars: one row per specific car model/trim level.

2. Issues Found in Source CSV
#	Issue	Details
1	Unicode Encoding Error	File contained special characters (byte 0x96) that crashed standard UTF-8 reading.
2	Dirty Currency Values	Prices contained dollar signs and commas (e.g., "$1,100,000 ").
3	Price Ranges	Some prices were ranges instead of single numbers (e.g., "$12,000-$15,000").
4	Text in Numeric Fields	Horsepower, Speed, and Acceleration contained text suffixes (e.g., "963 hp", "340 km/h").
5	Double Decimals	Malformed numbers with multiple dots (e.g., "7.25.4").
6	Missing Data	1 row had missing critical information (Company or Price).
3. Rules Applied
Encoding Fix: Read the file using latin1 encoding in Python (pd.read_csv(..., encoding='latin1')).

Price Cleaning: Used Python Regex and SQL SPLIT_PART to remove $, ,, and split ranges at the hyphen - to keep only the first number.

Numeric Extraction: Used PostgreSQL REGEXP_REPLACE(column, '[^0-9.]', '', 'g') to strip all letters and symbols from Horsepower, Speed, and Acceleration.

Decimal Fix: Wrapped numeric extraction in SUBSTRING to prevent multiple decimals from breaking the NUMERIC cast.

Null Guard: Dropped rows where Company Names or Cars Prices were missing/empty.

Deduplication: Used ON CONFLICT (car_name) DO NOTHING when loading dim_car to prevent duplicates.

4. Rows Rejected
Reason	Count
Missing critical data (Price/Company)	1
Total rejected	1
Rows loaded into fact_cars	1217
5. Data Insights (Top 5 Most Expensive Brands)
Bugatti (Avg: ~$5.9M)

Aston Martin (Avg: ~$752K)

Lamborghini (Avg: ~$650K)