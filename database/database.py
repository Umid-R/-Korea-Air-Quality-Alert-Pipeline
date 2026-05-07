
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_PUBLISHABLE_KEY")
)


def insert_weather(rows: list):
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
    if response.data:
        supabase.rpc("load_silver").execute()
        supabase.rpc("load_gold").execute()
    return response.data


def get_weather_for_twit():
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

    return list(latest.values())
