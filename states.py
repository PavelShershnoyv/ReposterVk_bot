from aiogram.dispatcher.filters.state import State, StatesGroup


class Addition(StatesGroup):
    Waiting = State()
    Link = State()


class Authorization(StatesGroup):
    Waiting = State()
    Link = State()


class Deletion(StatesGroup):
    Waiting = State()
    Numbers = State()
