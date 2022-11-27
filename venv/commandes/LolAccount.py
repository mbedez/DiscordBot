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
        responsejson = await self.id_taker(summoner_name)
        lvl = str(responsejson["summonerLevel"])
        id_lol = str(responsejson["id"])

        soloq_sentence = f"\nPas classé !\n"
        flex_sentence = f"\nPas classé !\n"

        # create an url to get info on summoner ranks by summoner id
        url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id_lol}?api_key={RIOT_KEY}"
        url = str(url)
        response = requests.get(url)
        responsejson = response.json()
        nb_of_ranks = len(responsejson)

        # if ranked in soloq or flex
        for i in range(nb_of_ranks):
            if responsejson[i]["queueType"] == "RANKED_SOLO_5x5":
                soloq_sentence = await self.sentence_maker(responsejson, i)
            elif responsejson[i]["queueType"] == "RANKED_FLEX_SR":
                flex_sentence = await self.sentence_maker(responsejson, i)

        await ctx.channel.send(f"```\n__{summoner_name}__\n{summoner_name} est lvl {lvl} sur LoL !\n\n"
                               f"\n__Soloq__{soloq_sentence}\n__Flex__{flex_sentence}\n```")

    @command(name='lolhisto')
    async def lolhisto(self, ctx, summoner_name, nb_game=5, type_queue="all"):
        if not 0 < nb_game < 30:
            nb_game = 30
        summoner_name = str(summoner_name)

        responsejson = await self.id_taker(summoner_name)
        puuid_lol = str(responsejson["puuid"])
        histo_lol = await self.histo_taker(puuid_lol, type_queue)

        posted_message = await ctx.channel.send("```Recherche en cours...```")

        message = "```"

        if nb_game > len(histo_lol):
            nb_game = len(histo_lol)
        for i in range(nb_game):
            await posted_message.edit(content=f"```Récupération de la game {i+1}```")
            match_lol = await self.match_info_taker(histo_lol[nb_game-i-1])
            j = 0
            while (((match_lol["info"])["participants"])[j])["puuid"] != puuid_lol:
                j = j+1

            kda = f"{match_lol['info']['participants'][j]['kills']}/{match_lol['info']['participants'][j]['deaths']}/" \
                  f"{match_lol['info']['participants'][j]['assists']}"
            championName=f"{match_lol['info']['participants'][j]['championName']}"

            if(((match_lol["info"])["participants"])[j])["win"]:
                message = f"{message}🟩 {kda} {championName}\n"
            elif not (((match_lol["info"])["participants"])[j])["win"]:
                message = f"{message}🟥 {kda} {championName}\n"
        message = f"{message}```"

        await posted_message.edit(content=f"```Analyse des games...```")

        max_lose_streak = 0
        max_win_streak = 0

        win_streak = 0
        lose_streak = 0
        for character in message:
            if character == "🟩":
                win_streak += 1
                if win_streak > max_win_streak:
                    max_win_streak = win_streak
                lose_streak = 0
            elif character == "🟥":
                lose_streak += 1
                if lose_streak > max_lose_streak:
                    max_lose_streak = lose_streak
                win_streak = 0

        await posted_message.edit(content=message)

        if 6 <= max_win_streak:
            await posted_message.add_reaction("🥵")
        elif 4 <= max_win_streak < 6:
            await posted_message.add_reaction("😎")
        elif 3 <= max_win_streak < 4:
            await posted_message.add_reaction("☺")
        if 6 <= max_lose_streak:
            await posted_message.add_reaction("💀")
        elif 4 <= max_lose_streak < 6:
            await posted_message.add_reaction("😱")
        elif 3 <= max_lose_streak < 4:
            await posted_message.add_reaction("😖")

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

    @staticmethod
    async def id_taker(summoner_name):
        url = str(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
                  f"{summoner_name}?api_key={RIOT_KEY}")
        responsejson = requests.get(url).json()
        return responsejson

    @staticmethod
    async def histo_taker(puuid, type):
        # 420 queueId = soloq, 440 queueId = flex
        if type == "soloq" or type == "flex":
            if type == "soloq":
                queueId = 420
            else:
                queueId = 440
            url = str(f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/"
                      f"{puuid}/ids?queue={queueId}&type=ranked&start=0&count=30&api_key={RIOT_KEY}")
        else:
            url = str(f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/"
                      f"{puuid}/ids?type=ranked&start=0&count=30&api_key={RIOT_KEY}")

        responsejson = requests.get(url).json()
        return responsejson

    @staticmethod
    async def match_info_taker(match_id):
        url = str(f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={RIOT_KEY}")
        responsejson = requests.get(url).json()
        return responsejson


def setup(bot):
    bot.add_cog(LolAccount(bot))
