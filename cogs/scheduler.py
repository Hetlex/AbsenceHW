import discord
from discord.ext import tasks, commands
import datetime
import pytz

CHANNEL_ID = 1359559397390549254    
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
        if now.weekday() in 5 and (now.hour == 22) and now.minute == 0:
            channel = self.bot.get_channel(CHANNEL_ID)
            if channel:
                guild = channel.guild
                role = guild.get_role(ROLE_ID)
                if role:
                    await channel.send(f"{role.mention} Don't forget to play 5vs5! You need to reach tier 3!")
        if now.weekday() in 6 and (now.hour == 5 and now.hour == 22) and now.minute == 00:
            channel = self.bot.get_channel(CHANNEL_ID)
            if channel:
                guild = channel.guild
                role = guild.get_role(ROLE_ID)
                if role:
                    await channel.send(f"{role.mention} Don't forget to play 5vs5! You need to reach tier 3!")
        if now.weekday() in 0 and now.hour == 5  and now.minute == 00:
            channel = self.bot.get_channel(CHANNEL_ID)
            if channel:
                guild = channel.guild
                role = guild.get_role(ROLE_ID)
                if role:
                    await channel.send(f"{role.mention} Don't forget to play 5vs5! You need to reach tier 3!")

async def setup(bot):
    await bot.add_cog(Scheduler(bot))
