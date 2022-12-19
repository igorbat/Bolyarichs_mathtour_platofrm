import telebot
from bot_head import father
from secret import TOKEN, TG_TOKEN, ADMINS, ADMIN_CHANNEL, PUBLIC_CHANNEL, HI_CHANNEL

tg_bot = telebot.TeleBot(TG_TOKEN)


def listener(messages):
    for m in messages:
        print(str(m))


tg_bot.set_update_listener(listener)


def id_for_tg(id):
    return "tg:" + id


@tg_bot.message_handler(commands=['solve'])  #help='Отправить решение в виде "solve ТЕМА ЗАДАЧА ОТВЕТ"
def tg_solve(ctx):
    print(ctx.chat.id, ctx.from_user.username, ctx.text)
    parts = ctx.text.strip().split(maxsplit=3)[1:]
    if len(parts) < 3:
        msg = "Недостаточно параметров"
        print(msg)
        tg_bot.send_message(ctx.chat.id, msg)
        return
    msg = father.solve(id_for_tg(str(ctx.chat.id)), *parts)
    print(msg)
    tg_bot.send_message(ctx.chat.id, msg)

@tg_bot.message_handler(commands=['points'])  #'Число очков команды')
def tg_points(ctx):
    print(ctx.chat.id, ctx.from_user.username, ctx.text)
    msg = father.points(id_for_tg(str(ctx.chat.id)))
    print(msg)
    tg_bot.send_message(ctx.chat.id, msg)

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

@tg_bot.message_handler(commands=['fio'])  #'Зарегистрировать ФИО')
def tg_fio(ctx):
    print(ctx.chat.id, ctx.from_user.username, ctx.text)
    parts = ctx.text.strip().split(maxsplit=1)[1:]
    if len(parts) == 0:
        msg = "Недостаточно параметров"
        print(msg)
        tg_bot.send_message(ctx.chat.id, msg)
        return
    ok, msg = father.fio(id_for_tg(str(ctx.chat.id)), parts[0])
    print(msg)
    tg_bot.send_message(ctx.chat.id, msg)

@tg_bot.message_handler(commands=['school'])  #'Зарегистрировать Школу')
def tg_school(ctx):
    print(ctx.chat.id, ctx.from_user.username, ctx.text)
    parts = ctx.text.strip().split(maxsplit=1)[1:]
    if len(parts) == 0:
        msg = "Недостаточно параметров"
        print(msg)
        tg_bot.send_message(ctx.chat.id, msg)
        return
    ok, msg = father.school(id_for_tg(str(ctx.chat.id)), parts[0])
    print(msg)
    tg_bot.send_message(ctx.chat.id, msg)

@tg_bot.message_handler(commands=['year'])  #'Зарегистрировать Класс обучения')
def tg_year(ctx):
    print(ctx.chat.id, ctx.from_user.username, ctx.text)
    parts = ctx.text.strip().split(maxsplit=1)[1:]
    if len(parts) == 0:
        msg = "Недостаточно параметров"
        print(msg)
        tg_bot.send_message(ctx.chat.id, msg)
        return
    ok, msg = father.year(id_for_tg(str(ctx.chat.id)), parts[0])
    print(msg)
    tg_bot.send_message(ctx.chat.id, msg)

@tg_bot.message_handler(commands=['city'])  #'Зарегистрировать Населенный пункт')
def tg_city(ctx):
    print(ctx.chat.id, ctx.from_user.username, ctx.text)
    parts = ctx.text.strip().split(maxsplit=1)[1:]
    if len(parts) == 0:
        msg = "Недостаточно параметров"
        print(msg)
        tg_bot.send_message(ctx.chat.id, msg)
        return
    ok, msg = father.city(id_for_tg(str(ctx.chat.id)), parts[0])
    print(msg)
    tg_bot.send_message(ctx.chat.id, msg)

@tg_bot.message_handler(commands=['region'])  #'Зарегистрировать Регион')
def tg_region(ctx):
    print(ctx.chat.id, ctx.from_user.username, ctx.text)
    parts = ctx.text.strip().split(maxsplit=1)[1:]
    if len(parts) == 0:
        msg = "Недостаточно параметров"
        print(msg)
        tg_bot.send_message(ctx.chat.id, msg)
        return
    ok, msg = father.region(id_for_tg(str(ctx.chat.id)), parts[0])
    print(msg)
    tg_bot.send_message(ctx.chat.id, msg)

@tg_bot.message_handler(commands=['phone'])  #'Зарегистрировать Телефон')
def tg_phone(ctx):
    print(ctx.chat.id, ctx.from_user.username, ctx.text)
    parts = ctx.text.strip().split(maxsplit=1)[1:]
    if len(parts) == 0:
        msg = "Недостаточно параметров"
        print(msg)
        tg_bot.send_message(ctx.chat.id, msg)
        return
    ok, msg = father.phone(id_for_tg(str(ctx.chat.id)), parts[0])
    print(msg)
    tg_bot.send_message(ctx.chat.id, msg)

@tg_bot.message_handler(commands=['trainer'])  #'Зарегистрировать Тренера')
def tg_trainer(ctx):
    print(ctx.chat.id, ctx.from_user.username, ctx.text)
    parts = ctx.text.strip().split(maxsplit=1)[1:]
    if len(parts) == 0:
        msg = "Недостаточно параметров"
        print(msg)
        tg_bot.send_message(ctx.chat.id, msg)
        return
    ok, msg = father.trainer(id_for_tg(str(ctx.chat.id)), parts[0])
    print(msg)
    tg_bot.send_message(ctx.chat.id, msg)

@tg_bot.message_handler(commands=['tour'])  #'Зарегистрировать Турнир')
def tg_tour(ctx):
    print(ctx.chat.id, ctx.from_user.username, ctx.text)
    parts = ctx.text.strip().split(maxsplit=1)[1:]
    if len(parts) == 0:
        msg = "Недостаточно параметров"
        print(msg)
        tg_bot.send_message(ctx.chat.id, msg)
        return
    ok, msg = father.tour(id_for_tg(str(ctx.chat.id)), parts[0])
    print(msg)
    tg_bot.send_message(ctx.chat.id, msg)

@tg_bot.message_handler(commands=['register'])  #'Отправить Анкету на проверку')
def tg_register(ctx):
    print(ctx.chat.id, ctx.from_user.username, ctx.text)
    ok, msg_user, msg_admin = father.register(id_for_tg(str(ctx.chat.id)))
    print(msg_user + '\n' + msg_admin)
    tg_bot.send_message(ctx.chat.id, msg_user)
    # if ok:
    #     tg_bot.get_channel(ADMIN_CHANNEL).send(msg_admin)
