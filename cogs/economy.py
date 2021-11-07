import disnake

from disnake.ext import commands
from launcher import functions as funs


class Economy(commands.Cog):
    def __init__(self, client):
        self.bot = client


    @commands.command()
    async def add_money(self,ctx,money:int=15):
        await ctx.send(f"Добавлено {money} монет")
        await funs.user_update(ctx.author, ctx.guild, "money", money, 'update', 'inc','users')


def setup(client):
    client.add_cog(Economy(client))
