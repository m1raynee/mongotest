import os
import discord

from discord.ext import commands

client = commands.Bot(command_prefix = '.', intents = discord.Intents.all())
client.remove_command('help')


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

print(f'Подгруженные расширения: {loads}')
client.run("")