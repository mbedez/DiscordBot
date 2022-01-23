import discord
from discord.ext.commands import Cog, command
from discord.ext import commands
from discord.ui import Button, View
from discord import Member


class Shifumi(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='shifumi')
    async def shifumi(self, ctx: commands.Context, guest: Member):
        print("coucou")

        button1 = Button(emoji="🪨", style=discord.ButtonStyle.success)
        button2 = Button(emoji="🧾", style=discord.ButtonStyle.success)
        button3 = Button(emoji="✂️", style=discord.ButtonStyle.success)

        view = View(timeout=300)
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)

        await ctx.send(f"{str(ctx.author)[:-5]} invite {guest.name} à jouer au shifumi !", view=view)

        choice_author = None
        choice_guest = None

        async def button_callback1(interaction, choice_author=choice_author, choice_guest=choice_guest):
            if str(ctx.author) == str(interaction.user):
                print(choice_author)
                choice_author = "pierre"
                print("choix auteur :", choice_author)
                print(str(interaction.user)[:-5])
            elif guest.id == interaction.user.id:
                choice_guest = "pierre"
                print("choix invité :", choice_guest)

            if choice_author != None and choice_guest != None:
                print("je")
                if choice_guest != choice_author:
                    print("suis")
                    await interaction.response.edit_message(content=f"todo")
                else:
                    print("là")
                    await interaction.response.edit_message(content="Égalité !")

        async def button_callback2(interaction):
            print("coucou")

        async def button_callback3(interaction):
            print("coucou")

        button1.callback = button_callback1
        button2.callback = button_callback2
        button2.callback = button_callback2


def setup(bot):
    bot.add_cog(Shifumi(bot))
