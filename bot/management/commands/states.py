from aiogram.dispatcher.filters.state import State,StatesGroup

class Mailing(StatesGroup):
    Text=State()
    Language=State()
