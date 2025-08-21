import os
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands
import logging

logging.basicConfig(level=logging.DEBUG)

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

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
        await bot.load_extension("cogs.away")
        await bot.load_extension("cogs.scheduler")
        await bot.start(TOKEN)
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")

asyncio.run(setup())