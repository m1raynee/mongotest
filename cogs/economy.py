import discord

from discord.ext import commands
from launcher import functions as funs


class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def money(self, ctx, member:discord.Member=None):
        member = ctx.author if not member else member
        userdb = await funs.user_check(member, ctx.guild)
        embed=discord.Embed(
            title="Монетки", 
            description=f"У `{member.display_name}` на балансе {userdb['cash']}"
            )
        await ctx.reply(embed=embed,mention_author=True)


def setup(bot):
    bot.add_cog(economy(bot))
    
def teardown(bot):
    bot.remove_cog(economy(bot))