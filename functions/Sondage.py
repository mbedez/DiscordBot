from discord.ext.commands import Cog, command
from discord.ext import commands

class Sondage(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='poll')
    async def sondage(self, ctx: commands.Context):
        
        messages = await ctx.channel.history(limit=2).flatten()
        await messages[0].delete()
        await messages[1].add_reaction("🟩")
        await messages[1].add_reaction("🟥")


def setup(bot):
    bot.add_cog(Sondage(bot))
