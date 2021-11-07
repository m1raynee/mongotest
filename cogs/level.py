import disnake
import json
import asyncio
import datetime

from launcher import functions as funs, guilds
from disnake.ext import commands

# async def level_up(users, user, message):
#     with open('levels.json', 'r') as g:
#         levels = json.load(g)
#     experience = users[f'{user.id}']['experience']
#     lvl = 0
#         msg = await message.channel.send(
#             embed = discord.Embed(
#                 title = '🔰 Уровни',
#                 description = f'{user.display_name} повысил уровень до {lvl_end}',
#                 color = 0x45ff30
#             )
#         )
#         await msg.add_reaction('🔥')
#         users[f'{user.id}']['level'] = lvl_end

class level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#     @commands.Cog.listener()
#     async def on_member_join(self, member):
#         with open("users.json", 'r') as f:
#             users = json.load(f)

#         await update_data(users, member)

#         with open('users.json', 'w') as f:
#             json.dump(users, f, indent=4)
    # @commands.Cog.listener()
    # async def on_member_remove(self, member):
    #     with open('users.json') as f:
    #         users = json.load(f)
    #     users[f'{member.id}'].delete()
    #     with open('users.json', 'w') as f:
    #         json.dump(users, f, indent=4)

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if message.author.bot == False:
    #         db = await funs.user_check(message.author, message.guild)
    #         await funs.user_update(message.author, message.guild, "xp", 1, 'update', 'inc','users')
    #         xp = db['xp']
    #         lvl = 0
    #         while True:
    #             if xp < ((3*(lvl**2))+(3*lvl)):
    #                 break
    #             lvl += 1
    #         xp -= ((3*((lvl-1)**2))+(3*(lvl-1)))
    #         if xp == 0:
    #             msg = await message.channel.send(
    #                 embed = disnake.Embed(
    #                     title = '🔰 Уровни',
    #                     description = f'{message.author.display_name} повысил уровень до {lvl}',
    #                     color = 0x45ff30
    #                 )
    #             )
    #             await msg.add_reaction('🎉')

def setup(bot):
    bot.add_cog(level(bot))

def teardown(bot):
    bot.remove_cog(level(bot))