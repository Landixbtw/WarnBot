import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from dateutil.relativedelta import relativedelta
import mariadb
import sys
import logging


bot = commands.Bot(command_prefix="&", intents=discord.Intents.all())



class info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="info", description="Get Info about a user, e.g how many infractions")
    @app_commands.default_permissions(manage_roles=True)
    @app_commands.describe(user="who do you want info about")
    async def user_info(
        self, interaction: discord.Interaction, user: discord.Member
    ):  #
        try:
    
            try:
                con = mariadb.connect(
                user="ole",
                password="QrsoL82",
                host="192.168.10.183",
                port=3306,
                database="BunnyDB",
            )


                # Get Cursor
                cur = con.cursor()
                
            except mariadb.Error as e:
                print(f"Error connecting to MariaDB Platform: {e}")
                sys.exit(1)
                            
            
            cur.execute("SELECT ID_TWO FROM warns")
            all_id_two = cur.fetchall()
            sanitized_all_id_two = [str(x[0]) for x in all_id_two]


            cur.execute("SELECT WARN_GRUND FROM warns WHERE ID_TWO = ?", (user.id, ))
            infractions = cur.fetchall()
            print(infractions)
            
            con.commit()
            
            
            
            shorted_all_id = list(set(sanitized_all_id_two))

            
            infractions_list = [infraction[0] for infraction in infractions]
            infractions_str = "\n".join(infractions_list)
            
            if not str(user.id) in shorted_all_id:
                    embed = discord.Embed(
                        title=f"No Infractions Found for {user}",
                        description="This user has no infractions.",
                        color=0x00FF00,  # Green color for no infractions
                    )
                    await interaction.response.send_message(embed=embed)
            
            if str(user.id) in shorted_all_id:
                    embed = discord.Embed(
                        title=f"Infractions from {user}",
                        description=f"These are all infractions:\n{infractions_str}",
                        color=0xFF0000,
                    )
                    
                    await interaction.response.send_message(embed=embed)


        except Exception as err:
            logging.warning(err)

        finally: 
            con.close()

async def setup(bot):
    await bot.add_cog(info(bot))
    print("info cog geladen ✔️")
