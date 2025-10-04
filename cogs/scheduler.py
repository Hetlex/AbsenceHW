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
        self.check_time.start()

    def cog_unload(self):
        self.check_time.cancel()

    @tasks.loop(minutes=1)
    async def check_time(self):
        now = datetime.datetime.now(self.moscow_tz)

        if now.weekday() == 5 and now.hour == 22 and now.minute == 0:
            await self.send_reminder()
            await self.tier2_reminder()

        if now.weekday() == 6 and now.hour == 22 and now.minute == 0:
            await self.send_reminder()
            await self.tier2_reminder()

    async def send_reminder(self):
        channel = self.bot.get_channel(CHANNEL_ID)
        if channel:
            guild = channel.guild
            role = guild.get_role(ROLE_ID)
            if role:
                messages = [
                    f"{role.mention} Don't forget to play 5vs5!",
                    f"{role.mention} Make sure to finish your daily 5vs5 matches please!",
                    f"{role.mention} Team up with your friends and play 5vs5 for the future of our guild!"
                ]
                await channel.send(random.choice(messages))
    
    async def tier2_reminder(self):
        channel = self.bot.get_channel(TIER2_CHANNEL)
        if channel:
            guild = channel.guild
            role = guild.get_role(TIER2_ID)
            if role:
                messages = [
                    f"{role.mention} Time to get tier 3 in 5vs5!",
                    f"{role.mention} 5vs5 time, can you reach tier 3 today?",
                    f"{role.mention} 5vs5, the road to tier 3 is open!"
                ]
                await channel.send(random.choice(messages))

async def setup(bot):
    await bot.add_cog(Scheduler(bot))

