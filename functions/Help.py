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

                               "**&lolhisto \"summoner_name\" (Optionnel : n, Optionnel : type)** : "
                               "affiche le résultats des n games "
                               "(5 par défaut) de flex et soloq (ou du type précisé) de l'historique en emoji\n"

                               "**&lolaram \"summoner_name\"** : "
                               "affiche le nombre d'aram de l'invocateur et la date de sa dernière aram\n\n"


                               "**&poll \"question\" \"first_option\" \"second_option\"** : "
                               "lance un sondage auquel tout le monde peut répondre\n\n"
                               
                               "**&morpion @member** : lance une partie de morpion avec **@member**\n")


def setup(bot):
    bot.add_cog(Help(bot))
