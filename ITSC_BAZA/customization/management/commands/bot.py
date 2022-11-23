import os
from distutils.util import strtobool

from django.core.management.base import BaseCommand
from django.conf import settings
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv, find_dotenv

from .keyboards.inline.choice_buttons import choice
from ...models import team_member
from asgiref.sync import sync_to_async
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle

load_dotenv(find_dotenv())


# Считываем настройки
BOT_TOKEN = os.getenv('BOT_TOKEN')
AUTH = strtobool(os.getenv('AUTH'))


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['menu'])
async def show_menu(message: types.message):
    if (await check_data_base(message)):
        await message.answer(text=f"Добро пожаловать в основное меню.\nЗдесь вы можете персонализировать свою карточку:)",
                            reply_markup=choice)


async def check_data_base(message: types.Message):
    try:
        p, obj = await sync_to_async(team_member.objects.get_or_create, thread_sensitive=True)(tg_id=message.from_user.id, tg_name=message.from_user.username)
        return True
    except:
        return False



class Command(BaseCommand):
    # Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        executor.start_polling(dp, skip_updates=True)
