from discord.ext.commands import Cog
from discord.ext import commands
from discord.commands import slash_command

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="config")

AUTHORIZED_GUILDS = eval(str(os.getenv("AUTHORIZED_GUILDS"))).values()


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=AUTHORIZED_GUILDS)
    @commands.guild_only()
    async def help(self, ctx):
        await ctx.response.send_message(
            "**/random n** : génère un nombre entre 1 et **n**\n"

            "**/dice (Optionnel : n)** : génère un nombre "
            "( ou entre 1 et **n** avec n inférieur ou égal à 6)\n\n"


            "**/lolaccount \"summoner_name\"** : affiche "
            "des statistiques sur le niveau, "
            "les rangs et les aram du compte indiqué\n"

            "**/lolhisto \"summoner_name\" (Optionnel : n, "
            "Optionnel : type)** : affiche le résultats des n games "
            "(5 par défaut) de flex et soloq (ou du type "
            "précisé) de l'historique en emoji\n\n"


            "**/poll** : "
            "Ajoute des réactions 🟩 et 🟥 sur le message précédent\n\n"


            "**/shifumi** : "
            "Ajoute des réactions 🪨, 🧾 et ✂️ sur un message du bot\n\n"


            "**/play (url youtube ou recherche)** : "
            "Joue une musique sur le salon vocal actuel\n\n"

            "**/seek (timecode en s)** : "
            "Se déplace au timecode donné dans la musique en cours\n\n")


def setup(bot):
    bot.add_cog(Help(bot))
