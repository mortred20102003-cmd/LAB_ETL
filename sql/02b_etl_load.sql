-- =========================================================
-- LAB 2-3 (Part B): Cleaning ETL into dw.fact_landing
-- =========================================================
INSERT INTO dw.fact_landing
  (date_key, port_key, species_key, vessel_key, trip_id, weight_kg, value_php)
WITH cleaned AS (
  SELECT
    r.*,
      ROW_NUMBER() OVER (
      PARTITION BY r.landing_date, r.port_name, r.species_name,
                   r.vessel_name, r.cooperative, r.weight_kg, r.value_php
      ORDER BY r.ctid
    ) AS rn
  FROM stg.raw_landings r
  WHERE r.landing_date IS NOT NULL AND trim(r.landing_date) <> ''
    AND r.weight_kg    IS NOT NULL AND trim(r.weight_kg)    <> ''
)
SELECT
  d.date_key,
  p.port_key,
  s.species_key,
  v.vessel_key,
  c.trip_id,
  c.weight_kg::numeric,
  c.value_php::numeric
FROM cleaned c
JOIN stg.species_mapping m ON m.messy_name = lower(trim(c.species_name))
JOIN dw.dim_date    d ON d.full_date     = c.landing_date::date
JOIN dw.dim_port    p ON p.port_name     = c.port_name
JOIN dw.dim_species s ON s.species_code  = m.species_code
JOIN dw.dim_vessel  v ON v.vessel_name   = c.vessel_name
                     AND c.landing_date::date BETWEEN v.valid_from AND v.valid_to
WHERE c.rn = 1
  AND c.weight_kg::numeric >  0
  AND c.weight_kg::numeric <= 10000
  AND c.value_php::numeric >= 0;

-- Verification
SELECT count(*) AS newly_loaded FROM dw.fact_landing WHERE trip_id LIKE 'T0%';