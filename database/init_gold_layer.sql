CREATE TABLE gold_air_quality (
    id              SERIAL PRIMARY KEY,
    sido_name       VARCHAR(50),      -- 서울, 부산 etc.
    worst_station   VARCHAR(100),     -- station with highest khai_value
    khai_value      FLOAT,            -- worst AQI score
    khai_grade      INTEGER,          -- 1/2/3/4
    grade_label     VARCHAR(20),      -- Good / Moderate / Bad / Very Bad
    pm25_value      FLOAT,            -- worst station's pm25
    pm10_value      FLOAT,            -- worst station's pm10
    should_tweet    BOOLEAN,          -- true if khai_grade >= 3
    data_time       TIMESTAMP,
    loaded_at       TIMESTAMP DEFAULT NOW()
);



