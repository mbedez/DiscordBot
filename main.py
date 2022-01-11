import os
from commandes import Morpion
from commandes import Random
from commandes import Delete
from commandes import Help
from commandes import Sondage
from abc import ABC

import discord
# from discord.ext.commands import command
from discord.ext.commands import Bot
from discord.ui import Button, View
from discord import Intents

from dotenv import load_dotenv

load_dotenv(dotenv_path="config")

COGS = [Morpion, Random, Delete, Help, Sondage]


class DocBot(Bot, ABC):
    def __init__(self):
        super().__init__(command_prefix="&", help_command=None, intents=Intents().all())

        for cog in COGS:
            cog.setup(self)
            print(f"Loading cog : {cog}")

    async def on_ready(self):
        print(f"{self.user.display_name} est connecté au serveur.")


bot = DocBot()


@bot.command(name='ping')
async def ping(message):
    await message.channel.send("pong")



bot.run(os.getenv("TOKEN"))
