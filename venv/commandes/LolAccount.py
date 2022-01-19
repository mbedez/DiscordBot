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
        url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={RIOT_KEY}"
        url = str(url)
        response = requests.get(url)
        responsejson = response.json()
        lvl = str(responsejson["summonerLevel"])
        print(lvl)
        id_lol = str(responsejson["id"])

        url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id_lol}?api_key={RIOT_KEY}"
        url = str(url)
        response = requests.get(url)
        responsejson = response.json()

        palier_lol = str(responsejson[0]["tier"])
        division_lol = str(responsejson[0]["rank"])
        league_point_lol = str(responsejson[0]["leaguePoints"])
        wins_lol = responsejson[0]["wins"]
        losses_lol = responsejson[0]["losses"]
        winrate_sentence = None
        if wins_lol+losses_lol != 0:
            winrate_lol = (wins_lol/(wins_lol+losses_lol))*100
            print(winrate_lol)
            winrate_lol = str(winrate_lol)
            print(winrate_lol)
            winrate_lol = winrate_lol[0:5]
            print(winrate_lol)
            winrate_sentence = f" Soit un winrate de {winrate_lol}%"

        await ctx.channel.send(f"```__{summoner_name}__\n{summoner_name} est lvl {lvl} sur LoL !\n"
                               f"{summoner_name} est {palier_lol} {division_lol} {league_point_lol} lp en soloq !\n"
                               f"{summoner_name} a joué {wins_lol+losses_lol} games en soloq avec {wins_lol} wins et "
                               f"{losses_lol} loses.{winrate_sentence}```")


def setup(bot):
    bot.add_cog(LolAccount(bot))
