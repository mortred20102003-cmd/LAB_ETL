-- =========================================================
-- LAB 2-3 (Part A): Staging schema + species mapping
-- =========================================================
CREATE SCHEMA IF NOT EXISTS stg;

CREATE TABLE stg.raw_landings (
  trip_id      text,
  landing_date text,
  port_name    text,
  species_name text,
  vessel_name  text,
  cooperative  text,
  weight_kg    text,
  value_php    text
);

CREATE TABLE stg.species_mapping (
  messy_name   text PRIMARY KEY,
  species_code text NOT NULL REFERENCES dw.dim_species(species_code)
);

INSERT INTO stg.species_mapping (messy_name, species_code) VALUES
  ('yft',            'YFT'),
  ('yellowfin tuna', 'YFT'),
  ('sjk',            'SJK'),
  ('skipjack tuna',  'SJK');