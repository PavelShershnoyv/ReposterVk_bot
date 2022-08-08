from adding_source import answer_add
from aiogram import executor, types
from connecting_VK_account import answer_connect
from create_bot import dp
from database_queries import add_new_user, disconnect_vk_account, get_user_info
from deleting_source import answer_delete
from handler import get_info_about_current_account, get_list_of_sources, is_user_added, is_vk_account_connected, set_status_to_OFF, set_status_to_ON
from KeyBoards import kb_account_VK_off, kb_account_VK_on, kb_configuring_sources, kb_main
from post_handler import get_posts
import asyncio

start_message = '''
Привет! \U0001F44B

Я помогу сэкономить время на листании ленты ВКонтакте и буду сам присылать тебе новые посты от необходимых сообществ и пользователей, список источников ты сможешь настроить сам \U0001f440

Чтобы узнать, как пользоваться мной, жми кнопку «Помощь» \u2B07
'''

help_message = '''
Прежде чем VK_Reposter начнёт свою работу необходимо подключить аккаунт от социальной сети ВКонтакте. Это можно сделать перейдя в раздел «Аккаунт ВКонтакте». В этом же разделе в будущем вы сможете отключить свой аккаунт (если пожелаете его сменить), либо узнать, какой аккаунт подключён в данный момент. Без подключенного аккаунта VK_Reposter работать не может!

Раздел «Настройка источников» предназначен для изменения списка сообществ и пользователей, от которых вы хотите получать посты. Для добавления нового источника потребуется ссылка на него.

<b>Внимание!</b>\u2757\u2757\u2757
— VK_Reposter работает исключительно с сообществами и пользователями социальной сети ВКонтакте.
— При нахождении в каком-либо разделе меню посты не приходят. Это сделано для удобства при настройке бота. Поэтому всегда возвращайтесь в главное меню!
— Для корректной настройки бота всё взаимодействие с ним должно происходить при помощи встроенной мини-клавиатуры, расположенной под текстовым полем для отправки сообщения.
'''


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    id_tg = message.from_user.id

    if not is_user_added(id_tg):
        add_new_user(id_tg)

    await message.answer(start_message, reply_markup=kb_main)


@dp.message_handler()
async def other_commands(message: types.Message):
    id_tg = message.from_user.id

    if message.text == 'Помощь':
        await message.answer(help_message, parse_mode='html')

    if message.text == 'Аккаунт ВКонтакте':
        set_status_to_OFF(id_tg)
        kb = kb_account_VK_on if is_vk_account_connected(id_tg) else kb_account_VK_off
        await message.answer('Аккаунт ВКонтакте \u2B07', reply_markup=kb)

    if message.text == 'Настройка источников':
        if not is_vk_account_connected(id_tg):
            await message.answer('Для доступа к настройке источников необходимо подключить аккаунт ВКонтакте \u274C')
        else:
            set_status_to_OFF(id_tg)
            await message.answer('Настройка источников \u2B07', reply_markup=kb_configuring_sources)

    if message.text == 'Подключить аккаунт':
        await answer_connect(message)

    if message.text == 'Отключить аккаунт':
        disconnect_vk_account(id_tg)
        await message.answer('Аккаунт ВК отключён \u2705', reply_markup=kb_account_VK_off)

    if message.text == 'Текущий аккаунт':
        if not is_vk_account_connected(id_tg):
            await message.answer('Аккаунт не подключён \u274C')
        else:
            info_about_current_account = get_info_about_current_account(id_tg)
            photo = info_about_current_account['url_of_photo']
            first_name = info_about_current_account['first_name']
            last_name = info_about_current_account['last_name']
            screen_name = info_about_current_account['screen_name']
            await message.answer_photo(photo, f'{first_name} {last_name} (@{screen_name})')

    if message.text == 'Список источников':
        list_of_sources = get_list_of_sources(id_tg)
        group_list = list_of_sources['group_list']
        user_list = list_of_sources['user_list']
        groups = ' не добавлены' if not group_list else '\n- ' + '\n- '.join(group_list)
        users = ' не добавлены' if not user_list else '\n- ' + '\n- '.join(user_list)
        await message.answer(f'<b>Сообщества:</b>{groups}\n\n<b>Пользователи:</b>{users}', parse_mode='html')

    if message.text == 'Добавить источник':
        await answer_add(message)

    if message.text == 'Удалить источник':
        user_info = get_user_info(id_tg)
        if not user_info['group_ids'] and not user_info['user_ids']:
            await message.answer('Источники отсутствуют \u274C')
        else:
            await answer_delete(message)

    if message.text == 'Назад':
        set_status_to_ON(id_tg)
        await message.answer('Главное меню \u2B07', reply_markup=kb_main)


async def on_startup(x):
    asyncio.create_task(get_posts())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
