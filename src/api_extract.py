import requests
from settings import Settings
import json

api_conf = Settings()
baseurl = "http://api.weatherapi.com/v1/current.json"
api_key= api_conf.api_key

def fetch_city_weather(city_name):
    weather_api = f"{baseurl}?key={api_key}&q={city_name}&aqi=no"
    response = requests.get(weather_api)
    print("Response Code: ", response.status_code)
    json_data = json.dumps(response.json())
    print(json_data)
    return response.json()