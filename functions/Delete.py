from discord.ext.commands import Cog
from discord.ext.commands import command


class Delete(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='supp')
    async def delete_messages(self, ctx, number_of_messages: int):
        """unreferenced command without security that can delete n message"""
        messages = await ctx.channel.history(
            limit=number_of_messages + 1).flatten()

        for each_message in messages:
            await each_message.delete()


def setup(bot):
    bot.add_cog(Delete(bot))
