from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_names = ['Помощь', 'Аккаунт ВКонтакте', 'Настройка источников']

kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
kb_main.add(*[KeyboardButton(button_name) for button_name in button_names])
