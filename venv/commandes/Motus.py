from discord.ext.commands import Cog
from discord.ext.commands import command


class Motus(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        nb_try = 0
        if str(message.channel.type) == 'private':
            if str(message.content)[:5] == 'motus':
                premier_passage = 1
                async for message in message.channel.history(limit=30):
                    if message.author.id == message.channel.me.id and premier_passage == 1:
                        premier_passage = 0
                        if message.content[:7] == "Essai 5":
                            await message.channel.send("Essai 6 :")
                        elif message.content[:7] == "Essai 4":
                            await message.channel.send("Essai 5 :")
                        elif message.content[:7] == "Essai 3":
                            await message.channel.send("Essai 4 :")
                        elif message.content[:7] == "Essai 2":
                            await message.channel.send("Essai 3 :")
                        elif message.content[:7] == "Essai 1":
                            await message.channel.send("Essai 2 :")
                        elif message.content[:7] == "Début d":
                            await message.channel.send("Essai 1 :")
                            nb_try = 0
                        else:
                            await message.channel.send("Début de la partie :\nE \_ \_ \_ \_ \_ \_ \_")

                print(message.content)
                print(str(message.content))


def setup(bot):
    bot.add_cog(Motus(bot))
