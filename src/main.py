import discord
from discord.ext import commands
from discord import HTTPException, NotFound, app_commands
from dotenv import load_dotenv
from datetime import datetime
import mariadb
import os
import logging
from typing import Literal
import sys
from help import MyHelp


load_dotenv()
token = str(os.getenv("TOKEN"))

logs_dir = "./Logs"
if not os.path.exists(logs_dir):
    print("Made Logs Folder and file!")
    os.makedirs(logs_dir)
# Logging Handler to log info
handler = logging.FileHandler(filename="./Logs/discord.log", encoding="utf-8", mode="w")

id_dir = "./guild_id"
if not os.path.exists(id_dir):
    print("made xml folder")
    os.makedirs(id_dir)


class bot(commands.Bot):
    def __init__(
        self,
    ):
        super().__init__(command_prefix="#", intents=discord.Intents.all())

        self.cogList: list[str] = [
            "warn",
            # "IDwarn",
        ]

    async def setup_hook(self):
        print("loading cogs ...")

        for file in os.listdir(
            "./cogs"
        ):  # lists all the cog files inside the cog folder. (for raspberry /home/username/DBB/src/cogs)
            if file.endswith(".py"):  # It gets all the cogs that ends with a ".py".
                try:
                    name = file[:-3]  # It gets the name of the file removing the ".py"
                    await bot.load_extension(f"cogs.{name}")  # This loads the cog.
                except Exception as e:
                    print(f"error: {e}")

    async def on_ready(self):
        print(f"{bot.user.name} is ready to rumble!")
        print("Published by Moritz Henri Richard Reiswaffel III")
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} commands!")
        except Exception as e:
            print(e)
        # print(f'{discord.__version__}')
        print("------------------------------")
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name=f"{bot.command_prefix}help"
            )
        )


try:
    con = mariadb.connect(
        user="ole",
        password="QrsoL82",
        host="192.168.10.101",
        port=3306,
        database="BunnyDB",
    )

except mariadb.Error as mariaErr:
    print(f"Error connecting to MariaDB Platform: {mariaErr}")
    sys.exit(1)


cur = con.cursor()

cur.execute(
    "CREATE TABLE IF NOT EXISTS warns(WARN_AUSGESTELLT_VON TEXT, ID_ONE BIGINT, WARN_AUSGESTELLT_AN TEXT, ID_TWO BIGINT,WARN_GRUND TEXT, AUSGESTELLT_AM DATETIME)"
)
con.commit()
con.close

bot = bot()


@app_commands.command(name="reload", description="Reloads a Cog Class")
async def reload(interaction: discord.Interaction, cog: Literal["warn", "Cog2"]):
    try:
        await bot.reload_extension(name="Cogs." + cog.lower())
        await interaction.response.send_message(f"Successfully reloaded **{cog}.py**")
    except Exception as e:
        await interaction.response.send_message(
            f"Failed! Could not reload this cog class. See error below\n```{e}```"
        )


bot.help_command = MyHelp()
bot.run(token, log_handler=handler, reconnect=True)
