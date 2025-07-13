import discord
from discord import ui, Interaction, SelectOption
from .away_modal import AwayModal

class AbsenceTypeSelect(ui.Select):
    def __init__(self):
        options = [
            SelectOption(label="Пропускаю неделю", description="Не смогу набить недельный лимит"),
            SelectOption(label="Пропускаю 1 день 5 на 5"),
        ]
        super().__init__(placeholder="Выберите тип отсутствия...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        await interaction.response.send_modal(AwayModal(absence_type=self.values[0]))
