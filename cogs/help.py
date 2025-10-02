import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="📖 What i can",
            color=discord.Color.blue()
        )
        embed.add_field(name="!away", value="Indicate the reason for absence", inline=False)
        embed.add_field(name="!suggest", value="Leave an offer", inline=False)
        embed.add_field(name="!getstats", value="Statistics for the season", inline=False)
        embed.add_field(name="!getstatsall", value="All-time statistics", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
