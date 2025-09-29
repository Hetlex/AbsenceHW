# views/suggests_selects.py
import discord
from discord import ui, Interaction, SelectOption
from .suggests_modal import SuggestModal
import traceback

class SuggestCategorySelect(ui.Select):
    def __init__(self):
        options = [
            SelectOption(label="Бот", description="Идеи для улучшения бота"),
            SelectOption(label="Сервер", description="Предложения для сервера"),
            SelectOption(label="Ивенты", description="Идеи для ивентов и активности"),
        ]
        super().__init__(
            placeholder="Выберите категорию для предложения...",
            min_values=1, max_values=1, options=options
        )

    async def callback(self, interaction: Interaction):
        category = self.values[0]
        try:
            await interaction.response.send_modal(SuggestModal(category))
        except Exception:
            traceback.print_exc()
            # Сообщаем пользователю об ошибке (эпхемерно)
            try:
                await interaction.response.send_message(
                    "❌ Не удалось открыть форму. Попробуйте ещё раз.",
                    ephemeral=True
                )
            except Exception:
                await interaction.followup.send(
                    "❌ Не удалось открыть форму. Попробуйте ещё раз.",
                    ephemeral=True
                )

class SuggestMenu(ui.View):
    def __init__(self, timeout: int = 60):
        super().__init__(timeout=timeout)
        self.add_item(SuggestCategorySelect())
