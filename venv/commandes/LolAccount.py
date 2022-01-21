from discord.ext.commands import Cog
from discord.ext.commands import command

import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path="config")
RIOT_KEY = (os.getenv("RIOT_KEY"))


class LolAccount(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='lolaccount')
    async def lol_account(self, ctx, summoner_name):
        summoner_name = str(summoner_name)
        url = str(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={RIOT_KEY}")
        response = requests.get(url)
        responsejson = response.json()
        lvl = str(responsejson["summonerLevel"])
        id_lol = str(responsejson["id"])

        url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id_lol}?api_key={RIOT_KEY}"
        url = str(url)
        response = requests.get(url)
        responsejson = response.json()
        nb_of_ranks = len(responsejson)

        soloq_sentence = f"\n{summoner_name} n'est pas classé en soloq !\n"
        flex_sentence = f"\n{summoner_name} n'est pas classé en flex !\n"

        if nb_of_ranks == 1:
            if responsejson[0]["queueType"] == "RANKED_SOLO_5x5":
                palier_lol = str(responsejson[0]["tier"])
                division_lol = str(responsejson[0]["rank"])
                league_point_lol = str(responsejson[0]["leaguePoints"])
                wins_lol = responsejson[0]["wins"]
                losses_lol = responsejson[0]["losses"]
                winrate_sentence = "Pas de game, pas de winrate..."
                if wins_lol + losses_lol != 0:
                    winrate_lol = str((wins_lol / (wins_lol + losses_lol)) * 100)[0:5]
                    winrate_sentence = f" Soit un winrate de {winrate_lol}%"

                soloq_sentence = f"\n{summoner_name} est {palier_lol} {division_lol} {league_point_lol} lp en soloq !\n" \
                                 f"{summoner_name} a joué {wins_lol + losses_lol} games en soloq avec {wins_lol} wins "\
                                 f" et {losses_lol} loses.{winrate_sentence}\n"

            elif responsejson[0]["queueType"] == "RANKED_FLEX_SR":
                palier_lol = str(responsejson[0]["tier"])
                division_lol = str(responsejson[0]["rank"])
                league_point_lol = str(responsejson[0]["leaguePoints"])
                wins_lol = responsejson[0]["wins"]
                losses_lol = responsejson[0]["losses"]
                winrate_sentence = "Pas de game, pas de winrate..."
                if wins_lol + losses_lol != 0:
                    winrate_lol = str((wins_lol / (wins_lol + losses_lol)) * 100)[0:5]
                    winrate_sentence = f" Soit un winrate de {winrate_lol}%"

                flex_sentence = f"\n{summoner_name} est {palier_lol} {division_lol} {league_point_lol} lp en flex !\n" \
                                f"{summoner_name} a joué {wins_lol + losses_lol} games en flex avec {wins_lol} wins " \
                                f" et {losses_lol} loses.{winrate_sentence}\n"

        elif nb_of_ranks >= 2:

            if responsejson[0]["queueType"] == "RANKED_SOLO_5x5":
                i = 0
            elif responsejson[1]["queueType"] == "RANKED_SOLO_5x5":
                i = 1
            else:
                i = 2
            if i < 2:
                palier_lol = str(responsejson[i]["tier"])
                division_lol = str(responsejson[i]["rank"])
                league_point_lol = str(responsejson[i]["leaguePoints"])
                wins_lol = responsejson[i]["wins"]
                losses_lol = responsejson[i]["losses"]
                winrate_sentence = None
                if wins_lol + losses_lol != 0:
                    winrate_lol = str((wins_lol / (wins_lol + losses_lol)) * 100)[0:5]
                    winrate_sentence = f" Soit un winrate de {winrate_lol}%"

                soloq_sentence = f"\n{summoner_name} est {palier_lol} {division_lol} {league_point_lol} lp en soloq !\n" \
                                 f"{summoner_name} a joué {wins_lol + losses_lol} games en soloq avec {wins_lol} wins "\
                                 f" et {losses_lol} loses.{winrate_sentence}\n"

            if responsejson[0]["queueType"] == "RANKED_FLEX_SR":
                i = 0
            elif responsejson[1]["queueType"] == "RANKED_FLEX_SR":
                i = 1
            else:
                i = 2
            if i < 2:
                palier_lol = str(responsejson[i]["tier"])
                division_lol = str(responsejson[i]["rank"])
                league_point_lol = str(responsejson[i]["leaguePoints"])
                wins_lol = responsejson[i]["wins"]
                losses_lol = responsejson[i]["losses"]
                winrate_sentence = None
                if wins_lol + losses_lol != 0:
                    winrate_lol = str((wins_lol / (wins_lol + losses_lol)) * 100)[0:5]
                    winrate_sentence = f" Soit un winrate de {winrate_lol}%"

                flex_sentence = f"\n{summoner_name} est {palier_lol} {division_lol} {league_point_lol} lp en flex !\n" \
                                f"{summoner_name} a joué {wins_lol + losses_lol} games en flex avec {wins_lol} wins " \
                                f"et {losses_lol} loses.{winrate_sentence}\n"

        await ctx.channel.send(f"```\n__{summoner_name}__\n{summoner_name} est lvl {lvl} sur LoL !\n"
                               f"{soloq_sentence}{flex_sentence}```")


def setup(bot):
    bot.add_cog(LolAccount(bot))
