import tweepy
import os
from dotenv import load_dotenv
from datetime import datetime
from database.database import get_weather_for_tweet
load_dotenv()

# authenticate
client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
)


def tweet():
    
    data=get_weather_for_tweet()
    number_of_tweets=len(data)
    print(f"Number of tweets: {number_of_tweets}")
    for region in data:
        message = f"""🔴 대기질 경보 — {region['sido_name']}!

최악 지역: {region['worst_station']}
통합대기환경지수: {region['khai_value']}
등급: {region['grade_label']} 😷
측정 시간: {datetime.fromisoformat(region['data_time']).strftime("%H:%M")}

PM2.5: {region['pm25_value']} μg/m³
PM10: {region['pm10_value']} μg/m³

실내에 머무르고 마스크를 착용하세요!
#미세먼지 #대기질 #Korea #AirQuality"""

        client.create_tweet(text=message)
        
