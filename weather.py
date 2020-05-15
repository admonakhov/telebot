import requests
import config

URL = 'http://api.openweathermap.org/data/2.5/weather'
_city = "Moscow"


def weather(city="Moscow"):
    global _city
    _city = city
    params = {
        'q': city,
        'appid': config.WEATHER_APPID,
        'lang': 'ru',
        'units': 'metric'

    }
    data = requests.get(URL, params=params).json()
    return data['main']
