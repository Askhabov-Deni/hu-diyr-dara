from database import get_activities
from weather_api import get_weather
from datetime import datetime
import pytz


def get_time_of_day():
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    hour = now.hour
    if 6 <= hour < 12:
        return "утро"
    elif 12 <= hour < 18:
        return "день"
    elif 18 <= hour < 23:
        return "вечер"
    else:
        return "ночь"


def recommend_activities(budget, mood, free_time, city):
    try:
        weather_data = get_weather(city)
        time_of_day = get_time_of_day()

        params = {
            'budget': float(budget),
            'mood': mood,
            'free_time': int(free_time),
            'temperature': weather_data['temperature'],
            'weather': weather_data['weather'],
            'time_of_day': time_of_day
        }

        return get_activities(params)
    except Exception as e:
        print(f"Recommendation error: {e}")
        return []