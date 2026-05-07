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
SELECT DISTINCT ON (s.sido_name)
    s.sido_name,
    s.station_name                          AS worst_station,
    s.khai_value,
    s.khai_grade,
    CASE
        WHEN s.khai_grade = 1 THEN 'Good'
        WHEN s.khai_grade = 2 THEN 'Moderate'
        WHEN s.khai_grade = 3 THEN 'Bad'
        WHEN s.khai_grade = 4 THEN 'Very Bad'
        ELSE 'Unknown'
    END                                     AS grade_label,
    s.pm25_value,
    s.pm10_value,
    CASE
        WHEN s.khai_grade >= 3 THEN true
        ELSE false
    END                                     AS should_tweet,
    s.data_time
FROM silver_air_quality s
WHERE s.khai_value IS NOT NULL
ORDER BY s.sido_name, s.khai_value DESC;