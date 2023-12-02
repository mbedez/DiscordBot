import discord
from discord.ext.commands import Cog
from discord.ext import commands
from discord.commands import slash_command

import os
from dotenv import load_dotenv
import requests
import datetime

from PIL import Image, ImageDraw, ImageFont

load_dotenv(dotenv_path="config")

RIOT_KEY = (os.getenv("RIOT_KEY"))
AUTHORIZED_GUILDS = eval(str(os.getenv("AUTHORIZED_GUILDS"))).values()


class LolAccount(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lolAccountFields = {'nameField': (1057, 310),
                                 'levelField': (2544, 324),
                                 'soloqGamesField': (644, 1180),
                                 'soloqRankField': (644, 1729),
                                 'soloqPointsField': (644, 1829),
                                 'soloqRatioField': (644, 2340),
                                 'soloqWinrateField': (644, 2460),
                                 'flexGamesField': (1512, 1180),
                                 'flexRankField': (1512, 1729),
                                 'flexPointsField': (1512, 1829),
                                 'flexRatioField': (1512, 2340),
                                 'flexWinrateField': (1512, 2460),
                                 'aramGamesField': (2392, 1180),
                                 'aramLastGameDayField': (2392, 1729),
                                 'aramLastGameHourField': (2392, 1810)}

    @slash_command(guild_ids=AUTHORIZED_GUILDS)
    @commands.guild_only()
    async def lolaccount(self, ctx, summoner_name):
        """Send recap of LoL account."""

        # Open an image and editing it
        template = Image.open('assets/template.png')
        draw = ImageDraw.Draw(template)

        # create an url to get info on summoner by summoner name
        responsejson = await self.id_taker(str(summoner_name))
        lvl = str(responsejson["summonerLevel"])
        id_lol = str(responsejson["id"])

        # create an url to get info on summoner ranks by summoner id
        url = (f"https://euw1.api.riotgames.com/lol"
               f"/league/v4/entries/by-summoner/{id_lol}?api_key={RIOT_KEY}")
        response = requests.get(url)
        responsejson = response.json()
        nb_of_ranks = len(responsejson)

        soloq_palier_lol = soloq_division_lol = ' '
        flex_palier_lol = flex_division_lol = ' '

        soloq_league_point_lol = flex_league_point_lol = '0'
        soloq_nb_of_games = flex_nb_of_games = '0'
        soloq_losses_lol = soloq_wins_lol = '0'
        flex_wins_lol = flex_losses_lol = '0'

        soloq_winrate = flex_winrate = 4*' ' + '0'

        # if ranked in soloq or flex
        for i in range(nb_of_ranks):
            if responsejson[i]["queueType"] == "RANKED_SOLO_5x5":
                soloq_palier_lol = str(responsejson[i]["tier"])
                soloq_division_lol = str(responsejson[i]["rank"])
                soloq_league_point_lol = str(responsejson[i]["leaguePoints"])
                soloq_wins_lol = responsejson[i]["wins"]
                soloq_losses_lol = responsejson[i]["losses"]
                soloq_winrate = str(
                    int(soloq_wins_lol) * 100 /
                    (int(soloq_wins_lol) + int(soloq_losses_lol)))
                soloq_nb_of_games = int(soloq_wins_lol) + int(soloq_losses_lol)

            elif responsejson[i]["queueType"] == "RANKED_FLEX_SR":
                flex_palier_lol = str(responsejson[i]["tier"])
                flex_division_lol = str(responsejson[i]["rank"])
                flex_league_point_lol = str(responsejson[i]["leaguePoints"])
                flex_wins_lol = responsejson[i]["wins"]
                flex_losses_lol = responsejson[i]["losses"]
                flex_winrate = str(int(flex_wins_lol) * 100 /
                                   (int(flex_wins_lol) + int(flex_losses_lol)))
                flex_nb_of_games = int(flex_wins_lol) + int(flex_losses_lol)

        responsejson = await self.id_taker(summoner_name)
        summoner_PUUID = str(responsejson["puuid"])

        start = str(0)
        url = (f"https://europe.api.riotgames.com/lol"
               f"/match/v5/matches/by-puuid/{summoner_PUUID}/ids?queue=450"
               f"&start={start}&count=100&api_key={RIOT_KEY}")

        responsejson = requests.get(url).json()
        all_aram = len(responsejson)

        last_aram = last_aram_date = 6*' '

        last_aram_date = ""
        if len(responsejson) != 0:
            last_aram = await self.match_info_taker(responsejson[0])
            last_aram_date = int(last_aram["info"]["gameCreation"])
            last_aram_date = datetime.datetime.fromtimestamp(
                             last_aram_date/1000).strftime(
                                '%Y-%m-%d %H:%M:%S')[:-3]

        while len(responsejson) == 100:
            start = int(start)
            start += 100
            start = str(start)

            url = (f"https://europe.api.riotgames.com/lol"
                   f"/match/v5/matches/by-puuid/{summoner_PUUID}/ids?queue=450"
                   f"&start={start}&count=100&api_key={RIOT_KEY}")
            responsejson = requests.get(url).json()
            all_aram += len(responsejson)

        myFont = ImageFont.truetype('./fonts/lolAccountFont.ttf', 250)

        _, _, r, b = draw.textbbox((0, 0), summoner_name, font=myFont)
        draw.text((self.lolAccountFields["nameField"][0]-r/2,
                   self.lolAccountFields["nameField"][1]-b/2),
                  summoner_name,
                  font=myFont,
                  fill=('#c5c5c5'))

        _, _, r, b = draw.textbbox((0, 0), lvl, font=myFont)
        draw.text((self.lolAccountFields["levelField"][0]-r/2,
                   self.lolAccountFields["levelField"][1]-b/2),
                  lvl,
                  font=myFont,
                  fill=('#c5c5c5'))

        myFont = ImageFont.truetype('./fonts/lolAccountFont.ttf', 200)

        _, _, r, b = draw.textbbox((0, 0), str(soloq_nb_of_games), font=myFont)
        draw.text((self.lolAccountFields["soloqGamesField"][0]-r/2,
                   self.lolAccountFields["soloqGamesField"][1]-b/2),
                  str(soloq_nb_of_games),
                  font=myFont,
                  fill=('#c5c5c5'))

        _, _, r, b = draw.textbbox((0, 0), str(flex_nb_of_games), font=myFont)
        draw.text((self.lolAccountFields["flexGamesField"][0]-r/2,
                   self.lolAccountFields["flexGamesField"][1]-b/2),
                  str(flex_nb_of_games),
                  font=myFont,
                  fill=('#c5c5c5'))

        _, _, r, b = draw.textbbox((0, 0), str(all_aram), font=myFont)
        draw.text((self.lolAccountFields["aramGamesField"][0]-r/2,
                   self.lolAccountFields["aramGamesField"][1]-b/2),
                  str(all_aram),
                  font=myFont,
                  fill=('#c5c5c5'))

        myFont = ImageFont.truetype('./fonts/lolAccountFont.ttf', 100)

        _, _, r, b = draw.textbbox((0, 0),
                                   f'{soloq_palier_lol} {soloq_division_lol}',
                                   font=myFont)
        draw.text((self.lolAccountFields["soloqRankField"][0]-r/2,
                   self.lolAccountFields["soloqRankField"][1]-b/2),
                  f'{soloq_palier_lol} {soloq_division_lol}',
                  font=myFont,
                  fill=('#c5c5c5'))

        _, _, r, b = draw.textbbox((0, 0),
                                   f'{flex_palier_lol} {flex_division_lol}',
                                   font=myFont)
        draw.text((self.lolAccountFields["flexRankField"][0]-r/2,
                   self.lolAccountFields["flexRankField"][1]-b/2),
                  f'{flex_palier_lol} {flex_division_lol}',
                  font=myFont,
                  fill=('#c5c5c5'))

        _, _, r, b = draw.textbbox((0, 0),
                                   last_aram_date[:-6],
                                   font=myFont)
        draw.text((self.lolAccountFields["aramLastGameDayField"][0]-r/2,
                   self.lolAccountFields["aramLastGameDayField"][1]-b/2),
                  last_aram_date[:-6],
                  font=myFont,
                  fill=('#c5c5c5'))

        _, _, r, b = draw.textbbox((0, 0),
                                   f'{str(soloq_league_point_lol)} lp',
                                   font=myFont)
        draw.text((self.lolAccountFields["soloqPointsField"][0]-r/2,
                   self.lolAccountFields["soloqPointsField"][1]-b/2),
                  f'{str(soloq_league_point_lol)} lp',
                  font=myFont,
                  fill=('#c5c5c5'))

        _, _, r, b = draw.textbbox((0, 0),
                                   f'{str(flex_league_point_lol)} lp',
                                   font=myFont)
        draw.text((self.lolAccountFields["flexPointsField"][0]-r/2,
                   self.lolAccountFields["flexPointsField"][1]-b/2),
                  f'{str(flex_league_point_lol)} lp',
                  font=myFont,
                  fill=('#c5c5c5'))

        _, _, r, b = draw.textbbox((0, 0), last_aram_date[-5:], font=myFont)
        draw.text((self.lolAccountFields["aramLastGameHourField"][0]-r/2,
                   self.lolAccountFields["aramLastGameHourField"][1]-b/2),
                  last_aram_date[-5:],
                  font=myFont,
                  fill=('#c5c5c5'))

        _, _, r, b = draw.textbbox((0, 0),
                                   f'{soloq_wins_lol}W/{soloq_losses_lol}L',
                                   font=myFont)
        draw.text((self.lolAccountFields["soloqRatioField"][0]-r/2,
                   self.lolAccountFields["soloqRatioField"][1]-b/2),
                  f'{soloq_wins_lol}W/{soloq_losses_lol}L',
                  font=myFont,
                  fill=('#c5c5c5'))

        _, _, r, b = draw.textbbox((0, 0),
                                   f'{flex_wins_lol}W/{flex_losses_lol}L',
                                   font=myFont)
        draw.text((self.lolAccountFields["flexRatioField"][0]-r/2,
                   self.lolAccountFields["flexRatioField"][1]-b/2),
                  f'{flex_wins_lol}W/{flex_losses_lol}L',
                  font=myFont,
                  fill=('#c5c5c5'))

        _, _, r, b = draw.textbbox((0, 0),
                                   f'{soloq_winrate[:5]}%',
                                   font=myFont)
        draw.text((self.lolAccountFields["soloqWinrateField"][0]-r/2,
                   self.lolAccountFields["soloqWinrateField"][1]-b/2),
                  f'{soloq_winrate[:5]}%',
                  font=myFont,
                  fill=('#c5c5c5'))

        _, _, r, b = draw.textbbox((0, 0), f'{flex_winrate[:5]}%', font=myFont)
        draw.text((self.lolAccountFields["flexWinrateField"][0]-r/2,
                   self.lolAccountFields["flexWinrateField"][1]-b/2),
                  f'{flex_winrate[:5]}%',
                  font=myFont,
                  fill=('#c5c5c5'))

        template.save('assets/LolAccount.png')

        await ctx.response.send_message(
            file=discord.File('assets/LolAccount.png'))

    @slash_command(guild_ids=AUTHORIZED_GUILDS)
    @commands.guild_only()
    async def lolhisto(self, ctx, summoner_name, nb_game=5, type_queue="all"):
        """Send the histo of the summoner."""

        if not 0 < nb_game < 30:
            nb_game = 30
        summoner_name = str(summoner_name)

        responsejson = await self.id_taker(summoner_name)
        puuid_lol = str(responsejson["puuid"])
        histo_lol = await self.histo_taker(puuid_lol, type_queue)

        posted_message = await ctx.response.send_message(
            "```Recherche en cours...```")

        message = "```"

        if nb_game > len(histo_lol):
            nb_game = len(histo_lol)
        for i in range(nb_game):
            await posted_message.edit_original_response(
                content=f"```Récupération de la game {i+1}```")
            match_lol = await self.match_info_taker(histo_lol[nb_game-i-1])
            j = 0
            while match_lol["info"]["participants"][j]["puuid"] != puuid_lol:
                j = j+1

            kda = (f"{match_lol['info']['participants'][j]['kills']}/"
                   f"{match_lol['info']['participants'][j]['deaths']}/"
                   f"{match_lol['info']['participants'][j]['assists']}")

            kda = kda.ljust(8)

            championName = (
                f"{match_lol['info']['participants'][j]['championName']}")

            if (((match_lol["info"])["participants"])[j])["win"]:
                message = f"{message}🟩 {kda} {championName}\n"
            elif not (((match_lol["info"])["participants"])[j])["win"]:
                message = f"{message}🟥 {kda} {championName}\n"
        message = f"{message}```"

        await posted_message.edit_original_response(
            content="```Analyse des games...```")

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

        await posted_message.edit_original_response(content=message)
        posted_message = await posted_message.original_response()

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
    async def id_taker(summoner_name):
        url = str(f"https://euw1.api.riotgames.com"
                  f"/lol/summoner/v4/summoners/by-name/"
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
            url = str(f"https://europe.api.riotgames.com"
                      f"/lol/match/v5/matches/by-puuid/"
                      f"{puuid}/ids?queue={queueId}&type=ranked"
                      f"&start=0&count=30&api_key={RIOT_KEY}")
        else:
            url = str(f"https://europe.api.riotgames.com"
                      f"/lol/match/v5/matches/by-puuid/"
                      f"{puuid}/ids?type=ranked"
                      f"&start=0&count=30&api_key={RIOT_KEY}")

        responsejson = requests.get(url).json()
        return responsejson

    @staticmethod
    async def match_info_taker(match_id):
        url = (f"https://europe.api.riotgames.com"
               f"/lol/match/v5/matches/{match_id}?api_key={RIOT_KEY}")
        responsejson = requests.get(url).json()
        return responsejson


def setup(bot):
    bot.add_cog(LolAccount(bot))
