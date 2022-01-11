from discord.ext.commands import Cog
from discord.ext.commands import command


class Delete(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_message(self, message):
		# 181092186228654082 -> Tom
		# 505198106350977024-> serveur nst "or message.channel.guild.id == 505198106350977024"
		if message.author.id == 181092186228654082 or message.channel.guild.id == 505198106350977024:
			messages = await message.channel.history(limit=1).flatten()
			print(message.author)
			print(message.channel)
			print(message.content)
			print("")
			for each_message in messages:
				await each_message.delete()

	@command(name='delete')
	async def delete(self, ctx, number_of_messages: int):
		messages = await ctx.channel.history(limit=number_of_messages + 1).flatten()

		for each_message in messages:
			await each_message.delete()


def setup(bot):
	bot.add_cog(Delete(bot))
