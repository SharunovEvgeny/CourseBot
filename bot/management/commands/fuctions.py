from .keyboards import ListOfButtons

async def get_text_help():
    text = f"""Вы можете:
    1)Посмотреть комнады для управления: /help

    2)Посмотреть матчи на сегодня /mathes

    3)Посмотреть свою статистику /statistics

    4)Посмотреть приглашённых друзей: /referrals

    5)Посмотреть свою ссылку для приглашений /link

    6)Выбрать язык /set_language
"""
    return text
async def get_inline_first_keyboard():
   keyboard = ListOfButtons(
        text=["Mathes", "Help", "Statistics"],
        callback=["mathes", "help", "stat"],
        align=[1, 2]
    ).inline_keyboard
   return keyboard

async def get_inline_language_keyboard():
   keyboard = ListOfButtons(
        text=["English", "Русский"],
        callback=["en", "ru"],
        align=[1, 1]
    ).inline_keyboard
   return keyboard
