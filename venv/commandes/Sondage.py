import discord
from discord.ext.commands import Cog, command
from discord.ext import commands
from discord.ui import Button, View


class Sondage(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='poll')
    async def sondage(self, ctx: commands.Context, question, proposition1, proposition2):
        call = await ctx.message.channel.history(limit=1).flatten()
        await call[0].delete()

        button1 = Button(label=f"{proposition1}", style=discord.ButtonStyle.success)
        button2 = Button(label=f"{proposition2}", style=discord.ButtonStyle.danger)

        view = View(timeout=None)
        view.add_item(button1)
        view.add_item(button2)
        await ctx.send(f"{question}", view=view)
        poll_message = await ctx.message.channel.history(limit=1).flatten()
        poll_id = poll_message[0].id

        async def button_callback1(interaction):
            utilisateur = str(interaction.user)
            post = f"🟩 {utilisateur}"
            histo = await ctx.message.channel.history(limit=50).flatten()
            first_reaction = True
            i = 0
            nb_vote_green = 0
            nb_vote_red = 0
            while histo[i].id != poll_id:
                if post[-2:] == histo[i].content[-2:]:
                    if post == histo[i].content:
                        await histo[i].delete()
                        first_reaction = False
                    else:
                        await histo[i].delete()
                i += 1
                if histo[i].content[-2:] == "🟩 ":
                    nb_vote_green += 1
                elif histo[i].content[-2:] == "🟥 ":
                    nb_vote_red += 1

            if first_reaction:
                await ctx.channel.send(post)
                nb_vote_green += 1

            if nb_vote_green + nb_vote_red != 0:
                percent = int((nb_vote_green / (nb_vote_green + nb_vote_red)) * 100)
            else:
                percent = "-"
            await interaction.response.edit_message(content=f"{question}                🟩 {nb_vote_green}  -  "
                                                    f"{nb_vote_red} 🟥         soit "
                                                    f"{percent}% 🟩")

        async def button_callback2(interaction):
            utilisateur = str(interaction.user)
            post = f"🟥 {utilisateur}"
            histo = await ctx.message.channel.history(limit=50).flatten()
            first_reaction = True
            i = 0
            nb_vote_green = 0
            nb_vote_red = 0
            while histo[i].id != poll_id:
                if post[-2:] == histo[i].content[-2:]:
                    if post == histo[i].content:
                        await histo[i].delete()
                        first_reaction = False
                    else:
                        await histo[i].delete()
                i += 1
                if histo[i].content[-2:] == "🟩 ":
                    nb_vote_green += 1
                elif histo[i].content[-2:] == "🟥 ":
                    nb_vote_red += 1

            if first_reaction:
                await ctx.channel.send(post)
                nb_vote_red += 1

            if nb_vote_green + nb_vote_red != 0:
                percent = int((nb_vote_green / (nb_vote_green + nb_vote_red)) * 100)
            else:
                percent = "-"
            await interaction.response.edit_message(content=f"{question}                🟩 {nb_vote_green}  -  "
                                                    f"{nb_vote_red} 🟥         soit "
                                                    f"{percent}% 🟩")

        button1.callback = button_callback1
        button2.callback = button_callback2


def setup(bot):
    bot.add_cog(Sondage(bot))
