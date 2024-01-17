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
    async def reload(interaction: discord.Interaction, cog: Literal["warn", "Cog2"]):
        try:
            await bot.reload_extension(name="Cogs." + cog.lower())
            await interaction.response.send_message(f"Successfully reloaded **{cog}.py**")
        except Exception as e:
            await interaction.response.send_message(
                f"Failed! Could not reload this cog class. See error below\n```{e}```"
            )
            
            
async def setup(bot):
    await bot.add_cog(reload(bot))
    print("warn cog geladen ✔️")
