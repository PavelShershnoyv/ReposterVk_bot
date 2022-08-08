from aiogram import types
from aiogram.dispatcher import FSMContext
from config import AUTHORIZATION_LINK
from create_bot import dp
from database_queries import connect_vk_account
from handler import get_id_and_token_vk
from KeyBoards import kb_account_VK_on
from states import Authorization


@dp.message_handler(state=Authorization.Waiting)
async def answer_connect(message: types.Message):
    await message.answer(f'Перейдите по ссылке, указанной ниже, и разрешите доступ к своей странице ВКонтакте. После этого необходимо скопировать URL-адрес страницы, на которой вы окажетесь.\n\n{AUTHORIZATION_LINK}')
    await Authorization.Link.set()


@dp.message_handler(state=Authorization.Link)
async def connect(message: types.Message, state: FSMContext):
    id_and_token = get_id_and_token_vk(message.text)

    if id_and_token == 'invalid link':
        await message.answer('Некорректная ссылка \u274C')
    elif id_and_token == 'invalid code':
        await message.answer('Попробуйте ещё раз \u274C')
    else:
        connect_vk_account(message.from_user.id, id_and_token['id'], id_and_token['token'])
        await message.answer('Аккаунт ВК подключён \u2705', reply_markup=kb_account_VK_on)

    await state.finish()
