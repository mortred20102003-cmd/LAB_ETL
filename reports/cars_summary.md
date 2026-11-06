# ETL Pipeline & Star Schema Report: Cars Dataset 2025

## Dataset Source
- **Name:** Cars Datasets 2025
- **Source:** Kaggle

## Data Cleaning Rules Applied
- **Encoding Fix:** Used `latin1` encoding in Pandas to fix the `UnicodeDecodeError`.
- **Price Extraction:** Used Python and advanced PostgreSQL Regex (`REGEXP_REPLACE` and `SPLIT_PART`) to remove dollar signs, commas, and ranges (e.g., "`$12,000-$15,000`" was successfully converted to `12000`).
- **Horsepower Extraction:** Stripped "hp" from strings to convert them to pure `NUMERIC` types.
- **Missing Data:** Dropped rows where Company Names or Car Prices were null.

## Star Schema Integration
- **Dimensions:**
  - `dim_company` (Company Key, Company Name)
  - `dim_car` (Car Key, Car Name, Fuel Type, Seats, Engine)
- **Fact Table:**
  - `fact_cars` (Foreign Keys, Horsepower, Top Speed, Acceleration, Price)
- **Loading Strategy:** Dynamically loaded dimensions using `ON CONFLICT DO NOTHING` to handle new cars safely, then populated the Fact table by joining on the surrogate keys. 
- **Total Rows Loaded:** 1,217 cars successfully mapped into the Star Schema.

## Data Insights (Top 5 Most Expensive Brands)
- Bugatti (Avg: ~$5.9M)
- Aston Martin (Avg: ~$752K)
- Lamborghini (Avg: ~$650K)