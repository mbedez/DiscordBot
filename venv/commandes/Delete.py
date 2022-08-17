from datetime import datetime
from discord.ext.commands import Cog
from discord.ext.commands import command

import time
from random import randint

class Delete(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.id_victime = 0
        self.id_serveur_cible = 0
        self.delete_activation = True
        self.delete_max = 15
        self.delete_min = 1

    @Cog.listener()
    async def on_message(self, message):
<<<<<<< HEAD
        if (message.author.id == self.id_victime and message.channel.guild.id == self.id_serveur_cible and
                self.delete_activation == True) :
            messages = await message.channel.history(limit=1).flatten()
            f = open('sortie.txt', 'a')
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{str(message.author)}\n"
                    f"{str(message.channel)}\n{str(message.content)}\n\n")
            f.close()
            time.sleep(randint(self.delete_min, self.delete_max))
            await messages[0].delete()
            '''print(f"Message écrit par {str(message.author)} à {datetime.now().strftime('%H:%M:%S')} sur "
                  f"{str(message.channel)} : {str(message.content)}\n\n")'''
=======
        serv_nst_id = 505198106350977024
        serv_fc_id = 464811558048890880
        channel_hydra_id = 930914775829987388
        probot_id = 282859044593598464
        tom_id = 181092186228654082
        bool_tom = True
        bool_fc = False
        bool_nst = False

        if str(message.channel.type) != 'private':

            if (message.author.id == tom_id and bool_tom) or (message.channel.guild.id == serv_nst_id and
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
>>>>>>> 1a0b73c914591def4e3981df18baecb8c24306e5

    # unreferenced command without security that can delete n message
    @command(name='deI')
    async def deI(self, ctx, number_of_messages: int):
        messages = await ctx.channel.history(limit=number_of_messages + 1).flatten()

        for each_message in messages:
            await each_message.delete()

    @command(name='set_id_serv')
    async def set_id_serv(self, ctx, id_serveur_cible: int):
        self.id_serveur_cible = id_serveur_cible
        await ctx.channel.send(f"Le serveur ciblé porte l'id {self.id_serveur_cible}")

    @command(name='set_id_victime')
    async def set_id_victime(self, ctx, id_victime: int):
        self.id_victime = id_victime
        await ctx.channel.send(f"La victime porte l'id {self.id_victime}")

    @command(name='delete_activation')
    async def delete_activation(self, ctx):
        if self.delete_activation == True :
            self.delete_activation = False
            await ctx.channel.send(f"La méthode delete est désactivée.")
        else :
            self.delete_activation = True
            await ctx.channel.send(f"La méthode delete est activée.")

    @command(name='get_id_serv')
    async def get_id_serv(self, ctx):
        await ctx.channel.send(f"505198106350977024")

    @command(name='set_delete_max')
    async def set_delete_max(self, ctx, max: int):
        self.delete_max = max
        await ctx.channel.send(f"La durée maximum avant suppression est de {self.delete_max}s.")

    @command(name='set_delete_min')
    async def set_delete_min(self, ctx, min: int):
        self.delete_min = min
        await ctx.channel.send(f"La durée minimum avant suppression est de {self.delete_min}s.")


def setup(bot):
    bot.add_cog(Delete(bot))
