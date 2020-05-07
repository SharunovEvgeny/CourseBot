from bot.management.commands.dialogs.general.handlers import *
from bot.management.commands.modules.custom_state import CustomState
from bot.management.commands.modules.keyboard import KeyboardInline


class General(StatesGroup):
    start = CustomState(
        message_text=None,
        kb=KeyboardInline([{"Матчи": "matches", "Статистика": "stat"},
                           {"Помощь": "help"}]).get(),
        func=register_user
    )
    help = CustomState(
        message_text="Вы можете:\n"
                     "1)Посмотреть комнады для управления: /help\n\n"
                     "2)Матчи на сегодня: /matches\n\n"
                     "3)Посмотреть статистику: /statistics(не работает)\n\n"
                     "4)Приглашённые друзей: /referrals\n\n"
                     "5)Ваша ссылка для приглашений: /link",
        kb=start.kb,
    )
    link = CustomState(
        message_text=None,
        kb=KeyboardInline([{"Назад": "back"}]).get(),
        prev=start,
    )
    referrals = CustomState(
        message_text=None,
        kb=KeyboardInline([{"Назад": "back"}]).get(),
        prev=start,
    )
    matches = CustomState(
        message_text=None,
        kb=lambda x: KeyboardInline([{f"{x[0]}": "None"}, {f"{x[1]}": "None"}, {f"{x[2]}": "None"},
                                     {"<-": "prev", "->": "next"},
                                     {"Назад": "back"}]).get(),
        prev=start,
    )
