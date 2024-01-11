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

logs_dir = "./src/Logs"
if not os.path.exists(logs_dir):
    print("Made Logs Folder and file!")
    os.makedirs(logs_dir)
# Logging Handler to log info
handler = logging.FileHandler(filename="./src/Logs/discord.log", encoding="utf-8", mode="w")

id_dir = "./src/guild_id"
if not os.path.exists(id_dir):
    print("made xml folder")
    os.makedirs(id_dir)


            
class bot(commands.Bot):
    def __init__(
        self,
    ):
        super().__init__(command_prefix="&", intents=discord.Intents.all())

        self.cogList: list[str] = [
            "warn",
            # "IDwarn",
        ]

    
    async def setup_hook(self):
        print("loading cogs ...")

        for file in os.listdir(
            "./src/cogs"
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
        
        async def role_check():
            for guild in bot.guilds:
                warn_one = discord.utils.get(guild.roles, name="1. WARN")
                warn_two = discord.utils.get(guild.roles, name="2. WARN")
                warn_three = discord.utils.get(guild.roles, name="3. WARN")
            
                if not all((warn_one, warn_two, warn_three)):
                    await guild.create_role(name="1. WARN", color=0xFF0000)
                    await guild.create_role(name="2. WARN", color=0xFF0000)
                    await guild.create_role(name="3. WARN", color=0xFF0000)
        
        await role_check()
        print('role check finished')
        
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
        

            
con.close()
bot.help_command = MyHelp()
bot.run(token, log_handler=handler)
