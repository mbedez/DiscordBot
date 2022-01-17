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
        lvl = responsejson["summonerLevel"]
        lvl = str(lvl)
        await ctx.channel.send(f"{summoner_name} est lvl {lvl} sur LoL !")

def setup(bot):
    bot.add_cog(LolAccount(bot))
