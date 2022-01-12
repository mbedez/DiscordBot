import sys
from datetime import datetime
from discord.ext.commands import Cog
from discord.ext.commands import command


class Delete(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_message(self, message):
		# 181092186228654082 -> Tom
		# 505198106350977024-> serveur nst "or message.channel.guild.id == 505198106350977024"
		if message.author.id == 181092186228654082 or (message.channel.guild.id == 505198106350977024 and message.channel.id != 930914775829987388 and message.author.id != 282859044593598464):
			messages = await message.channel.history(limit=1).flatten()
			f = open('sortie.txt', 'a')
			f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{str(message.author)}\n"
					f"{str(message.channel)}\n{str(message.content)}\n\n")
			f.close()
			await messages[0].delete()
			print(f"Message écrit par {str(message.author)} à {datetime.now().strftime('%H:%M:%S')} sur "
				  f"{str(message.channel)} : {str(message.content)}\n\n")

	@command(name='delete')
	async def delete(self, ctx, number_of_messages: int):
		messages = await ctx.channel.history(limit=number_of_messages + 1).flatten()

		for each_message in messages:
			await each_message.delete()


def setup(bot):
	bot.add_cog(Delete(bot))
