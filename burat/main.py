from discord_bot import discord_bot
from tg_bot import tg_bot
from secret import TOKEN

import threading


def run_ds():
    discord_bot.run(TOKEN)


def run_tg():
    try:
        tg_bot.polling(none_stop=True, )
    except Exception as e:
        print(str(e))


def main():
    ds_thr = threading.Thread(target=run_ds)
    tg_thr = threading.Thread(target=run_tg)
    ds_thr.start()
    tg_thr.start()


if __name__ == '__main__':
    main()
