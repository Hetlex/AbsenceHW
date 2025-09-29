# cogs/suggests.py
import discord
from discord.ext import commands
from views.suggests_selects import SuggestMenu
from utils.storage import load_suggests, save_suggests
from datetime import datetime

class Suggest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="suggest")
    async def suggest(self, ctx: commands.Context):
        """Оставить предложение (через меню категорий)"""
        view = SuggestMenu()
        await ctx.send("📌 Выберите категорию для вашего предложения:", view=view)

    @commands.command(name="suggestlist")
    async def suggestlist(self, ctx: commands.Context):
        """Посмотреть список предложений"""
        suggests = load_suggests()
        if not suggests:
            await ctx.send("📭 Пока предложений нет.")
            return

        # Отправляем пачкой по 20 полей, чтобы не выйти за лимит embed
        embed = discord.Embed(title="📋 Список предложений", color=discord.Color.blue())
        for i, s in enumerate(suggests, start=1):
            author = s.get("author", s.get("user", "Unknown"))
            category = s.get("category", "—")
            text = s.get("text", "[пусто]")
            time = s.get("time", "—")
            embed.add_field(
                name=f"#{i} от {author} ({category})",
                value=f"{text} *(добавлено {time})*",
                inline=False
            )

            if len(embed.fields) >= 20:
                await ctx.send(embed=embed)
                embed = discord.Embed(title="📋 Список предложений (продолжение)", color=discord.Color.blue())

        # отправляем остаток
        await ctx.send(embed=embed)

    @commands.command(name="suggestclear")
    @commands.has_permissions(administrator=True)
    async def suggestclear(self, ctx: commands.Context):
        """Очистить список предложений (только админ)"""
        save_suggests([])
        await ctx.send("🗑️ Все предложения были очищены.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Suggest(bot))
