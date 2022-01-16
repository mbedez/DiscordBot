import discord
from discord.ext.commands import Cog, command
from discord.ext import commands
from discord import Member
from typing import List


class Morpion(Cog):
    def __init__(self, bot):
        self.bot = bot
    invite: Member = ""
    auteur = ""

    @command(name='morpion')
    async def morpion(self, ctx: commands.Context, invite: Member):
        Morpion.invite = invite
        Morpion.auteur = ctx.author.name
        demande = await ctx.message.channel.history(limit=1).flatten()
        await demande[0].delete()
        await ctx.send(f"{Morpion.auteur} invite {str(invite)[:-5]} à jouer :", view=TicTacToe())


class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        invite = str(Morpion.invite)
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        response_ok = False

        if (view.current_player == view.X and Morpion.auteur == interaction.user.name) or \
                (view.current_player == view.O and invite[:-5] == interaction.user.name):
            response_ok = True

        if view.current_player == view.X and Morpion.auteur == interaction.user.name:
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = f"Au tour de {invite[:-5]} :"
        elif view.current_player == view.O and invite[:-5] == interaction.user.name:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = f"Au tour de {Morpion.auteur} :"
        else:
            content = "bug"

        winner = view.check_board_winner()

        if winner is not None:
            if winner == view.X or winner == view.O:
                content = f"{interaction.user.name} a gagné !"
            else:
                content = "Égalité !"

            for child in view.children:
                child.disabled = True

            view.stop()

        if response_ok:
            await interaction.response.edit_message(content=content, view=view)


class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__(timeout=None)
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


def setup(bot):
    bot.add_cog(Morpion(bot))
