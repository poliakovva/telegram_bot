from misc import dp, setup
from aiogram import executor

setup()

if __name__ == '__main__':
    executor.start_polling(dp)