from discord.ext.commands import Cog
from discord.ext.commands import command


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='help')
    async def helping(self, ctx):
        await ctx.channel.send("**&random n** : génère un nombre entre 1 et n\n"
                               "**&morpion @member** : lance une partie de morpion avec @member\n"
                               "**&poll 'question' 'first_option' 'second_option'** : "
                               "lance un sondage auquel tout le monde peut répondre\n"
                               "**&lolaccount 'summoner_name'** : affiche des statistiques sur le niveau et "
                               "les rangs du compte donné en paramètre")


def setup(bot):
    bot.add_cog(Help(bot))
