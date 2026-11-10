-- Remembers which alerts were already tweeted, so the bot does not repeat itself every hour.
CREATE TABLE IF NOT EXISTS tweet_log (
    id          SERIAL PRIMARY KEY,
    sido_name   VARCHAR(50) NOT NULL,   -- region
    khai_grade  INTEGER,                -- grade at the time of the alert
    khai_value  FLOAT,                  -- AQI at the time of the alert
    tweeted_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_tweet_log_sido_time ON tweet_log (sido_name, tweeted_at DESC);
