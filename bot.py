import os
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} connected.")

async def setup():
    await bot.load_extension("cogs.away")  # теперь обязательно await
    await bot.start(TOKEN)

asyncio.run(setup())