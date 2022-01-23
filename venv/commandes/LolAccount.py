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

        soloq_sentence = f"\n__Soloq__\nPas classé !\n"
        flex_sentence = f"\n__Flex__\nPas classé !\n"
        tft_sentence = f"\n__TFT__\nPas classé !\n"

        if nb_of_ranks == 1:
            if responsejson[0]["queueType"] == "RANKED_SOLO_5x5":
                soloq_sentence = await self.soloq_sentence_maker(responsejson, 0)

            elif responsejson[0]["queueType"] == "RANKED_FLEX_SR":
                flex_sentence = await self.flex_sentence_maker(responsejson, 0)

            elif responsejson[0]["queueType"] == "TFT":
                tft_sentence = await self.tft_sentence_maker(responsejson, 0)

        elif nb_of_ranks == 2:
            if responsejson[0]["queueType"] == "RANKED_SOLO_5x5":
                soloq_sentence = await self.soloq_sentence_maker(responsejson, 0)
            elif responsejson[1]["queueType"] == "RANKED_SOLO_5x5":
                soloq_sentence = await self.soloq_sentence_maker(responsejson, 1)

            if responsejson[0]["queueType"] == "RANKED_FLEX_SR":
                flex_sentence = await self.flex_sentence_maker(responsejson, 0)
            elif responsejson[1]["queueType"] == "RANKED_FLEX_SR":
                flex_sentence = await self.flex_sentence_maker(responsejson, 1)

            if responsejson[0]["queueType"] == "TFT":
                tft_sentence = await self.tft_sentence_maker(responsejson, 0)
            elif responsejson[1]["queueType"] == "TFT":
                tft_sentence = await self.tft_sentence_maker(responsejson, 1)

        elif nb_of_ranks == 3:
            if responsejson[0]["queueType"] == "RANKED_SOLO_5x5":
                soloq_sentence = await self.soloq_sentence_maker(responsejson, 0)
            elif responsejson[1]["queueType"] == "RANKED_SOLO_5x5":
                soloq_sentence = await self.soloq_sentence_maker(responsejson, 1)
            elif responsejson[2]["queueType"] == "RANKED_SOLO_5x5":
                soloq_sentence = await self.soloq_sentence_maker(responsejson, 2)

            if responsejson[0]["queueType"] == "RANKED_FLEX_SR":
                flex_sentence = await self.flex_sentence_maker(responsejson, 0)
            elif responsejson[1]["queueType"] == "RANKED_FLEX_SR":
                flex_sentence = await self.flex_sentence_maker(responsejson, 1)
            elif responsejson[2]["queueType"] == "RANKED_FLEX_SR":
                flex_sentence = await self.flex_sentence_maker(responsejson, 2)

            if responsejson[0]["queueType"] == "TFT":
                tft_sentence = await self.tft_sentence_maker(responsejson, 0)
            elif responsejson[1]["queueType"] == "TFT":
                tft_sentence = await self.tft_sentence_maker(responsejson, 1)
            elif responsejson[2]["queueType"] == "TFT":
                tft_sentence = await self.tft_sentence_maker(responsejson, 2)

        await ctx.channel.send(f"```\n__{summoner_name}__\n{summoner_name} est lvl {lvl} sur LoL !\n\n"
                               f"{soloq_sentence}{flex_sentence}{tft_sentence}```")

    @staticmethod
    async def soloq_sentence_maker(responsejson, i):
        palier_lol = str(responsejson[i]["tier"])
        division_lol = str(responsejson[i]["rank"])
        league_point_lol = str(responsejson[i]["leaguePoints"])
        wins_lol = responsejson[i]["wins"]
        losses_lol = responsejson[i]["losses"]
        winrate_sentence = None
        if wins_lol + losses_lol != 0:
            winrate_lol = str((wins_lol / (wins_lol + losses_lol)) * 100)[0:5]
            winrate_sentence = f" Soit un winrate de {winrate_lol}%"

        return f"\n__Soloq__\n{palier_lol} {division_lol} {league_point_lol} lp\n" \
               f"A joué {wins_lol + losses_lol} games, " \
               f"{wins_lol} wins/{losses_lol} loses.{winrate_sentence}\n"

    @staticmethod
    async def flex_sentence_maker(responsejson, i):
        palier_lol = str(responsejson[i]["tier"])
        division_lol = str(responsejson[i]["rank"])
        league_point_lol = str(responsejson[i]["leaguePoints"])
        wins_lol = responsejson[i]["wins"]
        losses_lol = responsejson[i]["losses"]
        winrate_sentence = None
        if wins_lol + losses_lol != 0:
            winrate_lol = str((wins_lol / (wins_lol + losses_lol)) * 100)[0:5]
            winrate_sentence = f" Soit un winrate de {winrate_lol}%"

        return f"\n__Flex__\n{palier_lol} {division_lol} {league_point_lol} lp\n" \
               f"A joué {wins_lol + losses_lol} games, " \
               f"{wins_lol} wins/{losses_lol} loses.{winrate_sentence}\n"

    @staticmethod
    async def tft_sentence_maker(responsejson, i):
        palier_lol = str(responsejson[i]["tier"])
        division_lol = str(responsejson[i]["rank"])
        league_point_lol = str(responsejson[i]["leaguePoints"])
        wins_lol = responsejson[i]["wins"]
        losses_lol = responsejson[i]["losses"]
        winrate_sentence = None
        if wins_lol + losses_lol != 0:
            winrate_lol = str((wins_lol / (wins_lol + losses_lol)) * 100)[0:5]
            winrate_sentence = f" Soit un winrate de {winrate_lol}%"

        return f"\n__TFT__\n{palier_lol} {division_lol} {league_point_lol} lp\n" \
               f"A joué {wins_lol + losses_lol} games, " \
               f"{wins_lol} wins/{losses_lol} loses.{winrate_sentence}\n"


def setup(bot):
    bot.add_cog(LolAccount(bot))
