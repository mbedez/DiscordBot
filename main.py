import os
from dotenv import load_dotenv

from functions import Random, Delete, Help, Poll, \
     LolAccount, Shifumi, OneWordEachDay, Music, Vxtwitter

from abc import ABC

from discord.ext.commands import Bot, MissingRequiredArgument, TooManyArguments
from discord.ext import commands
from discord.commands import slash_command
from discord import Intents


load_dotenv(dotenv_path="config")

AUTHORIZED_GUILDS = eval(str(os.getenv("AUTHORIZED_GUILDS"))).values()
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


@slash_command(guild_ids=AUTHORIZED_GUILDS)
@commands.guild_only()
async def ping(message):
    """Send ping of the bot (should be between 95 and 110 ms)"""
    await message.channel.send(f"{round(bot.latency*1000)} ms")


bot.run(os.getenv("TOKEN"))
