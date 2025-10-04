import discord
from discord.ext import commands
from utils import storage

class CongratsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="congrats")
    async def congrats(self, ctx, week_index: int = 1, *, message_text: str = None):
        """
        Поздравляет участников, у которых очки за указанную неделю (week_index)
        в диапазоне 5800–6330. Имена берутся из колонки D.
        Пример:
          !congrats 2 Поздравляем всех бойцов!
        """
        try:
            sheet = storage.connect_sheet()
        except Exception as e:
            await ctx.author.send(f"❌ Не удалось подключиться к Google Sheets: {e}")
            return

        all_values = sheet.get_all_values()
        if not all_values or len(all_values) < 2:
            await ctx.author.send("⚠️ В таблице нет данных.")
            return

        headers = all_values[0]

        # Находим все колонки, где в названии есть "week"
        week_columns = [i for i, h in enumerate(headers) if h.strip().lower().startswith("week")]
        if not week_columns:
            await ctx.author.send("⚠️ Не найдены колонки с названием 'week'.")
            return

        # Проверяем корректность индекса
        if week_index < 1 or week_index > len(week_columns):
            await ctx.author.send(f"⚠️ Неверный индекс недели. Всего доступно: {len(week_columns)}")
            return

        target_col_index = week_columns[week_index - 1]
        week_name = headers[target_col_index]

        # Собираем пользователей из колонки D с поинтами в диапазоне 5800–6330
        qualified_users = []
        for row in all_values[1:]:
            if len(row) > target_col_index:
                try:
                    value = int(row[target_col_index])
                    if 5800 <= value <= 6330:
                        if len(row) > 3:  # колонка D = индекс 3
                            qualified_users.append(row[3])
                except ValueError:
                    continue

        # Формируем сообщение
        message = (
            f"@Guild Member\n"
            f"Point counting for **{week_name}** finished!\n\n"
            f"Congratulate for 5v5 tier 3 up for :Crab: :\n"
            f"{message_text or '*no custom message*'}\n\n"
            f"Congratulations for max week limit for 🫡 :\n"
        )

        if qualified_users:
            message += "\n".join(f"@{nick}" for nick in qualified_users)
        else:
            message += "_No users reached 5800–6330 this week._"

        # Отправляем пользователю в личку embed
        try:
            embed = discord.Embed(
                title="🎉 Weekly Congratulations!",
                description=message,
                color=discord.Color.green()
            )
            await ctx.author.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("⚠️ Не удалось отправить сообщение в ЛС — у тебя закрыты личные сообщения.")


async def setup(bot):
    await bot.add_cog(CongratsCog(bot))
