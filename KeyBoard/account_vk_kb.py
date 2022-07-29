from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


b1 = KeyboardButton('Подключить аккаунт')
b2 = KeyboardButton('Текущий аккаунт')
b3 = KeyboardButton('Назад')
b4 = KeyboardButton('Отключить аккаунт')


kb_users_on = ReplyKeyboardMarkup(resize_keyboard=True)
kb_users_on.add(b1, b2, b3)

kb_users_off = ReplyKeyboardMarkup(resize_keyboard=True)
kb_users_off.add(b4, b2, b3)
