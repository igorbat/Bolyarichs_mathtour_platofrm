import sqlite3
import discord
from secret import TOKEN, ADMINS, ADMIN_CHANNEL
from discord.ext import commands

client = discord.Client()
bot = commands.Bot(command_prefix='!')

ADMIN_COMMANDS = ['!registered', '!banned']

@bot.check
def dm_only(ctx):
    return ctx.guild is None


@bot.check
def special_commands_only_for_admins(ctx):
    command = str(ctx.message.content).strip().split(maxsplit=1)[0]
    if command in ADMIN_COMMANDS:
        return ctx.author.id in ADMINS
    return True

@bot.command(name='registered', help='Принять команду в турнир')
async def registered(ctx):
    # await bot.get_channel(ADMIN_CHANNEL).send(msg)


@bot.command(name='banned', help='НЕ Принять команду в турнир')
async def banned(ctx):
    # await bot.get_channel(ADMIN_CHANNEL).send(msg)

# @bot.command(name='hello', help='Отправить hello в админский чат')
# async def me(ctx):
#     msg = 'Ваши текущие результаты.\n' + 'Жёлтым отмечены удвоенные бонусы!'
#     SUPER_CTX = ctx.client
#     await SUPER_CTX.find().send(msg)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# @bot.event
# async def on_message(msg):
#     print(msg.channel.id)
#     msg.client().loop.create_task(ADMIN_CHANNEL, msg + 'вот что пришло')

def main():
    bot.run(TOKEN)


if __name__ == '__main__':
    main()