import discord
from discord import ui, Interaction
from utils.storage import load_data, save_data
from datetime import datetime

class AwayModal(ui.Modal):
    def __init__(self, absence_type: str, lang: str = "en"):
        title = "Mark Absence" if lang == "en" else "Отметить отсутствие"
        super().__init__(title=title)
        self.absence_type = absence_type
        self.lang = lang

        # Подготовим лейблы и плейсхолдеры
        if lang == "en":
            labels = {
                "from_date": "Start date of the week (YYYY-MM-DD)",
                "to_date": "End date of the week (YYYY-MM-DD)",
                "date": "Date of absence (YYYY-MM-DD)",
                "first_date": "First absence date (YYYY-MM-DD)",
                "second_date": "Second absence date (YYYY-MM-DD)",
                "reason": "Reason (optional)",
                "placeholder_reason": "Vacation, work, etc."
            }
            error_invalid_date = "Invalid date format. Use YYYY-MM-DD."
            error_date_order = "End date cannot be earlier than start date."
            success_msg = f"Absence '{absence_type}' recorded until {{dates}}."
        else:
            labels = {
                "from_date": "Дата начала недели (YYYY-MM-DD)",
                "to_date": "Дата окончания недели (YYYY-MM-DD)",
                "date": "Дата отсутствия (YYYY-MM-DD)",
                "first_date": "Первая дата отсутствия (YYYY-MM-DD)",
                "second_date": "Вторая дата отсутствия (YYYY-MM-DD)",
                "reason": "Причина (опционально)",
                "placeholder_reason": "Отпуск, работа и т.д."
            }
            error_invalid_date = "Неверный формат даты. Используйте YYYY-MM-DD."
            error_date_order = "Дата окончания не может быть раньше даты начала."
            success_msg = f"Отсутствие '{absence_type}' отмечено: {{dates}}."

        # Добавляем поля
        if absence_type in ["Skipping a week", "Пропускаю неделю"]:
            self.from_date = ui.TextInput(label=labels["from_date"], placeholder="2025-07-14", max_length=10, required=True)
            self.to_date = ui.TextInput(label=labels["to_date"], placeholder="2025-07-20", max_length=10, required=True)
            self.add_item(self.from_date)
            self.add_item(self.to_date)
        elif absence_type in ["Skipping 1 day 5v5", "Пропускаю 1 день 5 на 5"]:
            self.date = ui.TextInput(label=labels["date"], placeholder="2025-07-15", max_length=10, required=True)
            self.add_item(self.date)
        elif absence_type in ["Skipping 2 days 5v5", "Пропускаю 2 дня 5 на 5"]:
            self.first_date = ui.TextInput(label=labels["first_date"], placeholder="2025-07-15", max_length=10, required=True)
            self.second_date = ui.TextInput(label=labels["second_date"], placeholder="2025-07-16", max_length=10, required=True)
            self.add_item(self.first_date)
            self.add_item(self.second_date)
        else:
            self.date = ui.TextInput(label=labels["date"], placeholder="2025-07-15", max_length=10, required=True)
            self.add_item(self.date)

        self.reason = ui.TextInput(label=labels["reason"], style=discord.TextStyle.paragraph, required=False, placeholder=labels["placeholder_reason"])
        self.add_item(self.reason)

        self.error_invalid_date = error_invalid_date
        self.error_date_order = error_date_order
        self.success_msg = success_msg

    async def on_submit(self, interaction: Interaction):
        try:
            if self.absence_type in ["Skipping a week", "Пропускаю неделю"]:
                from_dt = datetime.strptime(self.from_date.value, "%Y-%m-%d").date()
                to_dt = datetime.strptime(self.to_date.value, "%Y-%m-%d").date()
                if to_dt < from_dt:
                    await interaction.response.send_message(self.error_date_order, ephemeral=True)
                    return
                date_str = f"{from_dt} - {to_dt}"
            elif self.absence_type in ["Skipping 1 day 5v5", "Пропускаю 1 день 5 на 5"]:
                dt = datetime.strptime(self.date.value, "%Y-%m-%d").date()
                date_str = str(dt)
            elif self.absence_type in ["Skipping 2 days 5v5", "Пропускаю 2 дня 5 на 5"]:
                first_dt = datetime.strptime(self.first_date.value, "%Y-%m-%d").date()
                second_dt = datetime.strptime(self.second_date.value, "%Y-%m-%d").date()
                date_str = f"{first_dt}, {second_dt}"
            else:
                dt = datetime.strptime(self.date.value, "%Y-%m-%d").date()
                date_str = str(dt)

            data = load_data()
            data[str(interaction.user.id)] = {
                "name": interaction.user.name,
                "until": date_str,
                "reason": self.reason.value or (self.success_msg if self.lang == "ru" else "No reason"),
                "type": self.absence_type
            }
            save_data(data)

            await interaction.response.send_message(self.success_msg.format(dates=date_str), ephemeral=True)
        except ValueError:
            await interaction.response.send_message(self.error_invalid_date, ephemeral=True)
