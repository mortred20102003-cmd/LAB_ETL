-- =========================================================
-- LAB 1: Fisheries Star Schema
-- =========================================================
DROP SCHEMA IF EXISTS dw CASCADE;
CREATE SCHEMA dw;

-- ---------- Dimensions ----------
CREATE TABLE dw.dim_date (
  date_key    integer PRIMARY KEY,
  full_date   date NOT NULL UNIQUE,
  year        smallint NOT NULL,
  quarter     smallint NOT NULL,
  month       smallint NOT NULL,
  day         smallint NOT NULL,
  day_of_week smallint NOT NULL,
  is_weekend  boolean  NOT NULL
);

CREATE TABLE dw.dim_port (
  port_key  serial PRIMARY KEY,
  port_name text NOT NULL UNIQUE
);

CREATE TABLE dw.dim_species (
  species_key     serial PRIMARY KEY,
  species_code    text NOT NULL UNIQUE,
  species_name    text NOT NULL,
  scientific_name text
);

CREATE TABLE dw.dim_vessel (
  vessel_key  serial PRIMARY KEY,
  vessel_name text NOT NULL,
  cooperative text NOT NULL,
  valid_from  date    NOT NULL,
  valid_to    date    NOT NULL DEFAULT '9999-12-31',
  is_current  boolean NOT NULL DEFAULT TRUE
);

-- ---------- Fact ----------
CREATE TABLE dw.fact_landing (
  landing_key bigserial PRIMARY KEY,
  date_key    integer        NOT NULL REFERENCES dw.dim_date(date_key),
  port_key    integer        NOT NULL REFERENCES dw.dim_port(port_key),
  species_key integer        NOT NULL REFERENCES dw.dim_species(species_key),
  vessel_key  integer        NOT NULL REFERENCES dw.dim_vessel(vessel_key),
  trip_id     text,
  weight_kg   numeric(12,2)  NOT NULL CHECK (weight_kg > 0),
  value_php   numeric(14,2)  NOT NULL CHECK (value_php >= 0)
);

-- ---------- Populate dim_date (2020-01-01 → 2030-12-31) ----------
INSERT INTO dw.dim_date
SELECT
  to_char(d, 'YYYYMMDD')::int,
  d,
  EXTRACT(YEAR    FROM d)::smallint,
  EXTRACT(QUARTER FROM d)::smallint,
  EXTRACT(MONTH   FROM d)::smallint,
  EXTRACT(DAY     FROM d)::smallint,
  EXTRACT(ISODOW  FROM d)::smallint,
  EXTRACT(ISODOW  FROM d) IN (6,7)
FROM generate_series('2020-01-01'::date, '2030-12-31'::date, '1 day') AS d;

-- ---------- Sample dimensions ----------
INSERT INTO dw.dim_port (port_name) VALUES
  ('General Santos'), ('Davao'), ('Zamboanga'), ('Cebu');

INSERT INTO dw.dim_species (species_code, species_name, scientific_name) VALUES
  ('YFT', 'Yellowfin Tuna', 'Thunnus albacares'),
  ('SJK', 'Skipjack Tuna',  'Katsuwonus pelamis');

INSERT INTO dw.dim_vessel (vessel_name, cooperative, valid_from, valid_to, is_current) VALUES
  ('MB Sitti', 'GenSan Fishers Coop', '2020-01-01', '9999-12-31', TRUE),
  ('MB Lumba', 'Davao Tuna Coop',     '2020-01-01', '9999-12-31', TRUE);

-- ---------- 200 randomized fact rows (NO cartesian product) ----------
-- Each LATERAL returns EXACTLY one row → 200 fact rows guaranteed.
INSERT INTO dw.fact_landing (date_key, port_key, species_key, vessel_key,
                             trip_id, weight_kg, value_php)
SELECT
  d.date_key,
  p.port_key,
  s.species_key,
  v.vessel_key,
  'T' || lpad(g::text, 5, '0'),
  round((random()*1000 + 100)::numeric, 2),
  round((random()*200000 + 20000)::numeric, 2)
FROM generate_series(1,200) AS g
CROSS JOIN LATERAL (SELECT date_key FROM dw.dim_date
                    WHERE full_date BETWEEN '2026-01-01' AND '2026-12-31'
                    ORDER BY random() LIMIT 1) d
CROSS JOIN LATERAL (SELECT port_key    FROM dw.dim_port    ORDER BY random() LIMIT 1) p
CROSS JOIN LATERAL (SELECT species_key FROM dw.dim_species ORDER BY random() LIMIT 1) s
CROSS JOIN LATERAL (SELECT vessel_key  FROM dw.dim_vessel
                    WHERE is_current   ORDER BY random() LIMIT 1) v;

-- Verify exactly 200
SELECT count(*) AS fact_rows FROM dw.fact_landing;

-- ---------- SCD Type 2: MB Sitti changes cooperative ----------
-- Step 1: close the currently-active version
UPDATE dw.dim_vessel
SET    valid_to   = CURRENT_DATE - 1,
       is_current = FALSE
WHERE  vessel_name = 'MB Sitti'
  AND  is_current  = TRUE;

-- Step 2: insert the new version
INSERT INTO dw.dim_vessel (vessel_name, cooperative, valid_from, valid_to, is_current)
VALUES ('MB Sitti', 'Zamboanga Fleet', CURRENT_DATE, '9999-12-31', TRUE);

-- Inspect the SCD2 history
SELECT vessel_key, vessel_name, cooperative, valid_from, valid_to, is_current
FROM   dw.dim_vessel
ORDER  BY vessel_name, valid_from;