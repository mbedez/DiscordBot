from discord.ext.commands import Cog
from random import randint
from discord.ext.commands import command


class Random(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name='random')
	async def random(self, ctx, value: int):
		result = randint(1, value)
		await ctx.channel.send(f"{result}")

	# dice is like random but only between 1 and 6 and respond only with emoji
	@command(name='dice')
	async def dice(self, ctx, value=6):
		result = randint(1, value)
		if 7 > value > 0:
			if result == 1:
				await ctx.channel.send(f"1️⃣")
			elif result == 2:
				await ctx.channel.send(f"2️⃣")
			elif result == 3:
				await ctx.channel.send(f"3️⃣")
			elif result == 4:
				await ctx.channel.send(f"4️⃣")
			elif result == 5:
				await ctx.channel.send(f"5️⃣")
			elif result == 6:
				await ctx.channel.send(f"6️⃣")
		elif value >= 7:
			await ctx.channel.send(f"Le dé doit comporter six faces ou moins.")
		elif value <= 0:
			await ctx.channel.send(f"Le dé doit comporter au moins une face.")


def setup(bot):
	bot.add_cog(Random(bot))