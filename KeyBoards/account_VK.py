from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_names = ['Подключить аккаунт', 'Отключить аккаунт', 'Текущий аккаунт', 'Назад']

kb_account_VK_on = ReplyKeyboardMarkup(resize_keyboard=True)
kb_account_VK_on.add(*[KeyboardButton(button_name) for button_name in button_names[1:]])

kb_account_VK_off = ReplyKeyboardMarkup(resize_keyboard=True)
kb_account_VK_off.add(*[KeyboardButton(button_name) for button_name in button_names[:1] + button_names[2:]])
