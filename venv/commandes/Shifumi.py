import discord
from discord.ext.commands import Cog, command
from discord.ext import commands
from discord.ui import Button, View
from discord import Member


class Shifumi(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.choice_author = None
        self.choice_guest = None

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

        async def button_callback1(interaction):
            if str(ctx.author) == str(interaction.user):
                print(self.choice_author)
                self.choice_author = "pierre"
                print("choix auteur :", self.choice_author)
                print(str(interaction.user)[:-5])
            elif guest.id == interaction.user.id:
                self.choice_guest = "pierre"
                print("choix invité :", self.choice_guest)

            if self.choice_author is not None and self.choice_guest is not None:
                if self.choice_guest != self.choice_author:
                    await interaction.response.edit_message(content=f"todo")
                else:
                    await interaction.response.edit_message(content="Égalité !")

        async def button_callback2(interaction):
            if str(ctx.author) == str(interaction.user):
                print(self.choice_author)
                self.choice_author = "feuille"
                print("choix auteur :", self.choice_author)
                print(str(interaction.user)[:-5])
            elif guest.id == interaction.user.id:
                self.choice_guest = "feuille"
                print("choix invité :", self.choice_guest)

            if self.choice_author is not None and self.choice_guest is not None:
                if self.choice_guest != self.choice_author:
                    await interaction.response.edit_message(content=f"todo")
                else:
                    await interaction.response.edit_message(content="Égalité !")

        async def button_callback3(interaction):
            print("coucou")

        button1.callback = button_callback1
        button2.callback = button_callback2
        button3.callback = button_callback3


def setup(bot):
    bot.add_cog(Shifumi(bot))
