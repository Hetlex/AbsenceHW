from discord.ext import commands
from views.main_menu import MainMenu

class Away(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def menu(self, ctx):
        """Открыть главное меню управления отсутствиями"""
        view = MainMenu()
        await ctx.send("Выберите действие:", view=view)

async def setup(bot):
    await bot.add_cog(Away(bot))