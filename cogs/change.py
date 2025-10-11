import discord
from discord.ext import commands
from utils.storage import connect_sheet

EXCLUDED_IDS = {"hetlex", "kosh4tina", "legenda_1111", "quxy"}

class SyncNick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="syncnick")
    async def syncnick(self, ctx, text_id: str):
        """Синхронизировать ник одного пользователя по text_id (колонка D)."""
        await self._sync_single(ctx, text_id)

    @commands.command(name="syncall")
    @commands.has_permissions(administrator=True)
    async def syncall(self, ctx):
        """Синхронизировать ники всех пользователей из таблицы, кроме исключений."""
        try:
            sheet = connect_sheet()
            all_values = sheet.get_all_values()

            if not all_values or len(all_values[0]) < 4:
                await ctx.send("⚠️ Таблица пуста или неверный формат данных.")
                return

            updated = 0
            not_found = []
            skipped = []
            excluded = []

            for row in all_values[1:]:
                if len(row) < 4:
                    continue

                text_id = row[3].strip().lower()
                new_nick = row[1].strip() if len(row) > 1 else None

                if not text_id or not new_nick:
                    skipped.append(text_id or "(пусто)")
                    continue

                # Исключённые пользователи
                if text_id in EXCLUDED_IDS:
                    excluded.append(text_id)
                    continue

                member = discord.utils.find(
                    lambda m: m.name.lower() == text_id or (m.nick and m.nick.lower() == text_id),
                    ctx.guild.members
                )

                if member:
                    try:
                        await member.edit(nick=new_nick)
                        updated += 1
                    except discord.Forbidden:
                        skipped.append(text_id)
                    except Exception as e:
                        print(f"Ошибка при обновлении ника {text_id}: {e}")
                else:
                    not_found.append(text_id)

            report = (
                f"✅ Обновлено никнеймов: **{updated}**\n"
                f"🚫 Пропущено (исключения): {', '.join(excluded) if excluded else '—'}\n"
                f"❌ Не найдено на сервере: {', '.join(not_found) if not_found else '—'}\n"
                f"⚠️ Ошибки или пустые строки: {', '.join(skipped) if skipped else '—'}"
            )

            await ctx.send(report)

        except Exception as e:
            await ctx.send(f"❌ Ошибка при синхронизации: `{e}`")

    async def _sync_single(self, ctx, text_id: str):
        """Вспомогательная функция — синхронизирует ник одного пользователя."""
        try:
            text_id_lower = text_id.lower()
            if text_id_lower in EXCLUDED_IDS:
                await ctx.send(f"🚫 `{text_id}` находится в списке исключений. Пропускаю.")
                return

            sheet = connect_sheet()
            all_values = sheet.get_all_values()

            if not all_values or len(all_values[0]) < 4:
                await ctx.send("⚠️ В таблице нет нужных данных.")
                return

            found_row = None
            for row in all_values[1:]:
                if len(row) > 3 and row[3].strip().lower() == text_id_lower:
                    found_row = row
                    break

            if not found_row:
                await ctx.send(f"❌ Не найден `{text_id}` в колонке D.")
                return

            new_nick = found_row[1].strip()
            member = discord.utils.find(
                lambda m: m.name.lower() == text_id_lower or (m.nick and m.nick.lower() == text_id_lower),
                ctx.guild.members
            )

            if not member:
                await ctx.send(f"❌ Не найден `{text_id}` на сервере.")
                return

            await member.edit(nick=new_nick)
            await ctx.send(f"✅ Ник {member.mention} изменён на **{new_nick}**.")

        except discord.Forbidden:
            await ctx.send("⚠️ У бота нет прав менять ники.")
        except Exception as e:
            await ctx.send(f"❌ Ошибка при обновлении ника: `{e}`")

async def setup(bot):
    await bot.add_cog(SyncNick(bot))
