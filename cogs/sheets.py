import discord
from discord.ext import commands
from utils import storage

class SheetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="testget")
    async def all_rows(self, ctx):
        """Возвращает все строки из Google Sheet"""
        rows = storage.get_all_rows()
        if not rows:
            await ctx.send("⚠️ Таблица пуста.")
            return

        # Формируем красивый вывод
        msg = "📄 **Все строки в таблице:**\n"
        for i, row in enumerate(rows, start=2):  # start=2 чтобы соответствовать индексам sheet
            msg += f"{i}: {row}\n"

        # Если слишком много строк, разрезаем на несколько сообщений
        chunk_size = 2000  # ограничение Discord
        for i in range(0, len(msg), chunk_size):
            await ctx.send(msg[i:i+chunk_size])

# Функция загрузки COG-а
async def setup(bot):
    await bot.add_cog(SheetCog(bot))
