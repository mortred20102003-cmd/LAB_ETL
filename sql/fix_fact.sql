TRUNCATE dw.fact_cars;
TRUNCATE stg.cars_staging;

\copy stg.cars_staging FROM 'data/clean_cars_data.csv' WITH (FORMAT csv, HEADER true);

SET search_path TO dw;

INSERT INTO dw.fact_cars (car_key, horsepower, top_speed_kmh, acceleration_sec, price_usd)
SELECT 
    c.car_key,
    NULLIF(SUBSTRING(s.horsepower FROM '[0-9]+(\.[0-9]+)?'), '')::NUMERIC,
    NULLIF(SUBSTRING(s.total_speed FROM '[0-9]+(\.[0-9]+)?'), '')::NUMERIC,
    NULLIF(SUBSTRING(s.performance_0_100 FROM '[0-9]+(\.[0-9]+)?'), '')::NUMERIC,
    NULLIF(SUBSTRING(s.cars_prices FROM '[0-9]+(\.[0-9]+)?'), '')::NUMERIC
FROM stg.cars_staging s
JOIN dw.dim_car c ON s.cars_names = c.car_name
WHERE s.cars_prices IS NOT NULL AND s.cars_prices <> '';