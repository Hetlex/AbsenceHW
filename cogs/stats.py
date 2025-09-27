import discord
from discord.ext import commands
from utils import storage

class StatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="getstats")
    async def get_stats(self, ctx):
        """Показывает статистику пользователя на последнем листе"""
        result = storage.get_user_stats_by_nick(ctx.author)

        if not result:
            await ctx.send("❌ Твой ник не найден в таблице.")
            return

        nickname, stats = result
        msg = f"🎮 Ник в игре: **{nickname}**\n"
        msg += "📊 Твоя статистика по неделям:\n"

        total = 0
        for week, value in stats.items():
            points = int(value) if str(value).isdigit() else 0
            total += points
            msg += f"**{week}:** {points}\n"

        msg += f"\n🏆 Итог: **{total}** поинтов"
        await ctx.send(msg)

    @commands.command(name="getstatsall")
    async def get_stats_all(self, ctx):
        """
        Собирает статистику пользователя по всем листам, но ник берёт с последнего листа.
        """
        results = storage.get_user_stats_all(ctx.author)

        if not results:
            await ctx.send("❌ Твой ник не найден ни на одной вкладке.")
            return

        # Берём ник с последнего листа
        last_sheet_name = list(results.keys())[-1]
        nickname, _ = results[last_sheet_name]

        msg = f"🎮 Ник в игре: **{nickname}**\n"
        grand_total = 0

        for sheet_name, (_, stats) in results.items():
            msg += f"\n📊 Статистика на листе **{sheet_name}**:\n"
            total = 0
            for week, value in stats.items():
                points = int(value) if str(value).isdigit() else 0
                total += points
            grand_total += total
            msg += ", ".join(f"**{week}: {int(value) if str(value).isdigit() else 0}**" for week, value in stats.items())
            msg += f"\n🏆 Итог за сезон: **{total}** поинтов\n"

        msg += f"\n💎 Общий итог по всем сезонам: **{grand_total}** поинтов"
        await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(StatsCog(bot))
