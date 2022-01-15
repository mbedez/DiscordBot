from datetime import datetime
from discord.ext.commands import Cog
from discord.ext.commands import command


class Delete(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        serv_nst_id = 505198106350977024
        serv_fc_id = 464811558048890880
        channel_hydra_id = 930914775829987388
        probot_id = 282859044593598464
        tom_id = 181092186228654082

        bool_tom = True
        bool_fc = False
        bool_nst = False

        if (message.author.id == tom_id  and bool_tom) or (message.channel.guild.id == serv_nst_id and
                                           message.channel.id != channel_hydra_id and
                                           message.author.id != probot_id and bool_nst) or \
                (message.channel.guild.id == serv_fc_id and bool_fc):
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
