CREATE OR REPLACE FUNCTION load_silver()
RETURNS void AS $$
BEGIN

TRUNCATE silver_air_quality;

INSERT INTO silver_air_quality (
    station_name,
    sido_name,
    data_time,
    pm10_value,
    pm25_value,
    o3_value,
    no2_value,
    co_value,
    so2_value,
    khai_value,
    khai_grade,
    pm10_grade,
    pm25_grade,
    o3_grade,
    no2_grade,
    co_grade,
    so2_grade
)
SELECT
    station_name,
    sido_name,
    CASE
        WHEN data_time LIKE '%24:00%'
        THEN TO_TIMESTAMP(REPLACE(data_time, '24:00', '00:00'), 'YYYY-MM-DD HH24:MI') + INTERVAL '1 day'
        ELSE TO_TIMESTAMP(data_time, 'YYYY-MM-DD HH24:MI')
    END,
    NULLIF(pm10_value, '-')::FLOAT,
    NULLIF(pm25_value, '-')::FLOAT,
    NULLIF(o3_value,   '-')::FLOAT,
    NULLIF(no2_value,  '-')::FLOAT,
    NULLIF(co_value,   '-')::FLOAT,
    NULLIF(so2_value,  '-')::FLOAT,
    NULLIF(khai_value, '-')::FLOAT,
    NULLIF(khai_grade, '-')::INTEGER,
    NULLIF(pm10_grade, '-')::INTEGER,
    NULLIF(pm25_grade, '-')::INTEGER,
    NULLIF(o3_grade,   '-')::INTEGER,
    NULLIF(no2_grade,  '-')::INTEGER,
    NULLIF(co_grade,   '-')::INTEGER,
    NULLIF(so2_grade,  '-')::INTEGER
FROM bronze_air_quality;

END;
$$ LANGUAGE plpgsql;