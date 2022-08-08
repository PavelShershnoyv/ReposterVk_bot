from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_names = ['Список источников', 'Добавить источник', 'Удалить источник', 'Назад']

kb_configuring_sources = ReplyKeyboardMarkup(resize_keyboard=True)
kb_configuring_sources.add(*[KeyboardButton(button_name) for button_name in button_names])
