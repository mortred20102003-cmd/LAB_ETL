SET search_path TO dw;

WITH Cleaned AS (
    SELECT r.*, 
           CASE 
               WHEN LOWER(r.species_name) LIKE '%yft%' OR LOWER(r.species_name) LIKE '%yellowfin%' THEN 'Yellowfin Tuna'
               WHEN LOWER(r.species_name) LIKE '%sjk%' OR LOWER(r.species_name) LIKE '%skipjack%' THEN 'Skipjack Tuna'
               WHEN LOWER(r.species_name) = 'barracuda' THEN 'Barracuda'
               WHEN LOWER(r.species_name) = 'groupers' THEN 'Groupers'
               WHEN LOWER(r.species_name) = 'reef fish' THEN 'Reef Fish'
               ELSE INITCAP(r.species_name)
           END AS clean_species,
           ROW_NUMBER() OVER(PARTITION BY landing_date, port_name, species_name, vessel_name, weight_kg, value_php ORDER BY trip_id) as rn
    FROM stg.landings_raw r
    WHERE r.weight_kg ~ '^[0-9]+(\.[0-9]+)?$' 
      AND r.weight_kg::NUMERIC > 0 AND r.weight_kg::NUMERIC < 5000
      AND r.landing_date IS NOT NULL AND r.landing_date <> ''
)
INSERT INTO dw.fact_landing (date_key, port_key, species_key, vessel_key, trip_id, weight_kg, value_php)
SELECT 
    TO_CHAR(c.landing_date::DATE, 'YYYYMMDD')::INT, 
    p.port_key, 
    s.species_key, 
    v.vessel_key, 
    c.trip_id, 
    c.weight_kg::NUMERIC, 
    c.value_php::NUMERIC
FROM Cleaned c
JOIN dw.dim_port p ON c.port_name = p.port_name
JOIN dw.dim_vessel v ON c.vessel_name = v.vessel_name AND v.is_current = TRUE
JOIN dw.dim_species s ON c.clean_species = s.species_name
WHERE c.rn = 1;