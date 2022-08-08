from aiogram import types
from aiogram.dispatcher import FSMContext
from create_bot import dp
from handler import delete_source, get_list_of_sources
from states import Deletion


@dp.message_handler(state=Deletion.Waiting)
async def answer_delete(message: types.Message):
    sources = get_list_of_sources(message.from_user.id)
    groups = 'не подключены' if not sources['group_list'] else ''.join([f'\n1{i}. {group}' for i, group in enumerate(sources['group_list'])])
    users = 'не подключены' if not sources['user_list'] else ''.join([f'\n2{i}. {user}' for i, user in enumerate(sources['user_list'])])
    answer = f'<b>Сообщества:</b> {groups}\n\n<b>Пользователи:</b> {users}'

    await message.answer(answer, parse_mode='html')
    await message.answer('Перечислите через запятую номера источников, которые хотите удалить')
    await Deletion.Numbers.set()


@dp.message_handler(state=Deletion.Numbers)
async def delete(message: types.Message, state: FSMContext):
    result = delete_source(message.from_user.id, message.text)

    answer = {
        'delete': 'Источники успешно удалены \u2705',
        'incorrect list': 'Номера источников некорректны \u274C'
    }

    await message.answer(answer[result])
    await state.finish()
