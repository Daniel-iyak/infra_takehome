from flask import Flask, jsonify
import requests
import json
import sqlite3
import os


app = Flask(__name__)
PORT = int(os.getenv('PORT', 5000))

def get_bird(state: str):
    conn = sqlite3.connect("./birds.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM birds WHERE abbreviation = ?", (state,))
    res = cursor.fetchall()
    return [dict(item) for item in res]


def get_weather(state: str):
    try:
        r = requests.get(f'https://api.weather.gov/alerts/active?area={state}')
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        return {"error": str(e)}


@app.get('/')
def hello():
    return "Add a 2 letter state param to learn about birds and the weather challenges they face.", \
           200, \
           {'Content-Type': 'text/html; charset=utf-8'}


@app.get('/<state>')
def bird(state):

    bird = get_bird(state)
    print(bird)
    weather = get_weather(state)
    print(weather)
    out = str([bird, weather])
    return out, 200, {'Content-Type': 'application/json'}


@app.get('/health')
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)

