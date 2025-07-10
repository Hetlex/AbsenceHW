from discord import ui, Interaction, ButtonStyle
from utils.storage import load_data
from .away_modal import AwayModal

class MainMenu(ui.View):
    def __init__(self, timeout=60):
        super().__init__(timeout=timeout)

    @ui.button(label="Отметить отсутствие", style=ButtonStyle.primary)
    async def mark_away(self, button: ui.Button, interaction: Interaction):
        await interaction.response.send_modal(AwayModal())

    @ui.button(label="Список отсутствующих", style=ButtonStyle.secondary)
    async def show_awaylist(self, button: ui.Button, interaction: Interaction):
        data = load_data()
        if not data:
            await interaction.response.send_message("Список отсутствующих пуст.", ephemeral=True)
            return
        msg = "**Список отсутствующих:**\n"
        for user in data.values():
            msg += f"- {user['name']} до {user['until']} ({user['reason']})\n"
        await interaction.response.send_message(msg, ephemeral=True)
