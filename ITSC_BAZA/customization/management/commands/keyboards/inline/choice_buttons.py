from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_data import choose_callback

choice = InlineKeyboardMarkup(row_width=3)


name = InlineKeyboardButton(text = "Сменить имя", callback_data=choose_callback.new(
    what="name"
))
color = InlineKeyboardButton(text = "Сменить цвет", callback_data=choose_callback.new(
    what="color"
))
photo = InlineKeyboardButton(text = "Сменить фото", callback_data=choose_callback.new(
    what="photo"
))
role = InlineKeyboardButton(text = "Сменить роль", callback_data=choose_callback.new(
    what="role"
))
spec = InlineKeyboardButton(text = "Сменить специализацию", callback_data=choose_callback.new(
    what="spec"
))
course = InlineKeyboardButton(text = "Сменить курс", callback_data=choose_callback.new(
    what="course"
))
inf_about = InlineKeyboardButton(text = "Сменить информацию о себе", callback_data=choose_callback.new(
    what="inf_about"
))


choice.insert(name)
choice.insert(color)
choice.insert(photo)
choice.insert(role)
choice.insert(course)
choice.insert(spec)
choice.insert(inf_about)
