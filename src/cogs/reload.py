import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Literal

bot = commands.Bot(command_prefix="&", intents=discord.Intents.all())


class reload(
    commands.Cog,
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="reload", description="Reloads a Cog Class")
    async def reload(
        self, interaction: discord.Interaction, cog: Literal["warn", "info"],
    ):
        ctx = await self.bot.get_context(interaction)
        try:
            await bot.reload_extension(name="Cogs." + cog.lower())
            await ctx.send(f"Successfully reloaded **{cog}.py**")
        except Exception as e:
            await ctx.send(
                f"Failed! Could not reload this cog class. See error below\n```{e}```"
            )


async def setup(bot):
    await bot.add_cog(reload(bot))
    print("reload cog geladen ✔️")
