from misc import dp, bot
from aiogram import types
import db


async def send_brick(brick_id: int, user_id: int):
    brick = db.get_brick_by_id(brick_id)
    kb = types.ReplyKeyboardRemove()
    if brick['keyboard']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        brick['keyboard'] = eval(brick['keyboard'])
        for row in brick['keyboard']:
            kb.add(*row)
    t = brick['message'].rsplit('\n')
    flag = 0
    for br in t:
        if brick['id'] == 2 and flag == 1:
            flag = False
            await bot.send_sticker(chat_id=user_id,
                                   sticker="CAACAgIAAxkBAAIC92DTuh1KQboSa4tbF29SnqrnN2UVAALSBgACYyviCQfizLuVT_n9HwQ")
        flag += 1
        await bot.send_message(chat_id=user_id,
                               text=br,
                               reply_markup=kb)


@dp.message_handler(commands=['start'])
async def start_cmd(m: types.Message):
    db.delete_user(m.from_user.id)
    user = db.get_or_create_user(tg_id=m.from_user.id,
                                 tg_name=m.from_user.full_name)
    await send_brick(user['state'], user['tg_id'])


@dp.message_handler(content_types=['text'])
async def text(m: types.Message):
    user = db.get_or_create_user(tg_id=m.from_user.id,
                                 tg_name=m.from_user.full_name)
    edges = db.get_edges_by_brick(user['state'])

    for edge in edges:
        if edge['trigger'].lower() == m.text.lower() or eval(edge['trigger']) == eval(m.text):
            db.set_user_state(user['tg_id'], edge['to'])
            await send_brick(edge['to'], user['tg_id'])
            db.add_log(tg_id=m.from_user.id, brick_id=user['state'], msg=m.text, is_trigger=1)
            return
    await m.answer("Я тебя не понимаю :(")
    db.add_log(tg_id=m.from_user.id, brick_id=user['state'], msg=m.text, is_trigger=0)


@dp.message_handler(content_types=['sticker'])
async def stickers(s: types.Message):
    await bot.send_sticker(chat_id=s.from_user.id,
                           sticker=s["sticker"]["file_id"])
