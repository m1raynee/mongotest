import disnake as disnake
from disnake.ext import commands
import datetime
from datetime import datetime, timezone
import asyncio
from PIL import Image
import aiohttp
from io import BytesIO
from launcher import functions as funs, guilds

import pymorphy2

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

class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")


    async def paginator(self, inter, user, invoke):
        user = inter.guild.get_member(user.id)
        member = await funs.user_check(user, inter.guild)
        server = await self.client.collection.find_one({"_id": inter.guild.id})
        ava = user.avatar.replace(static_format='png',size=4096)
        avatar = str(ava)[:-10]
        
        async with aiohttp.ClientSession() as session:
            async with session.get(avatar) as resp:
                if resp.status != 200:
                    raise Exception
                img = Image.open(BytesIO(await resp.read()))
        colour = img.resize((1, 1), Image.ANTIALIAS).getpixel((0, 0))
        color = int("{:02x}{:02x}{:02x}".format(*colour), 16)       
        if invoke == 'profile':
        #---------Профиль--]        
            prestiges = member["prestige"]
            #-Престиж--^
            bio = member['bio']
            #-Описание--^
            countmsg = member["ms"]
            countcommands = member["cm"]
            #-Количество сообщений и использованых команд-^
            jjoin = user.joined_at.timestamp()
            join = f"<t:{jjoin:.0f}:f>"
            #-Дата когда пользователь присоединился-^
            if str(user.status) == 'online':
                status = "<:status_online:596576749790429200>"
            if str(user.status) == 'idle':
                status = "<:status_idle:596576773488115722>"
            if str(user.status) == 'dnd':
                status = "<:status_dnd:596576774364856321>"
            if str(user.status) == 'offline':
                status = "<:status_offline:596576752013279242>"
            profile = disnake.Embed(
                title=f"{status} Профиль {user.display_name}",
                color=color
            ).set_thumbnail(
                url=user.avatar.url
            ).add_field(
                name=f"\🗂️ Main Info",
                value=f"\📋 **Имя:** `{user}`\n"
                    f"\🆔 **Айди:** `{user.id}`\n"
                    f"\🌱 **Создан:** `{user.created_at.strftime('%Y-%m-%d')}`\n",
                    inline=False
            ).add_field(
                name=f"<:prestiges:892483896149676052> Престиж",
                value=f"{prestiges} престиж"
            ).add_field(
                name=f"<:icon1:892483703241080832> Присоединился",
                value=f"{join}"
            ).add_field(
                name=f"<a:loading:747680523459231834> Всего сообщений оправлено",
                value=f"{inflect_by_amount(countmsg, 'сообщение')}",
                inline=False
            ).add_field(
                name=f"<:creator:891624858516078622> Всего команд использовано",
                value=f"{inflect_by_amount(countcommands, 'команда')}",
                inline=False
            )
            if bio == None:
                pass
            else:
                profile.description = bio
        #------------------^
            await inter.response.send_message(embed = profile)

        elif invoke == 'level':
        #-------level----]
            xp = member["xp"]
            allxp = xp
            lvl = 0
            rank = 0
            while True:
                if xp < ((3*(lvl**2))+(3*lvl)):
                    break
                lvl += 1
            xp -= ((3*((lvl-1)**2))+(3*(lvl-1)))
            boxes = int((xp/(12*((1/2) * lvl)))*20)
            t = dict(sorted(server['users'].items(),key=lambda x: x[1]['xp'], reverse=True))
            rank = list(t.keys()).index(str(user.id)) +1
            if rank == 1:
                ranks = "🏅"
            if rank == 2:
                ranks = "🥈"
            if rank == 3:
                ranks = "🥉"
            if rank >= 4:
                ranks = ""
            #----
            xpnl = int(12*((1/2)*lvl))
            #----
            level = disnake.Embed(
                title=f"{user.display_name}",
                color=0xED760E
            ).add_field(
                name=f"Уровень",
                value=f"```{lvl-1} уровень```",
                inline=True
            ).add_field(
                name=f"Ранг",
                value=f"```{ranks}{rank} место```",
                inline=True
            ).add_field(
                name=f"Всего баллов",
                value=f"```{inflect_by_amount(allxp, 'балл')}```",
                inline=True
            ).add_field(
                name=f"До {lvl} уровня",
                value=f"```{inflect_by_amount(xpnl - xp, 'балл')}```",
                inline=True
            ).set_footer(
                text=f"{xp/ xpnl * 100:.0f}% {boxes * '█' + (20-boxes) * ' '}⎸→ {lvl}lvl"
            )
        #-----------------
            await inter.response.send_message(embed = level)

        elif invoke == 'money':
        #-------money----]
            money = member['money']
            money = disnake.Embed(
                title=f"<:___:894315448261279754> {user.display_name}",
                color=0x324AB2,
                timestamp = datetime.utcnow()
            ).set_thumbnail(
                url=user.avatar.url
            ).add_field(
                name=f"Монеты:",
                value=f"{inflect_by_amount(money, 'монета')}(здесь свой эмодзи монетки)"
            )
        #-----------------^
            await inter.response.send_message(embed = money)
        else:
            raise TypeError(f'Страницы {invoke} не существует')
        message = await inter.original_message()
        react_add = ['💼', '🔰', '💵']
        def check(reaction, rmember):
            return rmember == inter.author and message.id == reaction.message.id and str(reaction.emoji) in react_add
        for react in react_add:
            await message.add_reaction(react)
        while True:
            try:
                reaction, rmember = await self.client.wait_for('reaction_add',timeout=300, check = check)
                await message.remove_reaction(reaction, rmember)
                member = await funs.user_check(user, inter.guild)
                if str(reaction.emoji) == '💼':
                #---------Профиль--]        
                    prestiges = member["prestige"]
                    #-Престиж--^
                    bio = member['bio']
                    #-Описание--^
                    countmsg = member["ms"]
                    countcommands = member["cm"]
                    #-Количество сообщений и использованых команд-^
                    jjoin = user.joined_at.timestamp()
                    join = f"<t:{jjoin:.0f}:f>"
                    #-Дата когда пользователь присоединился-^
                    if str(user.status) == 'online':
                        status = "🟩"
                    if str(user.status) == 'idle':
                        status = "🟧"
                    if str(user.status) == 'dnd':
                        status = "🟥"
                    if str(user.status) == 'offline':
                        status = "💤"
                    profile = disnake.Embed(
                        title=f"{status} Профиль {user.display_name}",
                        color=color
                    ).set_thumbnail(
                        url=user.avatar.url
                    ).add_field(
                        name=f"\🗂️ Main Info",
                        value=f"\📋 **Имя:** `{user}`\n"
                            f"\🆔 **Айди:** `{user.id}`\n"
                            f"\🌱 **Создан:** `{user.created_at.strftime('%Y-%m-%d')}`\n",
                            inline=False
                    ).add_field(
                        name=f"<:prestiges:892483896149676052> Престиж",
                        value=f"{prestiges} престиж"
                    ).add_field(
                        name=f"<:icon1:892483703241080832> Присоединился",
                        value=f"{join}"
                    ).add_field(
                        name="<:badges:904114356613173351> Значки",
                        value=f"скоро"
                    ).add_field(
                        name=f"<:usericon:891624858214072382> Всего сообщений оправлено",
                        value=f"{inflect_by_amount(countmsg, 'сообщение')}",
                        inline=False
                    ).add_field(
                        name=f"<:creator:891624858516078622> Всего команд использовано",
                        value=f"{inflect_by_amount(countcommands, 'команда')}",
                        inline=False
                    )
                    if bio == None:
                        pass
                    else:
                        profile.description = bio
                #------------------^
                    await message.edit(embed = profile)
                elif str(reaction.emoji) == '🔰':
                #-------level----]
                    xp = member["xp"]
                    allxp = xp
                    lvl = 0
                    rank = 0
                    while True:
                        if xp < ((3*(lvl**2))+(3*lvl)):
                            break
                        lvl += 1
                    xp -= ((3*((lvl-1)**2))+(3*(lvl-1)))
                    boxes = int((xp/(12*((1/2) * lvl)))*20)
                    t = dict(sorted(server['users'].items(),key=lambda x: x[1]['xp'], reverse=True))
                    rank = list(t.keys()).index(str(user.id)) +1
                    if rank == 1:
                        ranks = "🏅"
                    if rank == 2:
                        ranks = "🥈"
                    if rank == 3:
                        ranks = "🥉"
                    if rank >= 4:
                        ranks = ""
                    #----
                    xpnl = int(12*((1/2)*lvl))
                    #----
                    level = disnake.Embed(
                        title=f"{user.display_name}",
                        color=0xED760E
                    ).add_field(
                        name=f"Уровень",
                        value=f"```{lvl-1} уровень```",
                        inline=True
                    ).add_field(
                        name=f"Ранг",
                        value=f"```{ranks}{rank} место```",
                        inline=True
                    ).add_field(
                        name=f"Всего баллов",
                        value=f"```{inflect_by_amount(allxp, 'балл')}```",
                        inline=True
                    ).add_field(
                        name=f"До {lvl} уровня",
                        value=f"```{inflect_by_amount(xpnl - xp, 'балл')}```",
                        inline=True
                    ).set_footer(
                        text=f"{xp/ xpnl * 100:.0f}% {boxes * '█' + (20-boxes) * ' '}⎸→ {lvl}lvl"
                    )
                #-----------------
                    await message.edit(embed = level)
                elif str(reaction.emoji) == '💵':
                #-------money----]
                    money = member['money']
                    money = disnake.Embed(
                        title=f"<:___:894315448261279754> {user.display_name}",
                        color=0x324AB2,
                        timestamp = datetime.utcnow()
                    ).set_thumbnail(
                        url=user.avatar.url
                    ).add_field(
                        name=f"Монеты:",
                        value=f"{inflect_by_amount(money, 'монета')}(здесь свой эмодзи монетки)"
                    )
                #-----------------^
                    await message.edit(embed = money)
            except asyncio.TimeoutError:
                try:
                    await message.clear_reactions()
                except:
                    pass


    @commands.slash_command(
        name="bio",
        description="Изменить описание в профиле",
        guild_ids=guilds,
        options=[
            disnake.Option("description", "Укажите новое описание в профиле", disnake.OptionType.string)
        ]
    )
    async def bio(self, inter,description=None):
        await funs.user_check(inter.author, inter.guild)
        if not description:
            await inter.response.send_message("Описание удалено!")
            await funs.user_update(inter.author, inter.guild, "bio", None, 'update', 'set','users')
            return
        if len(description) > 150:
            await inter.response.send_message("Описание слишком длинное!")
            return
        await inter.response.send_message("Описание изменено!")
        await funs.user_update(inter.author, inter.guild, "bio", str(description), 'update', 'set','users')

    @commands.slash_command(
        name="profile",
        description="Посмотреть профиль пользователя",
        guild_ids=guilds,
        options=[
            disnake.Option("user", "Укажите пользователя", disnake.OptionType.user),
        ]
    )
    async def profile(self,inter, user=None):
        user = inter.author if not user else user
        if not user.bot:
            await self.paginator(inter, user, 'profile')



    @commands.slash_command(
        name="level",
        description="Посмотреть уровень пользователя",
        guild_ids=guilds,
        options=[
            disnake.Option("user", "Укажите пользователя", disnake.OptionType.user),
        ]
    )
    async def level(self,inter, user=None):
        user = inter.author if not user else user
        if not user.bot:
            await self.paginator(inter, user, 'level')



    @commands.slash_command(
        name="money",
        description="Посмотреть баланс пользователя",
        guild_ids=guilds,
        options=[
            disnake.Option("user", "Укажите пользователя", disnake.OptionType.user),
        ]
    )
    async def money(self,inter, user=None):
        user = inter.author if not user else user
        if not user.bot:
            await self.paginator(inter, user, 'money')


    @commands.user_command(
        name="Профиль",
        description="Посмотреть профиль пользователя",
        guild_ids=guilds
    )
    async def pprofile(self,inter):
        user = inter.guild.get_member(inter.target.id)
        member = await funs.user_check(user, inter.guild)
        ava = user.avatar.replace(static_format='png',size=4096)
        avatar = str(ava)[:-10]
        
        async with aiohttp.ClientSession() as session:
            async with session.get(avatar) as resp:
                if resp.status != 200:
                    raise Exception
                img = Image.open(BytesIO(await resp.read()))
        colour = img.resize((1, 1), Image.ANTIALIAS).getpixel((0, 0))
        color = int("{:02x}{:02x}{:02x}".format(*colour), 16)    
        if inter.target.bot == False:  
        #---------Профиль--]        
            prestiges = member["prestige"]
            #-Престиж--^
            bio = member['bio']
            #-Описание--^
            countmsg = member["ms"]
            countcommands = member["cm"]
            #-Количество сообщений и использованых команд-^
            jjoin = user.joined_at.timestamp()
            join = f"<t:{jjoin:.0f}:f>"
            #-Дата когда пользователь присоединился-^
            if str(user.status) == 'online':
                status = "🟩"
            if str(user.status) == 'idle':
                status = "🟧"
            if str(user.status) == 'dnd':
                status = "🟥"
            if str(user.status) == 'offline':
                status = "💤"
            profile = disnake.Embed(
                title=f"{status} Профиль {user.display_name}",
                color=color
            ).set_thumbnail(
                url=user.avatar.url
            ).add_field(
                name=f"\🗂️ Main Info",
                value=f"\📋 **Имя:** `{user}`\n"
                    f"\🆔 **Айди:** `{user.id}`\n"
                    f"\🌱 **Создан:** `{user.created_at.strftime('%Y-%m-%d')}`\n",
                    inline=False
            ).add_field(
                name=f"<:prestiges:892483896149676052> Престиж",
                value=f"{prestiges} престиж"
            ).add_field(
                name=f"<:icon1:892483703241080832> Присоединился",
                value=f"{join}"
            ).add_field(
                name="<:badges:904114356613173351> Значки",
                value=f"скоро"
            ).add_field(
                name=f"<:usericon:891624858214072382> Всего сообщений оправлено",
                value=f"{inflect_by_amount(countmsg, 'сообщение')}",
                inline=False
            ).add_field(
                name=f"<:creator:891624858516078622> Всего команд использовано",
                value=f"{inflect_by_amount(countcommands, 'команда')}",
                inline=False
            )
            if bio == None:
                pass
            else:
                profile.description = bio
        else:
        #---------Профиль бота--]
            jjoin = user.joined_at.timestamp()
            join = f"<t:{jjoin:.0f}:f>"
            #-Дата когда пользователь присоединился-^
            if str(user.status) == 'online':
                status = "🟩"
            if str(user.status) == 'idle':
                status = "🟧"
            if str(user.status) == 'dnd':
                status = "🟥"
            if str(user.status) == 'offline':
                status = "💤"
            profile = disnake.Embed(
                title=f"{status} Профиль {user.display_name}",
                color=color
            ).set_thumbnail(
                url=user.avatar.url
            ).add_field(
                name=f"\🗂️ Main Info",
                value=f"\📋 **Имя:** `{user}`\n"
                    f"\🆔 **Айди:** `{user.id}`\n"
                    f"\🌱 **Создан:** `{user.created_at.strftime('%Y-%m-/%d')}`\n",
                    inline=False
            ).add_field(
                name=f"<:icon1:892483703241080832> Присоединился",
                value=f"{join}"
            )
        await inter.response.send_message(embed = profile,ephemeral=True)


def setup(client):
    client.add_cog(Profile(client))