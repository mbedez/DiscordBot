import os
from commandes import Morpion
from commandes import Random
from commandes import Delete
from commandes import Help
from commandes import Sondage
from commandes import LolAccount
from commandes import Shifumi
from commandes import Motus
from abc import ABC

from discord.ext.commands import Bot, MissingRequiredArgument
from discord import Intents

from dotenv import load_dotenv

load_dotenv(dotenv_path="config")

COGS = [Morpion, Random, Delete, Help, Sondage, LolAccount, Shifumi, Motus]


class DocBot(Bot, ABC):
    def __init__(self):
        super().__init__(command_prefix="&", help_command=None, intents=Intents().all())

        for cog in COGS:
            cog.setup(self)
            print(f"Loading cog : {cog}")

    async def on_ready(self):
        print(" ")
        print(f"{self.user.display_name} est connecté au serveur.")
        print(" ")

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, MissingRequiredArgument):
            await ctx.send("Il manque au moins un paramètre. (&help)")
        else:
            pass


bot = DocBot()


@bot.command(name='ping')
async def ping(message):
    await message.channel.send("pong")


bot.run(os.getenv("TOKEN_TEST"))
