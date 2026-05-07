import tweepy
import os
from dotenv import load_dotenv
from datetime import datetime
from database.database import get_weather_for_twit
load_dotenv()

# authenticate
client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
)


def tweet():
    
    data=get_weather_for_twit()
    
    for region in data:
        message = f"""🔴 Air Quality Alert — {region['sido_name']}!

Worst area: {region['worst_station']}
AQI Score: {region['khai_value']}
Grade: {region['grade_label']} 😷
Time: {datetime.fromisoformat(region['data_time']).strftime("%H:%M")}

PM2.5: {region['pm25_value']} μg/m³
PM10: {region['pm10_value']} μg/m³

Stay indoors and wear a mask!
#Korea #AirQuality #미세먼지"""

        client.create_tweet(text=message)
        
