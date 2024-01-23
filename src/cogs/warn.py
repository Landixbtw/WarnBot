import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from dateutil.relativedelta import relativedelta
import mariadb
import sys


bot = commands.Bot(command_prefix="&", intents=discord.Intents.all())


class warn(
    commands.Cog,
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="warn", description="Warn a user, with or without a reason given." )
    @app_commands.default_permissions(manage_roles=True)
    @app_commands.describe(warn="user name or ID of whom to warn")
    @app_commands.describe(reason="The reason for the warn")
    async def warn_user(
        self, interaction: discord.Interaction, warn: discord.Member, reason: str = None
    ):
        if interaction.user == bot.user:
            return
            
        guild = interaction.guild
        warn_one = discord.utils.get(guild.roles, name="1. WARN")
        warn_two = discord.utils.get(guild.roles, name="2. WARN")
        warn_three = discord.utils.get(guild.roles, name="3. WARN")

        try:
            
            try:
                con = mariadb.connect(
                user="ole",
                password="QrsoL82",
                host="192.168.10.183",
                port=3306,
                database="WarnDB",
            )


                # Get Cursor
                cur = con.cursor()
                
            except mariadb.Error as e:
                print(f"Error connecting to MariaDB Platform: {e}")
                sys.exit(1)
            
            
            true_id_list = []
            with open("src/guild_id/member_ids.xml", "w") as file:
                for member in guild.members:
                    file.write(str(member.id) + "\n")
                    true_id_list.append(member.id)

            with open("src/guild_id/member_ids.xml", "r") as file:
                lines = file.readlines()
                for line in lines:
                    true_id = int(line.strip())

            # print(f'this is reason: {reason}')
            # print('----------------------------')
            # #print(f'this is user: {user}')
            # print(f'this is true_id: {type(true_id)} »» {true_id}')
            # print('----------------------------')
            # print(f'this is interaction name: {interaction.user.name}')
            # print('----------------------------')
            # print(f'this is interaction id: {type(interaction.user.id)} »» {interaction.user.id}' )
            # print('----------------------------')
            # print(f'this is warn: {type(warn)} »» {warn}')
            # print('----------------------------')
            # print(f'this is warn id: {type(warn.id)} »» {warn.id}')
            # print('----------------------------')
            # now = datetime.now()# ausgestellt am
            # print(f'this is now: {type(now)} »» {now.strftime("%Y-%m-%d %H:%M:%S")}')

            DATA = []
            DATA.append(interaction.user.name)  # warn ausgestellt von
            DATA.append(interaction.user.id)  # id
            DATA.append(str(warn))  # warn ausgestellt an
            DATA.append(warn.id)  # id

            if warn_three in warn.roles:
                await interaction.response.send_message(
                    f"Du kannst {warn} nicht mehr verwarnen, da drei warns vorhanden sind."
                )

            if not warn_one in warn.roles:
                await warn.add_roles(warn_one)
            if warn_one in warn.roles:
                await warn.add_roles(warn_two)
            if warn_two in warn.roles:
                await warn.add_roles(warn_three)
                        
            if reason == None:
                await interaction.response.send_message(
                    f"**{interaction.user.name}** warned user {warn}, with reason : N/A"
                )
                DATA.append("N/A")  # warn grund
            else:
                DATA.append(reason)
            if reason != None:
                await interaction.response.send_message(
                    f"**{interaction.user.name}** warned user {warn}, with reason: {reason}",
                )

            now = datetime.now()
            DATA.append(now.strftime("%Y-%m-%d %H:%M:%S"))  # ausgestellt am

            cur.execute(
                "INSERT INTO warns(WARN_AUSGESTELLT_VON , ID_ONE , WARN_AUSGESTELLT_AN , ID_TWO ,WARN_GRUND , AUSGESTELLT_AM ) VALUES ( ?, ?, ?,  ?, ?, ?)",
                (DATA),
            )
            con.commit()
            
            print(
                f"{interaction.user.name} | {interaction.user.id} has warned user {warn}"
            )

        except ValueError:
            await interaction.response.send_message(f"Invalid user ID provided: {warn}")
        
        finally: 
            con.close()

async def setup(bot):
    await bot.add_cog(warn(bot))
    print("warn cog geladen ✔️")
