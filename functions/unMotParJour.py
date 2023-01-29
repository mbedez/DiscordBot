from discord.ext.commands import Cog
from discord.ext.commands import command

from bs4 import BeautifulSoup
import urllib.parse
import urllib.request

import requests
import os

import threading
import datetime
import time

class unMotParJour(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.started = False
        print("init")

        if not self.started:
            t = threading.Thread(target=self.randomUnMotParJour)
            t.start()
            self.started = True     

    def randomUnMotParJour(self):
        print("function")
        # headers for discord api
        headers = {'Authorization': f'Bot {os.getenv("TOKEN")}'}

        # channel i want send message
        channel_id = '1055154215820984391'

        while True:
            current_time = datetime.datetime.now()
            
            if current_time.hour == 19 and current_time.minute == 0:  # execute at 20:00 (UTC+1)

                url = "http://unmotparjour.fr/random/"

                html_content = urllib.request.urlopen(urllib.request.urlopen(url).url).read()
                soup = BeautifulSoup(html_content, 'html.parser')

                word = soup.find("h1", {"class": "entry-title"}).get_text()
                definition = soup.find("div", {"class": "entry-content"}).get_text()

                data = {'content': f'```\n{word}\n {definition}```'}
                
                requests.post(f'https://discord.com/api/v6/channels/{channel_id}/messages', headers=headers, json=data)

            time.sleep(60)
        


def setup(bot):
	bot.add_cog(unMotParJour(bot))
