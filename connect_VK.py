from state import Oauth
from aiogram import types
from aiogram.dispatcher import FSMContext
from KeyBoard import kb_users_off
from create_bot import dp
from config import AUTHORIZATION_LINK
from handler import get_id_and_token_vk
from database_queries import connect_vk_account


@dp.message_handler(state=Oauth.A0)
async def command_oauth(message: types.Message):
    await message.answer(f'Перейдите по ссылке, указанной ниже, и разрешите доступ к своей странице ВКонтакте. После этого необходимо скопировать адрес (URL) страницы, на которой вы окажетесь. \n\n'
                         f'{AUTHORIZATION_LINK}')
    await Oauth.A1.set()


@dp.message_handler(state=Oauth.A1)
async def check_code(message: types.Message, state: FSMContext):
    id_and_token = get_id_and_token_vk(message.text)
    if id_and_token == 'invalid link':
        await message.answer('Была отправлена неправильная ссылка')
    elif id_and_token == 'invalid code':
        await message.answer('Попробуйте авторизоваться ещё раз')
    else:
        connect_vk_account(message.from_user.id, id_and_token['id'], id_and_token['token'])
        await message.answer('Аккаунт ВК подключен \u2705', reply_markup=kb_users_off)
    await state.finish()
