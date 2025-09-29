# views/suggests_modal.py
import discord
from discord import ui, Interaction
from utils.storage import load_suggests, save_suggests
from datetime import datetime
import traceback

class SuggestModal(ui.Modal):
    def __init__(self, category: str):
        super().__init__(title=f"Предложение ({category})")
        self.category = category
        self.suggest_text = ui.TextInput(
            label="Ваше предложение",
            style=discord.TextStyle.paragraph,
            placeholder="Опишите вашу идею...",
            required=True,
            max_length=500
        )
        self.add_item(self.suggest_text)

    async def on_submit(self, interaction: Interaction):
        try:
            suggests = load_suggests()
            suggests.append({
                "author": str(interaction.user),
                "user_id": interaction.user.id,
                "category": self.category,
                "text": self.suggest_text.value,
                "time": datetime.now().strftime("%d.%m.%Y %H:%M")
            })
            save_suggests(suggests)
            await interaction.response.send_message(
                f"✅ Ваше предложение в категории **{self.category}** сохранено!",
                ephemeral=True
            )
        except Exception:
            # печатаем трассировку в консоль для отладки
            traceback.print_exc()
            # пытаемся сообщить пользователю
            try:
                await interaction.response.send_message(
                    "❌ Произошла ошибка при сохранении предложения. Посмотрите логи бота.",
                    ephemeral=True
                )
            except Exception:
                # если response уже был использован (редкий кейс), используем followup
                await interaction.followup.send(
                    "❌ Произошла ошибка при сохранении предложения. Посмотрите логи бота.",
                    ephemeral=True
                )
