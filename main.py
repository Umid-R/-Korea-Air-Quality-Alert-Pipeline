from api.weather  import  fetch_data
from database.database import insert_weather, get_weather_for_twit
from twitter.bot import tweet



all_data = fetch_data()
insert_weather(all_data) ## Load all layers: Bronze, Silver, Gold


regions_for_tweet=get_weather_for_twit()
print(regions_for_tweet)





# tweet(regions_for_tweet)

