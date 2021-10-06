from aiogram import Bot, Dispatcher
import sqlite3
import config

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

con = sqlite3.connect(config.DB_PATH)
con.row_factory = dict_factory  
cur = con.cursor()

bot = Bot(config.BOT_HASH)
dp = Dispatcher(bot)

def setup():
    import handlers