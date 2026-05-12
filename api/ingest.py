import requests
import os
from dotenv import load_dotenv
from database.database import insert_bronze
load_dotenv()
import time

API_KEY = os.getenv("WEATHER_API")
url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty'
regions = [
    "서울", "부산", "대구", "인천",
    "광주", "대전", "울산", "경기",
    "강원", "충북", "충남", "전북",
    "전남", "경북", "경남", "제주",
    "세종"
]

def fetch_data():
    all_data = []
    for region in regions:
        params = {
            'serviceKey': API_KEY,
            'returnType': 'json',
            'numOfRows': '100',
            'pageNo': '1',
            'sidoName': region,
            'ver': '1.0'
        }
        try:
            response = requests.get(url, params=params)
            items = response.json()['response']['body']['items']
            all_data.extend(items)
            print(f"✅ {region} — {len(items)} stations fetched")
        except Exception as e:
            print(f"❌ {region} failed: {e}")
        time.sleep(1)

    insert_bronze(all_data)
    print(f"✅ Total {len(all_data)} rows inserted to bronze")
    return 0


params = {
            'serviceKey': API_KEY,
            'returnType': 'json',
            'numOfRows': '100',
            'pageNo': '1',
            'sidoName': '세종',
            'ver': '1.0'
        }
response = requests.get(url, params=params)
print(response.text)
