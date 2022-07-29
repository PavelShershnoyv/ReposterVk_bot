from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

b1 = KeyboardButton('Помощь')
b2 = KeyboardButton('Аккаунт ВКонтакте')
b3 = KeyboardButton('Настройка источников')

kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
kb_main.add(b1, b2, b3)
