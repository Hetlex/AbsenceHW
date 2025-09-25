import discord
from discord.ext import commands
from utils import storage

class SheetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="testget")
    async def first_row(self, ctx):
        """Возвращает первую строку из Google Sheet"""
        rows = storage.get_all_rows()
        if not rows:
            await ctx.send("⚠️ Таблица пуста.")
            return

        first_row = rows[0]  # первая запись
        msg = f"📄 **Первая строка таблицы:**\n{first_row}"
        await ctx.send(msg)

# Функция загрузки COG-а
async def setup(bot):
    await bot.add_cog(SheetCog(bot))
