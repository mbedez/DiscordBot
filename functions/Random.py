from discord.ext.commands import Cog
from discord.ext import commands
from discord.commands import slash_command

from random import randint

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="config")

AUTHORIZED_GUILDS = eval(str(os.getenv("AUTHORIZED_GUILDS"))).values()


class Random(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=AUTHORIZED_GUILDS)
    @commands.guild_only()
    async def random(self, ctx, value: int):
        """Send random number between 1 and value."""

        result = randint(1, value)
        await ctx.response.send_message(f"{result}")

    @slash_command(guild_ids=AUTHORIZED_GUILDS)
    @commands.guild_only()
    async def dice(self, ctx, value=6):
        """dice is like random but only between 1 and 6 with emoji"""

        value = int(value)
        result = randint(1, value)
        if 7 > value > 0:
            if result == 1:
                await ctx.response.send_message("1️⃣")
            elif result == 2:
                await ctx.response.send_message("2️⃣")
            elif result == 3:
                await ctx.response.send_message("3️⃣")
            elif result == 4:
                await ctx.response.send_message("4️⃣")
            elif result == 5:
                await ctx.response.send_message("5️⃣")
            elif result == 6:
                await ctx.response.send_message("6️⃣")
        elif value >= 7:
            await ctx.response.send_message(
                "Le dé doit comporter six faces ou moins.")
        elif value <= 0:
            await ctx.response.send_message(
                "Le dé doit comporter au moins une face.")


def setup(bot):
    bot.add_cog(Random(bot))
