import discord
from discord.ext import commands
from utils import storage

class SheetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="getstats")
    async def get_stats(self, ctx):
        result = storage.get_user_stats(ctx.author.id)

        if not result:
            await ctx.send("❌ Твой Discord ID не найден в таблице.")
            return

        nickname, stats = result

        msg = f"🎮 Ник в игре: **{nickname}**\n"
        msg += "📊 Твоя статистика по неделям:\n"

        total = 0
        for week, value in stats.items():
            points = int(value) if value.isdigit() else 0
            total += points
            msg += f"**{week}:** {points}\n"

        msg += f"\n🏆 Итог: **{total}** поинтов"

        await ctx.send(msg)

# вот это важно!
async def setup(bot):
    await bot.add_cog(SheetCog(bot))

