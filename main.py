import os

from functions import Random, Delete, Help, Poll, \
     LolAccount, Shifumi, OneWordEachDay, Music, Vxtwitter

from abc import ABC

from discord.ext.commands import Bot, MissingRequiredArgument, TooManyArguments
from discord import Intents
from dotenv import load_dotenv

load_dotenv(dotenv_path="config")

COGS = [
    Random, Delete, Help, Poll, LolAccount, Shifumi,
    OneWordEachDay, Music, Vxtwitter
]


class DocBot(Bot, ABC):
    def __init__(self):
        super().__init__(command_prefix="&",
                         help_command=None,
                         intents=Intents().all())

        for cog in COGS:
            cog.setup(self)
            print(f"Loading cog : {cog}")

    async def on_ready(self):
        print(f"\n{self.user.display_name} est connecté au serveur.\n")

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, MissingRequiredArgument):
            await ctx.send("Il manque au moins un paramètre. (&help)")
        elif isinstance(exc, TooManyArguments):
            await ctx.send("Il a trop de paramètres. (&help)")
        else:
            pass


bot = DocBot()


@bot.command(name='ping')
async def ping(message):
    await message.channel.send(f"{round(bot.latency*1000)} ms")


bot.run(os.getenv("TOKEN"))
