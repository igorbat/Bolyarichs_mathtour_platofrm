import discord
from discord.ext import commands
from bot_head import father
from secret import ADMINS, ADMIN_CHANNEL, PUBLIC_CHANNEL, HI_CHANNEL

intents = discord.Intents.all()
discord_bot = commands.Bot(command_prefix='!', intents=intents)

ADMIN_COMMANDS = ['!registered', '!banned', '!finish',
 '!newtasks', '!gettasks',
  '!changetour', "!res_res_res", "!super_res"]

@discord_bot.check
def dm_only(ctx):
    return ctx.guild is None


@discord_bot.check
def special_commands_only_for_admins(ctx):
    command = str(ctx.message.content).strip().split(maxsplit=1)[0]
    if command in ADMIN_COMMANDS:
        return ctx.author.id in ADMINS
    return True

################################### АДМИН КОМАНДЫ

@discord_bot.command(name='registered', help='Принять команду в турнир')
async def ds_registered(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = ctx.message.content.strip().split(maxsplit=2)[1:]
    if len(parts) < 2:
        msg = "Недостаточно параметров"
        print(msg)
        await ctx.send(msg)
        return
    ok, msg1, msg2 = father.registered(parts[0], parts[1])
    await ctx.send(msg1)
    if ok:
        await discord_bot.get_channel(PUBLIC_CHANNEL).send(msg2)


@discord_bot.command(name='banned', help='НЕ Принять команду в турнир')
async def ds_banned(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = ctx.message.content.strip().split(maxsplit=1)[1:]
    if len(parts) == 0:
        msg = "Недостаточно параметров"
        print(msg)
        await ctx.send(msg)
        return
    ok, msg1, msg2 = father.banned(parts[0])
    await ctx.send(msg1)
    if ok:
        await discord_bot.get_channel(PUBLIC_CHANNEL).send(msg2)

@discord_bot.command(name='changetour', help='Сменить турнир у ПРИНЯТОЙ команды')
async def ds_changetour(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = ctx.message.content.strip().split(maxsplit=2)[1:]
    if len(parts) < 2:
        msg = "Недостаточно параметров"
        print(msg)
        await ctx.send(msg)
        return
    ok, msg1, msg2 = father.changetour(*parts)
    print(msg1)
    await ctx.send(msg1)
    if ok:
        await discord_bot.get_channel(PUBLIC_CHANNEL).send(msg2)

@discord_bot.command(name='newtasks', help='загрузить новые задачи: Турнир Тема ответ1 ответ2 ...')
async def ds_newtasks(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = ctx.message.content.strip().split(maxsplit=7)[1:]
    if len(parts) < 7:
        ok, msg = False, "Недостаточно параметров"
        print(msg)
        await ctx.send(msg)
    else:
        ok, msg = father.newtasks(*parts)
        print(msg)
        await ctx.send(msg)

# # отладочная команда
# @discord_bot.command(name='gettasks', help='получить задачи: Турнир Тема')
# async def gettasks(ctx):
#     print(ctx.author.id, ctx.author.name, ctx.message.content)
#     parts = ctx.message.content.strip().split(maxsplit=2)[1:]
#     if len(parts) < 2:
#         ok, msg = False, "Недостаточно параметров"
#         print(msg)
#         await ctx.send(msg)
#     else:
#         ok, msg = True, str(tasks.tours[parts[0]][parts[1]])
#         print(msg)
#         await ctx.send(msg)

@discord_bot.command(name='finish', help='Сдампить базу. Теперь можно убить бота')
async def ds_finish(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    father.finish()
    await ctx.send('Сдамплена база. Теперь можно убить бота')

@discord_bot.command(name='res_res_res', help='Сгенерировать табличку результатов')
async def ds_res_res_res(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    father.res_res_res()
    await ctx.send('Сгенерены html-ки')


@discord_bot.command(name='super_res', help='Сгенерировать табличку super-результатов')
async def ds_super_res(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    father.super_res()
    await ctx.send('Сгенерены super-html-ки')
################################### ИГРОВОЙ ПРОЦЕСС
@discord_bot.command(name='solve', help='Отправить решение в виде "solve ТЕМА ЗАДАЧА ОТВЕТ"')
async def ds_solve(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = ctx.message.content.strip().split(maxsplit=3)[1:]
    if len(parts) < 3:
        msg = "Недостаточно параметров"
        print(msg)
        await ctx.send(msg)
        return
    msg = father.solve(str(ctx.author.id), *parts)
    print(msg)
    await ctx.send(msg)

@discord_bot.command(name='points', help='Число очков команды')
async def ds_points(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    msg = father.points(str(ctx.author.id))
    print(msg)
    await ctx.send(msg)

################################### Анкетные приколы

"""
1. фио
2. название школы
3. класс обучения (только число)
4. населенный пункт
5. регион
6. телефон для связи
7. *тренер/учитель/руководитель (при наличии) — фио, должность, место работы
"""

@discord_bot.command(name='fio', help='Зарегистрировать ФИО')
async def ds_fio(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = ctx.message.content.strip().split(maxsplit=1)[1:]
    if len(parts) == 0:
        msg = "Недостаточно параметров"
        print(msg)
        await ctx.send(msg)
        return
    ok, msg = father.fio(str(ctx.author.id), parts[0])
    print(msg)
    await ctx.send(msg)

@discord_bot.command(name='school', help='Зарегистрировать Школу')
async def ds_school(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = ctx.message.content.strip().split(maxsplit=1)[1:]
    if len(parts) == 0:
        msg = "Недостаточно параметров"
        print(msg)
        await ctx.send(msg)
        return
    ok, msg = father.school(str(ctx.author.id), parts[0])
    print(msg)
    await ctx.send(msg)

@discord_bot.command(name='year', help='Зарегистрировать Класс обучения')
async def ds_year(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = ctx.message.content.strip().split(maxsplit=1)[1:]
    if len(parts) == 0:
        msg = "Недостаточно параметров"
        print(msg)
        await ctx.send(msg)
        return
    ok, msg = father.year(str(ctx.author.id), parts[0])
    print(msg)
    await ctx.send(msg)

@discord_bot.command(name='city', help='Зарегистрировать Населенный пункт')
async def ds_city(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = ctx.message.content.strip().split(maxsplit=1)[1:]
    if len(parts) == 0:
        msg = "Недостаточно параметров"
        print(msg)
        await ctx.send(msg)
        return
    ok, msg = father.city(str(ctx.author.id), parts[0])
    print(msg)
    await ctx.send(msg)

@discord_bot.command(name='region', help='Зарегистрировать Регион')
async def ds_region(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = ctx.message.content.strip().split(maxsplit=1)[1:]
    if len(parts) == 0:
        msg = "Недостаточно параметров"
        print(msg)
        await ctx.send(msg)
        return
    ok, msg = father.region(str(ctx.author.id), parts[0])
    print(msg)
    await ctx.send(msg)

@discord_bot.command(name='phone', help='Зарегистрировать Телефон')
async def ds_phone(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = ctx.message.content.strip().split(maxsplit=1)[1:]
    if len(parts) == 0:
        msg = "Недостаточно параметров"
        print(msg)
        await ctx.send(msg)
        return
    ok, msg = father.phone(str(ctx.author.id), parts[0])
    print(msg)
    await ctx.send(msg)

@discord_bot.command(name='trainer', help='Зарегистрировать Тренера')
async def ds_trainer(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = ctx.message.content.strip().split(maxsplit=1)[1:]
    if len(parts) == 0:
        msg = "Недостаточно параметров"
        print(msg)
        await ctx.send(msg)
        return
    ok, msg = father.trainer(str(ctx.author.id), parts[0])
    print(msg)
    await ctx.send(msg)

@discord_bot.command(name='tour', help='Зарегистрировать Турнир')
async def ds_tour(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    parts = ctx.message.content.strip().split(maxsplit=1)[1:]
    if len(parts) == 0:
        msg = "Недостаточно параметров"
        print(msg)
        await ctx.send(msg)
        return
    ok, msg = father.tour(str(ctx.author.id), parts[0])
    print(msg)
    await ctx.send(msg)

@discord_bot.command(name='register', help='Отправить Анкету на проверку')
async def ds_register(ctx):
    print(ctx.author.id, ctx.author.name, ctx.message.content)
    ok, msg_user, msg_admin = father.register(str(ctx.author.id))
    print(msg_user + '\n' + msg_admin)
    await ctx.send(msg_user)
    if ok:
        await discord_bot.get_channel(ADMIN_CHANNEL).send(msg_admin)

###################################
# @discord_bot.command(name='hello', help='Отправить hello в админский чат')
# async def me(ctx):
#     msg = 'Ваши текущие результаты.\n' + 'Жёлтым отмечены удвоенные бонусы!'
#     SUPER_CTX = ctx.client
#     await SUPER_CTX.find().send(msg)

@discord_bot.event
async def on_ready():
    print(f'{discord_bot.user.name} has connected to Discord!')

@discord_bot.event
async def on_message(msg):
    if msg.guild is not None and msg.content.startswith("!"):
        await msg.delete()
        return
    await discord_bot.process_commands(msg)

@discord_bot.event 
async def on_member_join(member): 
    print("Somebody joined") 
    await discord_bot.get_channel(HI_CHANNEL).send("Дорогой друг, <@{}>! Все команды нужно писать мне в личные сообщения! Не нужно писать команды в общем канале!".format(member.id))
