# Data Quality Report — Student Stress Dataset ETL

**Author:** Mai Kie
**Date:** 2026-11-07
**Source:** `StressLevelDataset.csv` 
**Target:** `dw_stress1.fact_student_stress`

## 1. Star Schema Diagram

```text
                    +----------------------+
                    |  dim_stress_level    |
                    |----------------------|
                    | level_key (PK)       |
                    | level_name           |
                    | (Low/Mod/High)       |
                    +----------+-----------+
                               |
                               | 1 : N
                               |
                  +------------v-------------+
                  |   fact_student_stress    |
                  |--------------------------|
                  | student_id (PK)          |
                  | level_key (FK)           |
                  | anxiety_level            |
                  | self_esteem              |
                  | depression               |
                  | headache                 |
                  | sleep_quality            |
                  | study_load               |
                  | social_support           |
                  | peer_pressure            |
                  | bullying                 |
                  +--------------------------+
Grain of fact_student_stress: one row per student survey response.

2. Issues Found in Source
#	Issue	Details
1	No Missing Values	The dataset is surprisingly clean and fully populated.
2	Categorical Target	The stress_level column is numeric (0, 1, 2) but represents a category.
3	Wide Table	21 columns total, requiring separation into dimensions and facts.
3. Rules Applied
Schema Design: Extracted the stress_level into a dedicated dim_stress_level table to allow for readable labels (Low, Moderate, High) instead of just numbers.

Fact Table Loading: Kept all the survey scores as numeric facts in fact_student_stress for easy aggregation (e.g., AVG(anxiety_level)).

Data Types: All scores were loaded as INT since they represent a 1-5 Likert scale or binary 0/1 responses.

4. Rows Loaded
Metric	Count
Total Rows in CSV	1100
Rows Rejected	0
Rows loaded into fact_student_stress	1100