import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Подключение когов
bot.load_extension("cogs.away")

@bot.event
async def on_ready():
    print(f"{bot.user.name} connected.")

bot.run(TOKEN)