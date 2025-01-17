import os
import requests


def weather_res(location):
    weather_url = f"http://api.weatherapi.com/v1/forecast.json?key={os.environ['API_KEY_WAPI']}&q={location}&days=1&aqi=no&alerts=no"
    return requests.get(weather_url).json()