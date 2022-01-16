from discord.ext.commands import Cog
from discord.ext.commands import command


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='help')
    async def helping(self, ctx):
        await ctx.channel.send("&delete n : supprime n messages\n"
                               "&random n : génère un nombre entre 1 et n\n"
                               "&morpion @member : lance une partie de morpion avec @member\n"
                               "&poll a b c : écrit a et lance un sondage entre b et c\n")


def setup(bot):
    bot.add_cog(Help(bot))
