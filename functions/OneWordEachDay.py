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
        definition = self.process_text(word + soup.find("div", {"class": "entry-content"}).get_text())

        data = {'content': f'```\n{definition}```'}
        
        requests.post(f'https://discord.com/api/v6/channels/{self.channel_id}/messages', headers=self.headers, json=data)
        
    def process_text(self, text):
        result = ''
        temp = ''
        previous_char = ''
        nb_n = 0
        uppercase_letters = ['A-', 'B-', 'C-', 'D-', 'E-']
        lowercase_letters = ['a-', 'b-', 'c-', 'd-', 'e-']
        numbers = ['1-', '2-', '3-', '4-', '5-']

        for char in text:
            # Remove consecutive spaces or consecutive newlines
            if (char == previous_char == ' ') or (char == '\n' and previous_char == '\n'): pass
            # Replace "«" and "»" with double quotes
            elif char in "«»": result += '"'
            # Remove spaces before newlines
            elif char == '\n' and previous_char == ' ': result = result[:-1] + char
            # Replace newlines with spaces if not at the end of a sentence
            elif char == '\n' and previous_char != '.': result += ' '
            # Keep the rest of the characters
            else: result += char
            # Store the previous character
            previous_char = char

        # Add a newline before each type of section (A-, 1-, a-, ...)
        for letter in uppercase_letters: result = result.replace(letter, '\n' + letter)
        for letter in lowercase_letters: result = result.replace(letter, '\n    ' + letter)
        for number in numbers:           result = result.replace(number, '\n  ' + number)

        # The following line removes extra newlines
        result = ''.join(char for i, char in enumerate(result) if i == 0 or char != '\n' or result[i-1] != '\n')
        
        # The following line adds a newline before each definition
        for letter in uppercase_letters: result = result.replace(letter, '\n' + letter)

        # Add a newline after the third consecutive newline
        temp = result
        result = ''
        for char in temp:
            if char == '\n':
                nb_n += 1
                result += char + '\n' if nb_n == 2 else char
            else: result += char

        return result

def setup(bot):
	bot.add_cog(unMotParJour(bot))
