import os

from disnake.ext import commands
import disnake

import certifi
import motor.motor_asyncio
from typing import Union


initial_extensions = (
    'economy',
    'level',
    'prestige',
    'profile',
)

NEW_USER_VALUES = {
    "money": 100,

    "xp": 0,
    "ms": 0, #количество сообщений
    "cm": 0, #количество использованых комманд

    "bio": None,
    "prestige": 0,
}

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='+',
            intents=disnake.Intents.all(),
            status=disnake.Status.idle
        )

        ca = certifi.where()
        mongo = motor.motor_asyncio.AsyncIOMotorClient("", tlsCAFile=ca)
        db = mongo.users
        self.collection = db.Cluster0

        for ext in initial_extensions:
            try:
                self.load_extension(f'cogs.{ext}')
            except Exception as e:
                print(f'Не удалось загрузить ког. Ошибка {e.__class__.__name__}: {e}')
    
    @commands.group(name = 'ext', invoke_without_command=True)
    async def extentions_menage(self, ctx):
        raise NotImplementedError

    @extentions_menage.command('load')
    async def extentions_load(self, ctx: commands.Context, ext_name: str):
        self.load_extension(f'cogs.{ext_name}')
        await ctx.send(f'Расширение `{ext_name}` загружено')

    @extentions_menage.command('unload')
    async def extentions_unload(self, ctx: commands.Context, ext_name: str):
        self.unload_extension(f'cogs.{ext_name}')
        await ctx.send(f'Расширение `{ext_name}` отгружено')

    @extentions_menage.command('reload')
    async def extentions_reload(self, ctx: commands.Context, ext_name: str):
        self.reload_extension(f'cogs.{ext_name}')
        await ctx.send(f'Расширение `{ext_name}` перезагружено')


    async def on_ready(self):
        print(f"Аккаунт: {self.user}")
    
    async def get_or_create_server(self, guild_id: int):
        server = {
            "_id": guild_id,
            'users': {},
            
        }
        await self.collection.insert_one(server)
        return True

    async def user_check(self, user: int, guild_id: int, met: str = None, key: str = 'users'):

        if type(user) == int:
            user.id = user

        server = await self.collection.find_one({"_id": guild_id})
        if server == None:
            await self.insert_server(guild_id)
            server = await self.collection.find_one({"_id": guild_id})
        if met == None:

            try:
                user = server[key][str(user.id)]
                return user
            except Exception:
                if user.bot == True:
                    return False

                a = server[key].copy()
                a.update({ str(user.id): upd(server) })
                await bot.collection.update_one({"_id": guild.id}, {"$set": {key: a}})
                return a[str(user.id)]

        if met == 'dcheck':

            try:
                user = server[key][str(user.id)]
                return True
            except Exception:
                return False

        if met == 'add':

            a = server[key].copy()
            a.update({str(user.id): upd(server) })
            await bot.collection.update_one({"_id": guild.id}, {"$set": {key: a}})
            return True