import discord
from discord.ext import tasks, commands
import datetime
import pytz
import random

CHANNEL_ID = 1420024438165999697    
ROLE_ID = 135957935630057890
TIER2_ID = 1423056349222146108
TIER2_CHANNEL = 1423057474440663161         

class Scheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.moscow_tz = pytz.timezone("Europe/Moscow")
        self.check_time.start()  # запускаем цикл

    def cog_unload(self):
        self.check_time.cancel()

    @tasks.loop(minutes=1)
    async def check_time(self):
        await self.bot.wait_until_ready()  # ждём, пока бот полностью подключится
        now = datetime.datetime.now(self.moscow_tz)

        if now.weekday() in (5, 6) and now.hour == 22 and now.minute == 0:
            await self.send_reminder(CHANNEL_ID, ROLE_ID)
            await self.send_reminder(TIER2_CHANNEL, TIER2_ID)

    async def send_reminder(self, channel_id, role_id):
        channel = self.bot.get_channel(channel_id)
        if not channel:
            print(f"⚠️ Канал с ID {channel_id} не найден")
            return
        guild = channel.guild
        role = guild.get_role(role_id)
        if not role:
            print(f"⚠️ Роль с ID {role_id} не найдена")
            return

        messages = [
            f"{role.mention} Don't forget to play 5vs5!",
            f"{role.mention} Make sure to finish your daily 5vs5 matches please!",
            f"{role.mention} Team up with your friends and play 5vs5 for the future of our guild!"
        ]
        await channel.send(random.choice(messages))

async def setup(bot):
    await bot.add_cog(Scheduler(bot))
