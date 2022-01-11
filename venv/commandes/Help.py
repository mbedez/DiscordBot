import discord
from discord.ext.commands import Cog
from discord.ext import commands
from discord.ext.commands import command



class Help(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name='help')
	async def helping(self, ctx):
		await ctx.channel.send("&ping : renvoie pong\n&delete x : supprime x messages\n"
							   "&random x : génère un nombre entre 1 et x\n&haitrixx : s'excuse pour le spam\n"
							   "&morpion : essaye de jouer au morpion, en vain")


def setup(bot):
    bot.add_cog(Help(bot))

