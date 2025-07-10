from discord.ext import commands
from datetime import datetime
from utils.storage import load_data, save_data

class Away(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def away(self, ctx, until_date, *, reason="No reason provided"):
        user_id = str(ctx.author.id)
        try:
            datetime.strptime(until_date, "%Y-%m-%d").date()
        except ValueError:
            await ctx.send("Invalid date format. Use YYYY-MM-DD.")
            return
        
        data = load_data()
        data[user_id] = {
            "name": ctx.author.name,
            "until": until_date,
            "reason": reason
        }
        save_data(data)
        await ctx.send(f"{ctx.author.name} marked as away until {until_date}. Reason: {reason}")

    @commands.command()
    async def awaylist(self, ctx):
        data = load_data()
        if not data:
            await ctx.send("No one is marked as away.")
            return
        msg = "**Away List:**\n"
        for user in data.values():
            msg += f"- {user['name']} until {user['until']} ({user['reason']})\n"
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(Away(bot))
