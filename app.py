from aiogram import executor, types
from create_bot import dp
from KeyBoard import kb_main, kb_source, kb_users_on, kb_users_off
from handler import is_user_added, set_status_to_ON, \
    set_status_to_OFF, is_vk_account_connected, get_info_about_current_account
from database_queries import add_new_user, disconnect_vk_account
from connect_VK import command_oauth


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
        await message.answer('Помощь скоро будет')
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



executor.start_polling(dp, skip_updates=True)
