from discord.ext.commands import Cog
from discord.ext import commands
from discord.commands import slash_command

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="config")

AUTHORIZED_GUILDS = eval(str(os.getenv("AUTHORIZED_GUILDS"))).values()


class Shifumi(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=AUTHORIZED_GUILDS)
    @commands.guild_only()
    async def shifumi(self, ctx):

        messages = await ctx.channel.history(limit=1).flatten()
        await messages[0].delete()
        posted_message = await ctx.response.send_message("SHIFUMI")
        posted_message = await posted_message.original_response()
        await posted_message.add_reaction("🪨")
        await posted_message.add_reaction("🧾")
        await posted_message.add_reaction("✂️")


def setup(bot):
    bot.add_cog(Shifumi(bot))
