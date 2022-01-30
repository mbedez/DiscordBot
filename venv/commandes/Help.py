from discord.ext.commands import Cog
from discord.ext.commands import command


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='help')
    async def helping(self, ctx):
        await ctx.channel.send("**&random n** : génère un nombre entre 1 et **n**\n"
                               "**&dice (Optionnel : n)** : "
                               "génère un nombre entre 1 et 6 ( ou entre 1 et **n** avec n inférieur ou égal à 6)\n\n"
                               "**&lolaccount \"summoner_name\"** : affiche des statistiques sur le niveau et "
                               "les rangs du compte indiqué\n"
                               "**&histo \"summoner_name\" (Optionnel : n)** : affiche une suite d'emoji en fonction "
                               "des **n**  dernières games de l'invocateur\n\n"
                               "**&poll \"question\" \"first_option\" \"second_option\"** : "
                               "lance un sondage auquel tout le monde peut répondre\n\n"
                               "**&morpion @member** : lance une partie de morpion avec **@member**\n")


def setup(bot):
    bot.add_cog(Help(bot))
