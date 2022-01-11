from discord.ext.commands import Cog
from random import randint
from discord.ext.commands import command


class Random(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name='random')
	async def random(self, ctx, value: int):
		result = randint(1, value)
		if value < 7:
			if result == 1:
				await ctx.channel.send(f"1️⃣")
			if result == 2:
				await ctx.channel.send(f"2️⃣")
			if result == 3:
				await ctx.channel.send(f"3️⃣")
			if result == 4:
				await ctx.channel.send(f"4️⃣")
			if result == 5:
				await ctx.channel.send(f"5️⃣")
			if result == 6:
				await ctx.channel.send(f"6️⃣")
		if not value < 7:
			print(f"{result}")
			await ctx.channel.send(f"{result}")


def setup(bot):
	bot.add_cog(Random(bot))
