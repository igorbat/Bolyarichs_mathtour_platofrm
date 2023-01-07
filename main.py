import discord
from secret import TOKEN, ADMINS
from discord.ext import commands
from abaka.data.tasks_5_strong import *

from abaka.abaka_cls import *

ADMIN_COMMANDS = ['!start', '!stop']

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())


# state_machine = StateMachine()
#
# karusel_test = GameKarusel("test",
#                            "https://docs.google.com/document/d/1VlLj1B6JeLmsBeVtijxZNSb5KWbF4nHI-uD7-zvZnwQ/edit?usp=sharing",
#                            ["1", "0", "0", "5", "0", "0"])
# state_machine.add_tour("test", karusel_test)


state_machine = StateMachine()
game_test = \
    GameAbaka("test",
              "https://docs.google.com/document/d/1VlLj1B6JeLmsBeVtijxZNSb5KWbF4nHI-uD7-zvZnwQ/edit?usp=sharing",
              TASKS_TEST)
state_machine.add_tour("test", game_test)

game_1 = \
    GameAbaka("game1",
              "https://docs.google.com/document/d/1_-LOZLcTnv9ps8SsSsMJAK0srCTo1rE4qcEwYfw3mCw/edit?usp=sharing",
              TASK_1)
state_machine.add_tour("game1", game_1)

# game_strong_5 = \
#     GameAbaka("phys",
#                               "https://drive.google.com/file/d/1AcGt8lXT9UEQYTBGgMsmalwwMJcSKCHG/view?usp=sharing",
#                               TASKS_5_STRONG)
# state_machine.add_tour("phys", game_strong_5)

# game_weak_5 = \
#     GameAbaka("novice_5",
#               "https://drive.google.com/file/d/1eXZjFVYTt9Iu9EQbZVulwQ4mYaHzUgeR/view?usp=sharing",
#               TASKS_5_WEAK)
# state_machine.add_tour("novice_5", game_weak_5)
# #
#
# game_strong_8 = \
#     GameAbaka("pro_8",
#               "https://drive.google.com/file/d/1Mjlc2-P1wdZw6WLuH6KPEML1CIz_Mrfb/view?usp=sharing",
#               TASKS_8_STRONG)
# state_machine.add_tour("pro_8", game_strong_8)
#
#
# game_weak_8 = \
#     GameAbaka("novice_8",
#               "https://drive.google.com/file/d/1a9L0kT0yJs9VTFjIgxTaZO7ELQdOYcin/view?usp=sharing",
#               TASKS_8_WEAK)
# state_machine.add_tour("novice_8", game_weak_8)


@bot.check
def dm_only(ctx):
    return ctx.guild is None


@bot.check
def special_commands_only_for_admins(ctx):
    command = str(ctx.message.content).strip().split(maxsplit=1)[0]
    if command in ADMIN_COMMANDS:
        return ctx.author.id in ADMINS
    return True


#  this is admin command
@bot.command(name='start', help='запустить турнир')
async def start(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = str(ctx.message.content).strip().split(maxsplit=1)
    if len(parts) < 2:
        msg = "Недостаточно аргументов. Нужно написать название турнира"
        print(msg)
        await ctx.send(msg)
    else:
        ok, msg = state_machine.start_tour(parts[1])
        print(msg)
        await ctx.send(msg)


#  this is admin command
@bot.command(name='stop', help='остановить турнир')
async def stop(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = str(ctx.message.content).strip().split(maxsplit=1)
    if len(parts) < 2:
        msg = "Недостаточно аргументов. Нужно написать название турнира"
        print(msg)
        await ctx.send(msg)
    else:
        ok, msg = state_machine.stop_tour(parts[1])
        print(msg)
        await ctx.send(msg)

@bot.command(name='register', help='зарегистрировать команду: школа, класс или целиком название')
async def register(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = str(ctx.message.content).strip().split(maxsplit=1)
    if len(parts) < 2:
        msg = "Недостаточно аргументов. Нужно написать школу класс"
        print(msg)
        await ctx.send(msg)
    else:
        team_name = state_machine.register_player(ctx.author.id, parts[1])
        msg = "Ваша команда: {}".format(team_name)
        print(msg)
        await ctx.send(msg)


@bot.command(name='join', help='Присоединиться к игре')
async def join(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = str(ctx.message.content).strip().split(maxsplit=1)
    if len(parts) < 2:
        msg = "Недостаточно аргументов. Нужно написать название соревнования"
        print(msg)
        await ctx.send()
    else:
        ok, msg = state_machine.join_tour(ctx.author.id, parts[1])
        print(msg)
        await ctx.send(msg)


# @bot.command(name='leave', help='Отсоединиться от игры. Прогресс сохранится')
# async def leave(ctx):
#     ok, msg = state_machine.leave(ctx.author.id)
#     await ctx.send(msg)


@bot.command(name='solve', help='Отправить решение в виде "solve ТЕМА ЗАДАЧА ОТВЕТ"')
async def solve(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = ctx.message.content.strip().split(maxsplit=4)[1:]

    ok, msg = state_machine.solve(ctx.author.id, *parts)
    print(msg)
    await ctx.send(msg)


@bot.command(name='tasks', help='Получить ссылку на задания')
async def tasks_link(ctx):
    # print(ctx.author.id, ctx.author.name, ctx.message.content)
    ok, msg = state_machine.tasks(ctx.author.id)
    # print(msg)
    await ctx.send(msg)


@bot.command(name='sent_task', help='Какие задания вы отправили')
async def sent_task(ctx):
    # print(ctx.author.id, ctx.author.name, ctx.message.content)
    ok, msg = state_machine.sent_task(ctx.author.id)
    # print(msg)
    await ctx.send(msg)


@bot.command(name='points', help='Сколько у нас очков')
async def points(ctx):
    # print(ctx.author.id, ctx.author.name, ctx.message.content)
    ok, msg = state_machine.points(ctx.author.id)
    # print(msg)
    await ctx.send(msg)


@bot.command(name='res_res_res', help='Обновить результаты')
async def res_res_res(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    state_machine.reload_res()
    msg = "Обновлено"
    print(msg)
    await ctx.send(msg)


@bot.command(name='res', help='Получить результаты')
async def res_res_res(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    _, msg = state_machine.get_text_res()
    print(msg)
    await ctx.send(msg)


@bot.command(name='table_res', help='Получить результаты в виде таблицы')
async def me(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    path = state_machine.res_table(ctx.author.id)
    msg = 'Ваши текущие результаты.\n' + 'Жёлтым отмечены удвоенные бонусы!'
    await ctx.send(msg, file=discord.File(path))

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


def main():
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
