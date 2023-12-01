from discord.ext import commands
from discord.ext.commands import Cog
from discord.commands import slash_command

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="config")

AUTHORIZED_GUILDS = eval(str(os.getenv("AUTHORIZED_GUILDS"))).values()


class Vxtwitter(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=AUTHORIZED_GUILDS)
    @commands.guild_only()
    async def vxtwitter(self, ctx, *, url):
        """Send the url with vxtwitter integration."""
        if "//twitter.com" in url:
            vxtwitter_url = url.replace("//twitter.com", "//vxtwitter.com")
        elif "//x.com" in url:
            vxtwitter_url = url.replace("//x.com", "//vxtwitter.com")
        else:
            vxtwitter_url = url
        await ctx.response.send_message(f"{vxtwitter_url}")


def setup(bot):
    bot.add_cog(Vxtwitter(bot))
