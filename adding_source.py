from aiogram import types
from aiogram.dispatcher import FSMContext
from create_bot import dp
from handler import add_source
from states import Addition


@dp.message_handler(state=Addition.Waiting)
async def answer_add(message: types.Message):
    await message.answer('Отправьте ссылку на источник, который хотите добавить')
    await Addition.Link.set()


@dp.message_handler(state=Addition.Link)
async def add(message: types.Message, state: FSMContext):
    result = add_source(message.from_user.id, message.text)

    answer = {
        None: 'Некорректная ссылка \u274C',
        'invalid source': 'Ссылка не ведёт на сообщество или пользователя ВК \u274C',
        'repeat group': 'Данное сообщество уже добавлено \u274C',
        'repeat user': 'Данный пользователь уже добавлен \u274C',
        'closed group': 'Данное сообщество закрыто \u274C\nДля добавления необходимо быть участником данного сообщества',
        'closed user': 'Профиль данного пользователя закрыт \u274C\nДля добавления необходимо добавить данного пользователя в друзья',
        'group': 'Сообщество успешно добавлено \u2705',
        'user': 'Пользователь успешно добавлен \u2705'
    }

    await message.answer(answer[result])
    await state.finish()
