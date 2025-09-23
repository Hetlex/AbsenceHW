import discord
from discord.ext import tasks, commands
import datetime
import pytz
import random

CHANNEL_ID = 1420024438165999697    
ROLE_ID = 1359579356300578907          

class Scheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.moscow_tz = pytz.timezone("Europe/Moscow")
        self.check_time.start()

    def cog_unload(self):
        self.check_time.cancel()

    @tasks.loop(minutes=1)
    async def check_time(self):
        now = datetime.datetime.now(self.moscow_tz)

        
        if now.weekday() == 5 and now.hour == 22 and now.minute == 0:
            await self.send_reminder()

        
        if now.weekday() == 6 and (now.hour == 5 or now.hour == 22) and now.minute == 0:
            await self.send_reminder()

        
        if now.weekday() == 0 and now.hour == 5 and now.minute == 0:
            await self.send_reminder()

    import random

    async def send_reminder(self):
        channel = self.bot.get_channel(CHANNEL_ID)
        if channel:
            guild = channel.guild
            role = guild.get_role(ROLE_ID)
            if role:
                messages = [
                    f"{role.mention} Don't forget to play 5vs5! You need to reach tier 3!",
                    f"{role.mention} Make sure to finish your daily 5vs5 matches please!",
                    f"{role.mention} Team up with your friends and try to reach tier 3 for the future of our guild!"
                ]
                await channel.send(random.choice(messages))

