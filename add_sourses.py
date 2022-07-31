from create_bot import dp
from state import Add
from aiogram import types
from aiogram.dispatcher import FSMContext
from handler import add_source


@dp.message_handler(state=Add.Q0)
async def ans_source(message: types.Message):
    await message.answer('Отправьте ссылку источника, который хотите добавить:')

    await Add.Q1.set()


@dp.message_handler(state=Add.Q1)
async def check_source(message: types.Message, state: FSMContext):
    source = add_source(message.from_user.id, message.text)

    if source is None:
        await message.answer('Некорректная ссылка')
    elif source == 'invalid source':
        await message.answer('Отправленная ссылка не указывает на сообщество или пользователя')
    elif source == 'repeat user':
        await message.answer('Данный пользователь уже добавлен')
    elif source == 'repeat group':
        await message.answer('Данное сообщество уже добавлено')
    elif source == 'closed user':
        await message.answer('Профиль данного пользователя закрыт. '
                             'Для добавления необходимо добавить этот профиль в друзья')
    elif source == 'closed group':
        await message.answer('Данное сообщество закрыто. Для добавления необходимо вступить в него')
    elif source == 'user':
        await message.answer('Пользователь успешно добавлен \u2705')
    elif source == 'group':
        await message.answer('Сообщество успешно добавлено \u2705')
    await state.finish()
