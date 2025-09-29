import json
import os
import gspread
from google.oauth2.service_account import Credentials

AWAY_FILE = "away.json"
SUGGEST_FILE = "suggests.json"
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

def connect_client():
    """Создаёт и возвращает авторизованный объект gspread Client"""
    creds_json = os.getenv("GOOGLE_CREDS")
    if not creds_json:
        raise ValueError("❌ Не найдена переменная окружения GOOGLE_CREDS!")
    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
    client = gspread.authorize(creds)
    return client

def connect_sheet(sheet_index=-1):
    """
    Возвращает объект листа (sheet) с уведомлением.
    По умолчанию выбирается последняя вкладка (-1).
    """
    try:
        client = connect_client()
        doc = client.open("HWGuild")
        sheets = doc.worksheets()
        sheet = sheets[sheet_index]
        print(f"✅ Подключение к Google Sheet прошло успешно! Используется лист: {sheet.title}")
        return sheet
    except Exception as e:
        print(f"❌ Ошибка при подключении к Google Sheet: {e}")
        raise e  # пробрасываем дальше, чтобы бот не запускался без листа

# --- Автопроверка подключения при импорте ---
try:
    _ = connect_sheet()  # проверяем подключение при загрузке модуля
except Exception:
    pass

def load_data():
    if not os.path.exists(AWAY_FILE):
        return {}
    with open(AWAY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(AWAY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_all_rows():
    sheet = connect_sheet()
    return sheet.get_all_records()

def get_user_stats_by_nick(discord_user):
    """Возвращает статистику пользователя на последней вкладке"""
    sheet = connect_sheet()
    all_values = sheet.get_all_values()
    user_str = str(discord_user)

    for row in all_values[1:]:
        if any(cell.strip() == user_str for cell in row):
            nickname = row[1] if len(row) > 1 else "Неизвестно"
            week_headers = all_values[0][6:16]  # G:P
            week_values = row[6:16] if len(row) > 6 else []
            stats = dict(zip(week_headers, week_values))
            return nickname, stats
    return None

def get_user_stats_all(discord_user):
    """Возвращает статистику пользователя по всем вкладкам"""
    client = connect_client()
    doc = client.open("HWGuild")
    result = {}

    for sheet in doc.worksheets():
        all_values = sheet.get_all_values()
        user_str = str(discord_user)

        for row in all_values[1:]:
            if any(cell.strip() == user_str for cell in row):
                nickname = row[1] if len(row) > 1 else "Неизвестно"
                week_headers = all_values[0][6:16]
                week_values = row[6:16] if len(row) > 6 else []
                stats = dict(zip(week_headers, week_values))
                result[sheet.title] = (nickname, stats)
                break
    return result

#Саджесты тут

if not os.path.exists(SUGGEST_FILE):
    with open(SUGGEST_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

def load_suggests():
    with open(SUGGEST_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_suggests(suggests):
    with open(SUGGEST_FILE, "w", encoding="utf-8") as f:
        json.dump(suggests, f, ensure_ascii=False, indent=2)
