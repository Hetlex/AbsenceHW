import os
import asyncio
import discord
from discord.ext import commands
import logging


logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("❌ Не найдена переменная окружения ток!")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"{bot.user.name} connected.")

@bot.event
async def on_command_error(ctx, error):
    print(f"Ошибка в команде {ctx.command}: {error}")

@bot.event
async def on_error(event_method, *args, **kwargs):
    import traceback
    print(f"Ошибка в событии {event_method}:")
    traceback.print_exc()

async def setup():
    try:
        # Загружаем ваши cogs
        await bot.load_extension("cogs.away")
        await bot.load_extension("cogs.scheduler")
        await bot.load_extension("cogs.stats")
        await bot.load_extension("cogs.suggests")
        await bot.load_extension("cogs.help")
        await bot.start(TOKEN)
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")

asyncio.run(setup())
