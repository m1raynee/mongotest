import os
import discord
import certifi
import motor.motor_asyncio

from discord.ext import commands

client = commands.Bot(
    command_prefix = '.',
    intents = discord.Intents.all()
)
client.remove_command('help')

ca = certifi.where()

client.mongo = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://FarMaT:123456789a@cluster0.v7xif.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=ca)
client.db = client.mongo.users

client.collection = client.db.Cluster0





@client.event
async def on_ready():
    print(f"Аккаунт: {client.user}")
    await client.change_presence(status=discord.Status.dnd)


@client.command(name = 'ext')
async def extentions_menage(ctx, sub_command, ext_name):
    if sub_command == 'load':
        client.load_extension(f'cogs.{ext_name}')
        await ctx.send(f'Расширение `{ext_name}` загружено')
    elif sub_command == 'unload':
        client.unload_extension(f'cogs.{ext_name}')
        await ctx.send(f'Расширение `{ext_name}` отгружено')
    elif sub_command == 'reload':
        client.reload_extension(f'cogs.{ext_name}')
        await ctx.send(f'Расширение `{ext_name}` перезагружено')

loads = ''
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        loads += f'{filename[:-3]}, '
        client.load_extension(f'cogs.{filename[:-3]}')
loads = loads[:-2]
client.load_extension('jishaku')

class functions:
    @staticmethod
    async def insert_server(guild):
        server = {
           "_id": guild.id,
           'users': {},
            
        }
        await client.collection.insert_one(server)
        return True

    @staticmethod
    async def user_check(user, guild: discord.Guild, met:str = None, key:str = 'users'):
        
        def upd(server):
            return {
                "cash": 40,

                "xp": 0,


                "bio": None,
                "rep": 0,
            }

        if type(user) == int:
            user.id = user

        server = await client.collection.find_one({"_id": guild.id})
        if server == None:
            await functions.insert_server(guild)
            server = await client.collection.find_one({"_id": guild.id})
        if met == None:

            try:
                user = server[key][str(user.id)]
                return user
            except Exception:
                if user.bot == True:
                    return False

                a = server[key].copy()
                a.update({ str(user.id): upd(server) })
                await client.collection.update_one({"_id": guild.id}, {"$set": {key: a}})
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
            await client.collection.update_one({"_id": guild.id}, {"$set": {key: a}})
            return True

    @staticmethod
    async def user_update(user, guild: discord.Guild, key:str, ch, met = 'update', func='set', key2 = 'users'):
        userdb = await functions.user_check(user, guild)
        server = await client.collection.find_one({"_id": guild.id})
        if server == None:
            await functions.insert_server(guild)
            userdb = await functions.user_check(user, guild)
            server = await client.collection.find_one({"_id": guild.id})
        

        a = server[key2].copy()
        if type(user.id) == discord.Member:
            user.id = user.id.id
        if met == 'update':
            if func == 'set':
                chh = ch
            elif func == 'inc':
                chh = userdb[key] + ch
            try:
                a[str(user.id)].update({key : chh })
            except Exception:
                a.update({str(user.id) : {key : chh } })
            await client.collection.update_one({"_id": guild.id}, {"$set": {key2: a}})
            return True

        if met == 'pop':

            try:

                a[str(user.id)].pop(key)
                if a[str(user.id)] == {}:
                    a.pop(str(user.id))
                await client.collection.update_one({"_id": guild.id}, {"$set": {key2: a}})
                return True

            except Exception:
                return False
        else:
            print(f'Метод {met} не найден')


print(f'Подгруженные расширения: {loads}')
client.run("ODgyMjgxOTE4NjE4NTQyMTIx.YS5HEQ.mJcdeU8THIglZ4SARvdAR1ikXf4")