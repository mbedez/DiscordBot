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
        # create an url to get info on summoner by summoner name
        url = str(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={RIOT_KEY}")
        response = requests.get(url)
        responsejson = response.json()
        lvl = str(responsejson["summonerLevel"])
        id_lol = str(responsejson["id"])

        soloq_sentence = f"\nPas classé !\n"
        flex_sentence = f"\nPas classé !\n"
        tft_duo_sentence = f"\nPas classé !\n"
        tft_sentence = f"\nPas classé !\n"

        # create an url to get info on summoner ranks by summoner id
        url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id_lol}?api_key={RIOT_KEY}"
        url = str(url)
        response = requests.get(url)
        responsejson = response.json()
        nb_of_ranks = len(responsejson)
        # if ranked in soloq or flex
        for j in range(3):
            if nb_of_ranks == j:
                for i in range(nb_of_ranks):
                    if responsejson[i]["queueType"] == "RANKED_SOLO_5x5":
                        soloq_sentence = await self.sentence_maker(responsejson, i)
                    elif responsejson[i]["queueType"] == "RANKED_FLEX_SR":
                        flex_sentence = await self.sentence_maker(responsejson, i)

        # create an url to get info on summoner tft rank by summoner id
        url = f"https://euw1.api.riotgames.com/tft/league/v1/entries/by-summoner/{id_lol}?api_key={RIOT_KEY}"
        url = str(url)
        response = requests.get(url)
        responsejson = response.json()
        nb_of_ranks = len(responsejson)
        await ctx.channel.send(f"```\n__{summoner_name}__\n{summoner_name} est lvl {lvl} sur LoL !\n\n"
                               f"\n__Soloq__{soloq_sentence}\n__Flex__{flex_sentence}\n```")

    @staticmethod
    async def sentence_maker(responsejson, i):
        palier_lol = str(responsejson[i]["tier"])
        division_lol = str(responsejson[i]["rank"])
        league_point_lol = str(responsejson[i]["leaguePoints"])
        wins_lol = responsejson[i]["wins"]
        losses_lol = responsejson[i]["losses"]
        nb_games = wins_lol + losses_lol
        winrate_sentence = f" {str((wins_lol / (wins_lol + losses_lol)) * 100)[0:5]}% winrate"

        return f"\n{palier_lol} {division_lol} {league_point_lol} lp\nA joué {nb_games} games, " \
               f"{wins_lol} wins/{losses_lol} loses.{winrate_sentence}\n"


def setup(bot):
    bot.add_cog(LolAccount(bot))
