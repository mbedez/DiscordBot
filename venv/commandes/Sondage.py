import discord
from discord.ext.commands import Cog, command
from discord.ext import commands
from discord.ui import Button, View


class Sondage(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='poll')
    async def sondage(self, ctx: commands.Context, question, proposition1, proposition2):
        button1 = Button(label=f"{proposition1}", style=discord.ButtonStyle.success)
        button2 = Button(label=f"{proposition2}", style=discord.ButtonStyle.danger)

        view = View()
        view.add_item(button1)
        view.add_item(button2)
        await ctx.send(f"{question}", view=view)

        async def button_callback(interaction):
            await interaction.response.send_message("test")
            await interaction.response.edit_message()
            await interaction.response.send_message("test")

        button1.callback = button_callback
        button2.callback = button_callback


def setup(bot):
    bot.add_cog(Sondage(bot))
