from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

b1 = KeyboardButton('Список источников')
b2 = KeyboardButton('Добавить источник')
b3 = KeyboardButton('Удалить источник')
b4 = KeyboardButton('Назад')

kb_source = ReplyKeyboardMarkup(resize_keyboard=True)
kb_source.add(b1, b2, b3, b4)
