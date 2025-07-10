from discord.ext import commands
from views.main_menu import MainMenu
from utils.storage import load_data

class Away(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="away")
    async def away(self, ctx):
        """Starts absence marking process"""
        view = MainMenu()
        await ctx.send("Please select your language / Пожалуйста, выберите язык:", view=view)

    @commands.command(name="awaylist")
    @commands.has_permissions(administrator=True)
    async def awaylist(self, ctx):
        """Shows list of absences, admin only"""
        data = load_data()
        if not data:
            await ctx.send("No one is marked as away.")
            return
        msg = "**Absence List:**\n"
        for user in data.values():
            msg += f"- {user['name']} until {user['until']} ({user['reason']}) Type: {user.get('type', 'N/A')}\n"
        await ctx.send(msg)

    @awaylist.error
    async def awaylist_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")

async def setup(bot):
    await bot.add_cog(Away(bot))
