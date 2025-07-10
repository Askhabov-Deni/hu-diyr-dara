import requests
from config import OPENWEATHERMAP_API_KEY


def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': OPENWEATHERMAP_API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        print(data['main']['temp'])
        print(data['weather'][0]['description'])
        print(data['name'])
        return {
            'temperature': data['main']['temp'],
            'weather': data['weather'][0]['description'],
            'city': data['name']
        }
    else:
        raise Exception(f"Weather API error: {data.get('message', 'Unknown')}")