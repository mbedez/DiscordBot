from discord.ext.commands import Cog
from discord.ext.commands import command


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='help')
    async def helping(self, ctx):
        await ctx.channel.send("&delete n : supprime n messages\n&random x : génère un nombre entre 1 et x\n"
                               "&morpion : essaye de jouer au morpion, en vain\n"
                               " TODO : &poll a b : lance un sondage entre a et b")


def setup(bot):
    bot.add_cog(Help(bot))
