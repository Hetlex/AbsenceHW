from discord.ext import commands
from views.main_menu import MainMenu
from utils.storage import load_data, save_data

class Away(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="away")
    async def away(self, ctx):
        view = MainMenu()
        await ctx.send("Please select your language / Пожалуйста, выберите язык:", view=view)

    @commands.command(name="awaylist")
    @commands.has_permissions(administrator=True)
    async def awaylist(self, ctx):
        data = load_data()
        if not data:
            await ctx.send("Away list is empty.")
            return

        msg = "**Away List:**\n"
        for user_id, user_entries in data.items():
            member = ctx.guild.get_member(int(user_id))
            for entry in user_entries:
                if member:
                    discord_name = f"{member.name}" if member else entry['name']
                    display_name = member.display_name if member else "Unknown"
                else:
                    discord_name = entry['name']
                    display_name = "Unknown"

                msg += (
                    f"- {discord_name} ({display_name}) | {entry['type']} | {entry['until']} "
                    f"({entry['reason']}) — ID: `{entry['id']}`\n"
                )

        chunks = [msg[i:i+1900] for i in range(0, len(msg), 1900)]
        for chunk in chunks:
            await ctx.send(chunk)

    @commands.command(name="awayremove")
    @commands.has_permissions(administrator=True)
    async def awayremove(self, ctx, record_id: str):
        data = load_data()
        found = False

        for uid in list(data.keys()):
            original_len = len(data[uid])
            data[uid] = [entry for entry in data[uid] if entry.get("id") != record_id]
            if len(data[uid]) < original_len:
                found = True
                # Удалить юзера если у него больше нет записей
                if not data[uid]:
                    del data[uid]
                break

        if found:
            save_data(data)
            await ctx.send(f"Record with ID `{record_id}` removed.")
        else:
            await ctx.send(f"No record with ID `{record_id}` found.")

    @awaylist.error
    async def awaylist_error(self, ctx, error):
        await ctx.send("Permission denied.")

    @awayremove.error
    async def awayremove_error(self, ctx, error):
        await ctx.send("Usage: `!awayremove <id>` or permission denied.")

async def setup(bot):
    await bot.add_cog(Away(bot))
