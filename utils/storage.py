import json
import os
import gspread
from google.oauth2.service_account import Credentials
import logging

AWAY_FILE = "away.json"
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds_json = os.getenv("GOOGLE_CREDS")
if not creds_json:
    raise ValueError("❌ Не найдена переменная окружения GOOGLE_CREDS!")

def connect_sheet():
    try:
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
        client = gspread.authorize(creds)
        sheet = client.open("HWGuild").sheet1
        print(f"✅ Подключение к Google Sheet прошло успешно!")
        return sheet
    except Exception as e:
        print(f"❌ Ошибка при подключении к Google Sheet: {e}")
        raise e  # пробрасываем дальше, чтобы бот не запускался без листа

sheet = connect_sheet()

def load_data():
    if not os.path.exists(AWAY_FILE):
        return {}
    with open(AWAY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(AWAY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_all_rows():
    return sheet.get_all_records()