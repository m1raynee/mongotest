from typing import Union
import disnake


class functions:
    

    @staticmethod
    async def user_update(user, guild: disnake.Guild, key:str, ch, met = 'update', func='set', key2 = 'users'):
        userdb = await functions.user_check(user, guild)
        server = await bot.collection.find_one({"_id": guild.id})
        if server == None:
            await functions.insert_server(guild)
            userdb = await functions.user_check(user, guild)
            server = await bot.collection.find_one({"_id": guild.id})
        

        a = server[key2].copy()
        if type(user.id) == disnake.Member:
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
            await bot.collection.update_one({"_id": guild.id}, {"$set": {key2: a}})
            return True

        if met == 'pop':

            try:

                a[str(user.id)].pop(key)
                if a[str(user.id)] == {}:
                    a.pop(str(user.id))
                await bot.collection.update_one({"_id": guild.id}, {"$set": {key2: a}})
                return True

            except Exception:
                return False
        else:
            print(f'Метод {met} не найден')

from bot import Bot

Bot().run('token')