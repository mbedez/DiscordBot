from discord.ext.commands import Cog

from bs4 import BeautifulSoup
import urllib.parse
import urllib.request

import requests
import os

from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class unMotParJour(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = os.getenv("CHANNEL_MOTS")
        self.url = "http://unmotparjour.fr/random/"
        self.headers = {'Authorization': f'Bot {os.getenv("TOKEN")}'}
        self.scheduler = AsyncIOScheduler(timezone="Europe/Paris")
        self._add_job = self.scheduler.add_job(self.getMot, CronTrigger(hour=20,minute=0,second=0))
        self.scheduler.start()

    def getMot(self):
        html_content = urllib.request.urlopen(urllib.request.urlopen(self.url).url).read()
        soup = BeautifulSoup(html_content, 'html.parser')

        word = soup.find("h1", {"class": "entry-title"}).get_text()
        definition = soup.find("div", {"class": "entry-content"}).get_text()

        data = {'content': f'```\n{word}\n {definition}```'}
        
        requests.post(f'https://discord.com/api/v6/channels/{self.channel_id}/messages', headers=self.headers, json=data)
        

def setup(bot):
	bot.add_cog(unMotParJour(bot))
