# Data Warehousing & ETL Pipeline (ITD100)

This repository contains the ETL pipelines, Star Schema designs, and automated PDF reporting scripts for the ITD100 final project. 

## Datasets Processed
1. **Fisheries Landings** (Mock messy CSV) - Lab 1-3
2. **Cars Dataset 2025** (Kaggle) 
3. **Date Fruit Dataset** (Kaggle)
4. **Student Stress Level** (Kaggle)
5. **Student Stress Survey** (Kaggle)

## Project Structure
- `data/`: Contains raw and cleaned datasets (CSV and Excel).
- `scripts/`: Python scripts for data cleaning and automated PDF report generation.
- `sql/`: PostgreSQL scripts for creating Star Schemas and loading data.
- `reports/`: Final Data Quality PDF reports and automated chart reports.

## How to Run (General Workflow)
1. Ensure PostgreSQL is running.
2. Activate the virtual environment: `source .venv/bin/activate`
3. Run the Python cleaning scripts (e.g., `python3 scripts/clean_cars.py`).
4. Run the SQL scripts in `psql` to create schemas and load data.
5. Generate the automated PDF report: `python3 scripts/generate_report.py`