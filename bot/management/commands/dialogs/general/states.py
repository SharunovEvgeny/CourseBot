from aiogram.dispatcher.filters.state import State, StatesGroup


class General(StatesGroup):
    start = State()
    help = State()
    link = State()
    referrals = State()
    matches = State()