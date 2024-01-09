import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

# https://gist.github.com/InterStella0/b78488fb28cadf279dfd3164b9f0cf96


class MyHelp(commands.HelpCommand):
    # &help
    async def send_bot_help(self, mapping):
        await self.context.send(
            "\n You can *warn* a *User*, with the */warn command*. You **dont have to give a reason**.\nYou can check how many infractions a user has with the */info command*.\n \n Gday. "
        )
