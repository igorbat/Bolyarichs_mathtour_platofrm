import sqlite3
import discord
from burat.secret import TOKEN, ADMINS, ADMIN_CHANNEL
from discord.ext import commands

from burat.util import calculate_points
from solution_cache import SolutionCache
from player_cache import PlayerCache
from task_cache import TaskCache

def reset():
    pass

# reset()

client = discord.Client()
bot = commands.Bot(command_prefix='!')
solutions = SolutionCache()
players = PlayerCache()
tasks = TaskCache()

ADMIN_COMMANDS = ['!registered', '!banned', '!finish', '!newtasks', '!gettasks']

@bot.check
def dm_only(ctx):
    return ctx.guild is None


@bot.check
def special_commands_only_for_admins(ctx):
    command = str(ctx.message.content).strip().split(maxsplit=1)[0]
    if command in ADMIN_COMMANDS:
        return ctx.author.id in ADMINS
    return True

################################### АДМИН КОМАНДЫ

# @bot.command(name='registered', help='Принять команду в турнир')
# async def registered(ctx):
#     # await bot.get_channel(ADMIN_CHANNEL).send(msg)


# @bot.command(name='banned', help='НЕ Принять команду в турнир')
# async def banned(ctx):
#     # await bot.get_channel(ADMIN_CHANNEL).send(msg)


@bot.command(name='newtasks', help='загрузить новые задачи: Турнир Тема ответ1 ответ2 ...')
async def newtasks(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = ctx.message.content.strip().split(maxsplit=8)[1:]
    if len(parts) < 7:
        ok, msg = False, "Недостаточно параметров"
        print(msg)
        await ctx.send(msg)
    else:
        ok, msg = tasks.create_or_update_task(*parts)
        print(msg)
        await ctx.send(msg)

# отладочная команда
@bot.command(name='gettasks', help='получить задачи: Турнир Тема')
async def gettasks(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = ctx.message.content.strip().split(maxsplit=3)[1:]
    if len(parts) < 2:
        ok, msg = False, "Недостаточно параметров"
        print(msg)
        await ctx.send(msg)
    else:
        ok, msg = True, str(tasks.tours[parts[0]][parts[1]])
        print(msg)
        await ctx.send(msg)

@bot.command(name='finish', help='Сдампить базу. Теперь можно убить бота')
async def finish(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    solutions.conn.close()
    players.conn.close()
    tasks.conn.close()
    await ctx.send('Сдамплена база. Теперь можно убить бота')


################################### ИГРОВОЙ ПРОЦЕСС
@bot.command(name='solve', help='Отправить решение в виде "solve ТЕМА ЗАДАЧА ОТВЕТ"')
async def solve(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = ctx.message.content.strip().split(maxsplit=5)[1:]
    tour = players.players_storage[ctx.author.id].tour
    ok_, msgg = tasks.is_task(tour, *parts)
    if not ok_:
        await ctx.send(msgg)
        return
    # проверить, что не было повторной посылки по той же задаче
    theme_count = 0
    for sol in solutions.solution_storage:
        if sol[0] == ctx.author.id and sol[1] == parts[0]:
            theme_count += 1
    if theme_count + 1 > int(parts[1]):
        await ctx.send("Вы уже отправляли данную задачу")
        return
    elif theme_count + 1 < int(parts[1]):
        await ctx.send("Вы ещё не отправили прошлые задачи")
        return

    ok, msg1 = solutions.new_solution(ctx.author.id, *parts)
    print(msg1)
    ok2 = tasks.check_task(tour, *parts)
    await ctx.send(msg1 + '\n' + "Ура! ответ совпал с текущим в базе" if ok2 else "Увы, ответ не совпал с текущим в базе")

@bot.command(name='points', help='Число очков команды')
async def points(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    tour = players.players_storage[ctx.author.id].tour
    ok, msg = calculate_points(ctx.author.id, tour, solutions, tasks)
    print(msg)
    await ctx.send(msg)

################################### Анкетные приколы

@bot.command(name='points', help='Получить число предварительных очков')
async def points(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    ok, msg = solutions.solution_count(str(ctx.author.id))
    print(msg)
    await ctx.send(msg)

@bot.command(name='fio', help='Зарегистрировать ФИО')
async def points(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    ok, msg = solutions.solution_count(str(ctx.author.id))
    print(msg)
    await ctx.send(msg)

@bot.command(name='points', help='Получить число предварительных очков')
async def points(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    ok, msg = solutions.solution_count(str(ctx.author.id))
    print(msg)
    await ctx.send(msg)

@bot.command(name='points', help='Получить число предварительных очков')
async def points(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    ok, msg = solutions.solution_count(str(ctx.author.id))
    print(msg)
    await ctx.send(msg)
###################################
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
