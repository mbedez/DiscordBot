import discord
from discord.ext.commands import Cog
from discord.ext import commands
from discord.ext.commands import command


class Sondage(Cog):
	def __init__(self, bot):
		self.bot = bot



def setup(bot):
    bot.add_cog(Sondage(bot))

