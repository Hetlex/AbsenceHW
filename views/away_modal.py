import uuid
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

        if lang == "en":
            labels = {
                "from_date": "Start date (DD-MM)",
                "to_date": "End date (DD-MM)",
                "date": "Absence date (DD-MM)",
                "reason": "Reason (optional)",
                "placeholder_reason": "Vacation, work, etc."
            }
            error_invalid_date = "Invalid date format. Use DD-MM."
            error_date_order = "End date must be after start date."
            success_msg = f"Absence '{{type}}' recorded: {{dates}}."
        else:
            labels = {
                "from_date": "Дата начала (ДД-ММ)",
                "to_date": "Дата окончания (ДД-ММ)",
                "date": "Дата отсутствия (ДД-ММ)",
                "reason": "Причина (необязательно)",
                "placeholder_reason": "Отпуск, работа и т.п."
            }
            error_invalid_date = "Неверный формат даты. Используйте ДД-ММ."
            error_date_order = "Дата окончания должна быть позже начала."
            success_msg = f"Отсутствие '{{type}}' отмечено: {{dates}}."

        if absence_type in ["Skipping a week", "Пропускаю неделю"]:
            self.from_date = ui.TextInput(label=labels["from_date"], placeholder="14-07", max_length=5, required=True)
            self.to_date = ui.TextInput(label=labels["to_date"], placeholder="20-07", max_length=5, required=True)
            self.add_item(self.from_date)
            self.add_item(self.to_date)
        elif absence_type in ["Skipping 1 day 5v5", "Пропускаю 1 день 5 на 5"]:
            self.date = ui.TextInput(label=labels["date"], placeholder="15-07", max_length=5, required=True)
            self.add_item(self.date)

        self.reason = ui.TextInput(
            label=labels["reason"],
            style=discord.TextStyle.paragraph,
            required=False,
            placeholder=labels["placeholder_reason"]
        )
        self.add_item(self.reason)

        self.error_invalid_date = error_invalid_date
        self.error_date_order = error_date_order
        self.success_msg = success_msg

    async def on_submit(self, interaction: Interaction):
        try:
            year = datetime.now().year

            if self.absence_type in ["Skipping a week", "Пропускаю неделю"]:
                from_dt = datetime.strptime(self.from_date.value + f"-{year}", "%d-%m-%Y").date()
                to_dt = datetime.strptime(self.to_date.value + f"-{year}", "%d-%m-%Y").date()
                if to_dt < from_dt:
                    await interaction.response.send_message(self.error_date_order, ephemeral=True)
                    return
                date_str = f"{self.from_date.value}–{self.to_date.value}"

            elif self.absence_type in ["Skipping 1 day 5v5", "Пропускаю 1 день 5 на 5"]:
                dt = datetime.strptime(self.date.value + f"-{year}", "%d-%m-%Y").date()
                date_str = self.date.value

            else:
                await interaction.response.send_message(self.error_invalid_date, ephemeral=True)
                return

            record_id = str(uuid.uuid4())
            data = load_data()

            if str(interaction.user.id) not in data:
                data[str(interaction.user.id)] = []

            data[str(interaction.user.id)].append({
                "name": interaction.user.name,
                "until": date_str,
                "reason": self.reason.value or ("No reason" if self.lang == "en" else "Без причины"),
                "type": self.absence_type,
                "id": record_id
            })
            save_data(data)

            await interaction.response.send_message(self.success_msg.format(type=self.absence_type, dates=date_str), ephemeral=True)

        except ValueError:
            await interaction.response.send_message(self.error_invalid_date, ephemeral=True)