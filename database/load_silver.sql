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
    TO_TIMESTAMP(data_time, 'YYYY-MM-DD HH24:MI')   AS data_time,
    NULLIF(pm10_value, '-')::FLOAT                   AS pm10_value,
    NULLIF(pm25_value, '-')::FLOAT                   AS pm25_value,
    NULLIF(o3_value,   '-')::FLOAT                   AS o3_value,
    NULLIF(no2_value,  '-')::FLOAT                   AS no2_value,
    NULLIF(co_value,   '-')::FLOAT                   AS co_value,
    NULLIF(so2_value,  '-')::FLOAT                   AS so2_value,
    NULLIF(khai_value, '-')::FLOAT                   AS khai_value,
    NULLIF(khai_grade, '-')::INTEGER                 AS khai_grade,
    NULLIF(pm10_grade, '-')::INTEGER                 AS pm10_grade,
    NULLIF(pm25_grade, '-')::INTEGER                 AS pm25_grade,
    NULLIF(o3_grade,   '-')::INTEGER                 AS o3_grade,
    NULLIF(no2_grade,  '-')::INTEGER                 AS no2_grade,
    NULLIF(co_grade,   '-')::INTEGER                 AS co_grade,
    NULLIF(so2_grade,  '-')::INTEGER                 AS so2_grade
FROM bronze_air_quality;

