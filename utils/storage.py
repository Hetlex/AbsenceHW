import json
import os

AWAY_FILE = "away.json"

def load_data():
    if not os.path.exists(AWAY_FILE):
        return {}
    with open(AWAY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(AWAY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
