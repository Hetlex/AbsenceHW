import json
import os

AWAY_FILE = "away.json"

def load_data():
    if not os.path.exists(AWAY_FILE):
        return {}
    with open(AWAY_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(AWAY_FILE, "w") as f:
        json.dump(data, f, indent=2)