import sqlite3
import json


def get_connection():
    return sqlite3.connect('activities.db')


def get_activities(params):
    conn = get_connection()
    c = conn.cursor()

    query = '''
    SELECT * FROM activities
    WHERE 
        ? BETWEEN min_budget AND max_budget
        AND ? BETWEEN min_temperature AND max_temperature
        AND ? BETWEEN min_duration AND max_duration
        AND EXISTS (SELECT 1 FROM json_each(moods) WHERE value = ?)
        AND EXISTS (SELECT 1 FROM json_each(weather_conditions) WHERE value = ? OR value = 'любые')
        AND EXISTS (SELECT 1 FROM json_each(time_of_day) WHERE value = ?)
    '''

    c.execute(query, (
        params['budget'],
        params['temperature'],
        params['free_time'],
        params['mood'],
        params['weather'],
        params['time_of_day']
    ))

    activities = c.fetchall()
    conn.close()
    return activities