import disnake as disnake
from disnake.ext import commands
import datetime
from datetime import datetime, timezone
import asyncio
from PIL import Image
from io import BytesIO

from disnake.ext.commands.cooldowns import BucketType
from launcher import functions as funs

import pymorphy2

guilds = [
    846682680791531530
]

morph = pymorphy2.MorphAnalyzer()
def inflect_by_amount(amount, word):
    parse = morph.parse(word)[0]
    inflect = parse.word

    _number = int(str(amount)[-2:])
    if _number > 10 and _number < 15:
        inflect = parse.inflect({'plur', 'gent'}).word
    else:
        _number = int(str(_number)[-1:])
        if _number == 0:
            inflect = parse.inflect({'plur', 'gent'}).word
        elif _number == 1:
            inflect = word
        elif _number > 4:
            inflect = parse.inflect({'plur', 'gent'}).word
        elif _number > 1:
            inflect = parse.inflect({'gent'}).word
    return f'{amount} {inflect}'

class prestige(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name="prestige",
        description="Повысить престиж",
        guild_ids=guilds,
        options=[
            disnake.Option("user", "Укажите пользователя", disnake.OptionType.user),
        ]
    )
    @commands.cooldown(4, 86400, BucketType.user)
    async def prestige(self, inter, user = disnake.Member):
        if user.id == inter.author.id:
            await inter.response.send_message('Нельзя повысить престиж самому себе!')
        if user.bot == True:
            await inter.response.send_message('Нельзя повысить престиж боту!')
        if not user.bot:
            member = await funs.user_check(user, inter.guild)
            await funs.user_update(user, inter.guild, "prestige", 1, 'update', 'inc','users')
            await inter.response.send_message(f'Успешно повышен престиж пользователю {user.display_name}.')

def setup(client):
    client.add_cog(prestige(client))