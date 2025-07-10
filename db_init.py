import sqlite3
import json


def init_db():
    conn = sqlite3.connect('activities.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        min_budget REAL DEFAULT 0,
        max_budget REAL,
        moods TEXT NOT NULL,
        min_temperature INTEGER,
        max_temperature INTEGER,
        weather_conditions TEXT NOT NULL,
        time_of_day TEXT NOT NULL,
        min_duration INTEGER,
        max_duration INTEGER
    )''')

    # Примеры активностей
    activities = [
        {
            "name": "Чтение книги",
            "description": "Погружение в мир литературы дома или в парке",
            "min_budget": 0,
            "max_budget": 300,
            "moods": json.dumps(["спокойный", "грустный", "нейтральный"]),
            "min_temperature": 10,
            "max_temperature": 30000,
            "weather_conditions": json.dumps(["ясно", "облачно"]),
            "time_of_day": json.dumps(["утро", "вечер", "день", "ночь"]),
            "min_duration": 30,
            "max_duration": 120
        },
        {
            "name": "Пикник",
            "description": "Еда на природе с друзьями",
            "min_budget": 500,
            "max_budget": 2000,
            "moods": json.dumps(["веселый", "энергичный", "радостный"]),
            "min_temperature": 18,
            "max_temperature": 37,
            "weather_conditions": json.dumps(["ясно"]),
            "time_of_day": json.dumps(["утро", "вечер", "день"]),
            "min_duration": 60,
            "max_duration": 180
        },
        {
            "name": "Футбол с друзьями",
            "description": "Активная игра в футбол на открытом воздухе",
            "min_budget": 0,
            "max_budget": 1000,
            "moods": json.dumps(["энергичный", "веселый", "радостный"]),
            "min_temperature": 15,
            "max_temperature": 33,
            "weather_conditions": json.dumps(["ясно", "облачно"]),
            "time_of_day": json.dumps(["утро", "вечер", "день"]),
            "min_duration": 60,
            "max_duration": 120
        },
        {
            "name": "Поход в музей",
            "description": "Посещение местного музея",
            "min_budget": 200,
            "max_budget": 1000,
            "moods": json.dumps(["нейтральный", "любознательный"]),
            "min_temperature": 5,
            "max_temperature": 33,
            "weather_conditions": json.dumps(["дождь", "пасмурно", "ясно"]),
            "time_of_day": json.dumps(["утро", "вечер", "день"]),
            "min_duration": 90,
            "max_duration": 180
        },
        {
            "name": "Кинотеатр",
            "description": "Просмотр нового фильма в кино",
            "min_budget": 300,
            "max_budget": 1500,
            "moods": json.dumps(["нейтральный", "романтичный", "грустный"]),
            "min_temperature": -10,
            "max_temperature": 2500,
            "weather_conditions": json.dumps(["любые"]),
            "time_of_day": json.dumps(["утро", "вечер", "день", "ночь"]),
            "min_duration": 120,
            "max_duration": 240
        },
        {
            "name": "Йога в парке",
            "description": "Занятие йогой на свежем воздухе",
            "min_budget": 0,
            "max_budget": 0,
            "moods": json.dumps(["спокойный", "расслабленный"]),
            "min_temperature": 18,
            "max_temperature": 28,
            "weather_conditions": json.dumps(["ясно", "легкий ветер"]),
            "time_of_day": json.dumps(["утро", "вечер"]),
            "min_duration": 45,
            "max_duration": 90
        },
        {
            "name": "Велосипедная прогулка",
            "description": "Прокатиться на велосипеде по городу",
            "min_budget": 0,
            "max_budget": 0,
            "moods": json.dumps(["энергичный", "радостный"]),
            "min_temperature": 15,
            "max_temperature": 30,
            "weather_conditions": json.dumps(["ясно", "облачно"]),
            "time_of_day": json.dumps(["утро", "день"]),
            "min_duration": 60,
            "max_duration": 120
        },
        {
            "name": "Приготовление ужина",
            "description": "Приготовить изысканный ужин дома",
            "min_budget": 300,
            "max_budget": 1500,
            "moods": json.dumps(["спокойный", "романтичный", "нейтральный"]),
            "min_temperature": -10,
            "max_temperature": 300,
            "weather_conditions": json.dumps(["любые"]),
            "time_of_day": json.dumps(["вечер", "ночь"]),
            "min_duration": 60,
            "max_duration": 120
        },
        {
            "name": "Игра в настольные игры",
            "description": "Собраться с друзьями для игр",
            "min_budget": 0,
            "max_budget": 500,
            "moods": json.dumps(["веселый", "социальный"]),
            "min_temperature": -10,
            "max_temperature": 100000000000,
            "weather_conditions": json.dumps(["любые"]),
            "time_of_day": json.dumps(["утро", "вечер", "день", "ночь"]),
            "min_duration": 60,
            "max_duration": 180
        },
        {
            "name": "Прогулка по городу",
            "description": "Неспешная прогулка по интересным местам",
            "min_budget": 0,
            "max_budget": 200,
            "moods": json.dumps(["спокойный", "нейтральный"]),
            "min_temperature": 10,
            "max_temperature": 2100,
            "weather_conditions": json.dumps(["ясно", "облачно", "небольшой дождь"]),
            "time_of_day": json.dumps(["утро", "вечер", "день", "ночь"]),
            "min_duration": 30,
            "max_duration": 90
        }
    ]

    for activity in activities:
        c.execute('''INSERT INTO activities (
            name, description, min_budget, max_budget, moods, 
            min_temperature, max_temperature, weather_conditions, 
            time_of_day, min_duration, max_duration
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
            activity['name'],
            activity['description'],
            activity['min_budget'],
            activity['max_budget'],
            activity['moods'],
            activity['min_temperature'],
            activity['max_temperature'],
            activity['weather_conditions'],
            activity['time_of_day'],
            activity['min_duration'],
            activity['max_duration']
        ))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")