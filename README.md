# Data Warehousing & ETL Pipeline (ITD100)

This repository contains the ETL pipelines and Star Schema designs for the ITD100 final project.

## Project Structure
- `data/`: Contains raw and cleaned datasets.
- `scripts/`: Python scripts for data cleaning (`clean_cars.py`, `clean_dates.py`) and automated PDF report generation (`generate_report.py`).
- `sql/`: PostgreSQL scripts for creating the Star Schemas and loading data.
- `reports/`: Final Data Quality PDF reports for Fisheries, Cars, and Date Fruit datasets.

## How to Run
1. Ensure PostgreSQL is running.
2. Activate the virtual environment: `source .venv/bin/activate`
3. Run the Python cleaning scripts: `python3 scripts/clean_cars.py`
4. Run the SQL scripts in `psql`.
5. Generate the report: `python3 scripts/generate_report.py`