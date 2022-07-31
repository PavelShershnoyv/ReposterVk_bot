from state import Del
from create_bot import dp
from aiogram import types
from handler import get_list_of_sources, delete_source
from aiogram.dispatcher import FSMContext


@dp.message_handler(state=Del.D0)
async def answer_source(message: types.Message):
    sources = get_list_of_sources(message.from_user.id)
    groups = 'не подключены' if sources['group_list'] is None else ''.join([f'\n1{i}. {group}' for i, group in enumerate(sources['group_list'])])
    users = 'не подключены' if sources['user_list'] is None else ''.join([f'\n2{i}. {user}' for i, user in enumerate(sources['user_list'])])
    ans = f'''
    Сообщества: {groups}\n
Пользователи: {users}
    '''
    await message.answer(ans)
    await message.answer('Напишите через запятую номера источников, которые хотите удалить')
    await Del.D1.set()


@dp.message_handler(state=Del.D1)
async def del_source(message: types.Message, state: FSMContext):
    ans = delete_source(message.from_user.id, message.text)
    if ans == 'incorrect list':
        await message.answer('Номер(а) источника(ов) некорректен(ны)')
    elif ans == 'delete':
        await message.answer('Источник(и) успешно удален(ы)')
    await state.finish()
