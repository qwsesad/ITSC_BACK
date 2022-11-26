import logging
import os
import time
import re
from distutils.util import strtobool

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from django.core.management.base import BaseCommand
from django.conf import settings
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv, find_dotenv

from .keyboards.inline.choice_buttons import choice
from .states import Name, Course, Role, Spec, Inf_about, Color, Photo
from ...models import team_member
from asgiref.sync import sync_to_async
from aiogram.types import CallbackQuery

load_dotenv(find_dotenv())

# Считываем настройки
BOT_TOKEN = os.getenv('BOT_TOKEN')
AUTH = strtobool(os.getenv('AUTH'))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message: types.message):
    await show_menu(message)

@dp.message_handler(commands=['menu'])
async def show_menu(message: types.message):
    if (await check_data_base(message)):
        await message.answer(
            text=f"Добро пожаловать в основное меню.\nЗдесь вы можете персонализировать свою карточку:)",
            reply_markup=choice)


async def check_data_base(message: types.Message):
    try:
        p, obj = await sync_to_async(team_member.objects.get_or_create, thread_sensitive=True)(
            tg_id=message.from_user.id)
        if p.tg_name != message.from_user.username:
            p.tg_name = message.from_user.username
            await sync_to_async(p.save, thread_sensitive=True)()
        return True
    except:
        return False


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Отменено.', reply_markup=types.ReplyKeyboardRemove())



@dp.callback_query_handler(text_contains="name")
async def change_name(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.answer("Введите новое ФИО")
    await Name.First.set()


@dp.callback_query_handler(text_contains="course")
async def change_сourse(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.answer("Введите новый курс")
    await Course.First.set()


@dp.callback_query_handler(text_contains="role")
async def change_role(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.answer("Введите новую роль")
    await Role.First.set()


@dp.callback_query_handler(text_contains="spec")
async def change_spec(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.answer("Введите новую специализацию")
    await Spec.First.set()


@dp.callback_query_handler(text_contains="inf_about")
async def change_inf_about(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.answer("Введите новую дополнительную информацию о себе")
    await Inf_about.First.set()


@dp.callback_query_handler(text_contains="color")
async def change_color(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("red", "blue", "green", "default")

    await call.message.answer("Выберите цвет для вашей карточки", reply_markup=markup)
    await Color.First.set()


@dp.callback_query_handler(text_contains="photo")
async def change_photo(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")


    await call.message.answer("Отправьте вашу фотографию")
    await Photo.First.set()


@dp.message_handler(state=Name.First)
async def answer_NFirst(message: types.Message, state: FSMContext):
    answer = message.text
    bd = await sync_to_async(team_member.objects.get, thread_sensitive=True)(tg_id=message.from_user.id)
    bd.name = answer
    await sync_to_async(bd.save, thread_sensitive=True)()
    await message.answer("ФИО успешно изменено")
    await message.answer(text=f"Добро пожаловать в основное меню.\nЗдесь вы можете персонализировать свою карточку:)",
                         reply_markup=choice)
    await state.finish()


@dp.message_handler(lambda message: not message.text.isdigit() or int(message.text) <=0 or int(message.text) > 5, state=Course.First)
async def process_age_invalid(message: types.Message):
    return await message.reply("Введите, пожалуйста корректый курс")


@dp.message_handler(state=Course.First)
async def answer_CourseFirst(message: types.Message, state: FSMContext):
    answer = int(message.text)
    bd = await sync_to_async(team_member.objects.get, thread_sensitive=True)(tg_id=message.from_user.id)
    bd.course = answer
    await sync_to_async(bd.save, thread_sensitive=True)()
    await message.answer("Курс успешно изменён")
    await message.answer(text=f"Добро пожаловать в основное меню.\nЗдесь вы можете персонализировать свою карточку:)",
                         reply_markup=choice)
    await state.finish()


@dp.message_handler(state=Role.First)
async def answer_RoleFirst(message: types.Message, state: FSMContext):
    answer = message.text
    bd = await sync_to_async(team_member.objects.get, thread_sensitive=True)(tg_id=message.from_user.id)
    bd.role = answer
    await sync_to_async(bd.save, thread_sensitive=True)()
    await message.answer("Роль успешно изменена")
    await message.answer(text=f"Добро пожаловать в основное меню.\nЗдесь вы можете персонализировать свою карточку:)",
                         reply_markup=choice)
    await state.finish()


@dp.message_handler(state=Spec.First)
async def answer_SpecFirst(message: types.Message, state: FSMContext):
    answer = message.text
    bd = await sync_to_async(team_member.objects.get, thread_sensitive=True)(tg_id=message.from_user.id)
    bd.spec = answer
    await sync_to_async(bd.save, thread_sensitive=True)()
    await message.answer("Специализация успешно изменена")
    await message.answer(text=f"Добро пожаловать в основное меню.\nЗдесь вы можете персонализировать свою карточку:)",
                         reply_markup=choice)
    await state.finish()


@dp.message_handler(state=Inf_about.First)
async def answer_InfAboutFirst(message: types.Message, state: FSMContext):
    answer = message.text
    bd = await sync_to_async(team_member.objects.get, thread_sensitive=True)(tg_id=message.from_user.id)
    bd.inf_about = answer
    await sync_to_async(bd.save, thread_sensitive=True)()
    await message.answer("Дополнительная информация успешно изменена")
    await message.answer(text=f"Добро пожаловать в основное меню.\nЗдесь вы можете персонализировать свою карточку:)",
                         reply_markup=choice)
    await state.finish()



@dp.message_handler(lambda message: message.text not in ["red", "blue", "green", "default"], state=Color.First)
async def process_gender_invalid(message: types.Message):
    return await message.reply("Плохой цвет) Выберите один из наших")


@dp.message_handler(state=Color.First)
async def answer_Color(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardRemove()
    answer = message.text
    bd = await sync_to_async(team_member.objects.get, thread_sensitive=True)(tg_id=message.from_user.id)
    bd.color = answer
    await sync_to_async(bd.save, thread_sensitive=True)()
    await message.answer("Цвет успешно изменён", reply_markup=markup)
    await message.answer(text=f"Добро пожаловать в основное меню.\nЗдесь вы можете персонализировать свою карточку:)",
                         reply_markup=choice)
    await state.finish()


@dp.message_handler(state=Photo.First, content_types=['photo'])
async def answer_Photo(message: types.Message, state: FSMContext):

    regex = re.compile(fr'{message.from_user.id}_.*')
    for root, dirs, files in os.walk(f'{settings.MEDIA_ROOT}/images/'):
        for file in files:
            if regex.match(file):
                print(file)
                os.remove(f'{settings.MEDIA_ROOT}/images/{file}')

    t = time.time()
    await message.photo[-1].download(f'{settings.MEDIA_ROOT}/images/{message.from_user.id}_{t}_photo.jpg')
    bd = await sync_to_async(team_member.objects.get, thread_sensitive=True)(tg_id=message.from_user.id)
    bd.photo = f'/images/{message.from_user.id}_{t}_photo.jpg'
    await sync_to_async(bd.save, thread_sensitive=True)()
    await message.answer("Фото успешно изменено")
    await message.answer(text=f"Добро пожаловать в основное меню.\nЗдесь вы можете персонализировать свою карточку:)",
                         reply_markup=choice)
    await state.finish()


class Command(BaseCommand):
    # Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        executor.start_polling(dp, skip_updates=True)
