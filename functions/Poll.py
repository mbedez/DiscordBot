from discord.ext.commands import Cog
from discord.ext import commands
from discord.commands import slash_command

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="config")

AUTHORIZED_GUILDS = eval(str(os.getenv("AUTHORIZED_GUILDS"))).values()


class Sondage(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=AUTHORIZED_GUILDS)
    @commands.guild_only()
    async def poll(self, ctx: commands.Context):

        messages = await ctx.channel.history(limit=1).flatten()
        await messages[0].add_reaction("🟩")
        await messages[0].add_reaction("🟥")

        await ctx.response.send_message(
                                    "Polled !", ephemeral=True)


def setup(bot):
    bot.add_cog(Sondage(bot))
