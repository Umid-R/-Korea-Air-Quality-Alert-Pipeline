
import os
from datetime import datetime, timedelta, timezone
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_PUBLISHABLE_KEY")
)


def insert_bronze(rows: list):
    mapped = [{
        "station_name": row.get("stationName"),
        "sido_name":    row.get("sidoName"),
        "data_time":    row.get("dataTime"),
        "pm10_value":   row.get("pm10Value"),
        "pm25_value":   row.get("pm25Value"),
        "o3_value":     row.get("o3Value"),
        "no2_value":    row.get("no2Value"),
        "co_value":     row.get("coValue"),
        "so2_value":    row.get("so2Value"),
        "khai_value":   row.get("khaiValue"),
        "khai_grade":   row.get("khaiGrade"),
        "pm10_grade":   row.get("pm10Grade"),
        "pm25_grade":   row.get("pm25Grade"),
        "o3_grade":     row.get("o3Grade"),
        "no2_grade":    row.get("no2Grade"),
        "co_grade":     row.get("coGrade"),
        "so2_grade":    row.get("so2Grade"),
        "co_flag":      row.get("coFlag"),
        "pm10_flag":    row.get("pm10Flag"),
        "pm25_flag":    row.get("pm25Flag"),
        "no2_flag":     row.get("no2Flag"),
        "o3_flag":      row.get("o3Flag"),
        "so2_flag":     row.get("so2Flag"),
    } for row in rows]
    
    response = supabase.table("bronze_air_quality").insert(mapped).execute()
    
    return response.data


# Do not repeat an alert for the same region within this many hours,
# unless the grade got worse since the last alert (e.g. Bad -> Very Bad).
TWEET_COOLDOWN_HOURS = 24


def get_last_tweets():
    """Return {sido_name: {"khai_grade": ..., "tweeted_at": ...}} for alerts sent within the cooldown."""
    since = (datetime.now(timezone.utc) - timedelta(hours=TWEET_COOLDOWN_HOURS)).isoformat()
    response = (
        supabase.table("tweet_log")
        .select("sido_name, khai_grade, tweeted_at")
        .gte("tweeted_at", since)
        .order("tweeted_at", desc=True)
        .execute()
    )
    last = {}
    for row in response.data:
        if row["sido_name"] not in last:
            last[row["sido_name"]] = row
    return last


def log_tweet(region: dict):
    supabase.table("tweet_log").insert({
        "sido_name": region["sido_name"],
        "khai_grade": region["khai_grade"],
        "khai_value": region["khai_value"],
    }).execute()


def should_send_alert(region: dict, last_tweets: dict) -> bool:
    """Alert if no alert was sent for this region in the cooldown window, or the grade got worse."""
    last = last_tweets.get(region["sido_name"])
    if last is None:
        return True
    return (region["khai_grade"] or 0) > (last["khai_grade"] or 0)


def get_weather_for_tweet():
    response = (
        supabase.table("gold_air_quality")
        .select("*")
        .eq("should_tweet", True)
        .order("data_time", desc=True)
        .execute()
    )

    data = response.data

    latest = {}
    for row in data:
        city = row["sido_name"]
        if city not in latest:
            latest[city] = row

    last_tweets = get_last_tweets()
    return [row for row in latest.values() if should_send_alert(row, last_tweets)]
