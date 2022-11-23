import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv, find_dotenv
from customization.models import team_member


load_dotenv(find_dotenv())


# Считываем настройки
BOT_TOKEN = os.getenv('BOT_TOKEN')
AUTH = os.getenv('AUTH')


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    if AUTH:
        try:
            obj = team_member.objects.get(tg_id = message.from_user.id)
        except team_member.DoeNotExist:
            await message.reply(f"Извини, тебя нет в базе.\n Если ты - член команды, обратись, пожалуйста, к администратору.")
    else:
        obj = team_member.objects.get_or_create(tg_id = message.from_user.id)

async def min():
    executor.start_polling(dp, skip_updates=True)
