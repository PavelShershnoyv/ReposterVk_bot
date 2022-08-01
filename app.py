import asyncio
import time
from create_bot import bot
from get_posts import get_post
from aiogram import executor, types
from create_bot import dp
from KeyBoard import kb_main, kb_source, kb_users_on, kb_users_off
from handler import is_user_added, set_status_to_ON, \
    set_status_to_OFF, is_vk_account_connected, get_info_about_current_account, get_list_of_sources
from database_queries import add_new_user, disconnect_vk_account
from connect_VK import command_oauth
from add_sourses import ans_source
from delete_sourses import answer_source


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    welcome = '''
    Привет!
    
Я помогу сэкономить время на листании ленты ВКонтакте и буду сам присылать тебе новые посты от необходимых сообществ и пользователей, список источников ты сможешь настроить сам \U0001f440

Чтобы узнать, как пользоваться мной, жми кнопку «Помощь» \u2B07
    '''
    id_tg = message.from_user.id
    if not is_user_added(id_tg):
        add_new_user(id_tg)
    await message.answer(f'{welcome}', reply_markup=kb_main)


@dp.message_handler()
async def commands_main(message: types.Message):
    if message.text == 'Помощь':
        await message.answer('''
        Прежде чем VK_Reposter начнёт свою работу необходимо подключить аккаунт от социальной сети ВКонтакте. Это можно сделать перейдя в раздел «Аккаунт ВКонтакте». В этом же разделе в будущем вы сможете отключить свой аккаунт (если пожелаете его сменить), либо узнать, какой аккаунт подключён в данный момент. Без подключенного аккаунта VK_Reposter работать не может!

Раздел «Настройка источников» предназначен для изменения списка сообществ и пользователей, от которых вы хотите получать посты. Для добавления нового источника потребуется ссылка на него.

Внимание!
— VK_Reposter работает исключительно с сообществами и пользователями социальной сети ВКонтакте.
— При нахождении в каком-либо разделе меню посты не приходят. Это сделано для удобства при настройке бота. Поэтому всегда возвращайтесь в главное меню!
— Для корректной настройки бота всё взаимодействие с ним должно происходить при помощи встроенной мини-клавиатуры, расположенной под текстовым полем для отправки сообщения.
''')
    if message.text == 'Аккаунт ВКонтакте':
        id_tg = message.from_user.id
        set_status_to_OFF(id_tg)
        kb = kb_users_off if is_vk_account_connected(id_tg) else kb_users_on
        await message.answer('\u2B07Аккаунт ВКонтакте\u2B07', reply_markup=kb)
    if message.text == 'Назад':
        set_status_to_ON(message.from_user.id)
        await message.answer('\u2B07Главное меню\u2B07', reply_markup=kb_main)
    if message.text == 'Настройка источников':
        set_status_to_OFF(message.from_user.id)
        await message.answer('\u2B07Настройка источников\u2B07', reply_markup=kb_source)
    if message.text == 'Подключить аккаунт':
        await command_oauth(message)
    if message.text == 'Отключить аккаунт':
        disconnect_vk_account(message.from_user.id)
        await message.answer('Аккаунт ВК отключен\u2705', reply_markup=kb_users_on)
    if message.text == 'Текущий аккаунт':
        id_tg = message.from_user.id
        if not is_vk_account_connected(id_tg):
            await message.answer('Аккаунт не подключен')
        else:
            info_about_current_account = get_info_about_current_account(message.from_user.id)
            await message.answer_photo(info_about_current_account['url_of_photo'],
                                       f"{info_about_current_account['first_name']} {info_about_current_account['last_name']}"
                                       f" (@{info_about_current_account['screen_name']})")
    if message.text == 'Добавить источник':
        await ans_source(message)
    if message.text == 'Список источников':
        lst = get_list_of_sources(message.from_user.id)
        communities = 'Нет добавленных' if lst['group_list'] is None else "\n".join(lst['group_list'])
        users = 'Нет добавленных' if lst['user_list'] is None else "\n".join(lst['user_list'])
        await message.answer(f'Сообщества: {communities} \n'
                             f'\nПользователи: {users}')
    if message.text == 'Удалить источник':
        await answer_source(message)



# async def is_enabled():
#   while True:
#     await bot.send_message(chat_id=1071458321, text='Hello')
#     await asyncio.sleep(3)


async def on_startup(x):
    asyncio.create_task(get_post())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
