from discord import ui, Interaction
from utils.storage import load_data, save_data
from datetime import datetime

class AwayModal(ui.Modal, title="Отметить отсутствие"):
    until_date = ui.TextInput(
        label="До какой даты? (в формате YYYY-MM-DD)",
        placeholder="Например: 2025-07-20",
        required=True,
        max_length=10
    )
    reason = ui.TextInput(
        label="Причина (опционально)",
        placeholder="Работа, отпуск, учёба и т.д.",
        required=False,
        style=discord.TextStyle.paragraph
    )

    async def on_submit(self, interaction: Interaction):
        try:
            datetime.strptime(self.until_date.value, "%Y-%m-%d").date()
        except ValueError:
            await interaction.response.send_message("Неверный формат даты. Используй YYYY-MM-DD.", ephemeral=True)
            return

        data = load_data()
        data[str(interaction.user.id)] = {
            "name": interaction.user.name,
            "until": self.until_date.value,
            "reason": self.reason.value or "Не указана"
        }
        save_data(data)

        await interaction.response.send_message(
            f"Отмечено: {interaction.user.name} отсутствует до {self.until_date.value}. Причина: {self.reason.value or 'Не указана'}",
            ephemeral=True
        )
