CREATE OR REPLACE FUNCTION load_gold()
RETURNS void AS $$
BEGIN

TRUNCATE gold_air_quality;

INSERT INTO gold_air_quality (
    sido_name,
    worst_station,
    khai_value,
    khai_grade,
    grade_label,
    pm25_value,
    pm10_value,
    should_tweet,
    data_time
)
WITH latest AS (
    SELECT DISTINCT ON (station_name, sido_name) *
    FROM silver_air_quality
    WHERE khai_value IS NOT NULL
    ORDER BY station_name, sido_name, data_time DESC
),
recent AS (
    SELECT * FROM latest
    WHERE data_time >= (SELECT MAX(data_time) FROM latest) - INTERVAL '3 hours'
)
SELECT DISTINCT ON (sido_name)
    sido_name,
    station_name,
    khai_value,
    khai_grade,
    CASE khai_grade
        WHEN 1 THEN 'Good'
        WHEN 2 THEN 'Moderate'
        WHEN 3 THEN 'Bad'
        WHEN 4 THEN 'Very Bad'
        ELSE 'Unknown'
    END,
    pm25_value,
    pm10_value,
    (khai_grade >= 3),
    data_time
FROM recent
ORDER BY sido_name, khai_value DESC;

END;
$$ LANGUAGE plpgsql;