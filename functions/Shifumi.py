from discord.ext.commands import Cog, command


class Shifumi(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='shifumi')
    async def shifumi(self, ctx):

        messages = await ctx.channel.history(limit=1).flatten()
        await messages[0].delete()
        posted_message = await ctx.channel.send("SHIFUMI")
        await posted_message.add_reaction("🪨")
        await posted_message.add_reaction("🧾")
        await posted_message.add_reaction("✂️")


def setup(bot):
    bot.add_cog(Shifumi(bot))
