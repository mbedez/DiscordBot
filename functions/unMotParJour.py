from discord.ext.commands import Cog
from discord.ext.commands import command

from bs4 import BeautifulSoup
import urllib.parse
import urllib.request

class unMotParJour(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='mot')
    async def mot(self, ctx):
        url = "http://unmotparjour.fr/random/"

        html_content = urllib.request.urlopen(urllib.request.urlopen(url).url).read()
        soup = BeautifulSoup(html_content, 'html.parser')

        word = soup.find("h1", {"class": "entry-title"}).get_text()
        definition = soup.find("div", {"class": "entry-content"}).get_text()
        
        await ctx.channel.send(f"```{word}\n\n {definition}```")


def setup(bot):
	bot.add_cog(unMotParJour(bot))
