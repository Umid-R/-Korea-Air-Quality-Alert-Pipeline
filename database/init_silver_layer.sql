CREATE TABLE silver_air_quality (
    id              SERIAL PRIMARY KEY,
    station_name    VARCHAR(100),
    sido_name       VARCHAR(50),
    data_time       TIMESTAMP,     
    pm10_value      FLOAT,   
    pm25_value      FLOAT,
    o3_value        FLOAT,
    no2_value       FLOAT,
    co_value        FLOAT,
    so2_value       FLOAT,
    khai_value      FLOAT,
    khai_grade      INTEGER,       
    pm10_grade      INTEGER,
    pm25_grade      INTEGER,
    o3_grade        INTEGER,
    no2_grade       INTEGER,
    co_grade        INTEGER,
    so2_grade       INTEGER,
    loaded_at       TIMESTAMP DEFAULT NOW()
);


