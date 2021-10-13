from aiogram.dispatcher.filters.state import StatesGroup, State


class State_t(StatesGroup):
    all = State()
    creater = State()
    add_towar = State()
    delete_towar = State()