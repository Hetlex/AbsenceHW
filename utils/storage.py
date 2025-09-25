import json
import os
import gspread
from google.oauth2.service_account import Credentials

AWAY_FILE = "away.json"
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

CREDS_FILE = "credentials.json"
SHEET_NAME = "HWGuild"

def connect_sheet():
    try:
        creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPE)
        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME).sheet1
        print(f"✅ Подключение к Google Sheet '{SHEET_NAME}' прошло успешно!")
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