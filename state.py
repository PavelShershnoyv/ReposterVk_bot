from aiogram.dispatcher.filters.state import StatesGroup, State


class Oauth(StatesGroup):
    A0 = State()
    A1 = State()
    A2 = State()


class Add(StatesGroup):
    Q0 = State()
    Q1 = State()
    Q2 = State()


class Del(StatesGroup):
    D0 = State()
    D1 = State()
    D2 = State()
