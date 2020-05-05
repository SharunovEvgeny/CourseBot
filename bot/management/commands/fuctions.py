from .keyboards import ListOfButtons

async def get_text_help():
    text = f"""Вы можете:
    1)Посмотреть комнады для управления: /help

    2)Посмотреть матчи на сегодня /matches

    3)Посмотреть свою статистику /statistics(не работает)

    4)Посмотреть приглашённых друзей: /referrals

    5)Посмотреть свою ссылку для приглашений /link
"""
    return text
async def get_inline_first_keyboard():
   keyboard = ListOfButtons(
        text=["Matches", "Help", "Statistics"],
        callback=["matches", "help", "stat"],
        align=[1, 2]
    ).inline_keyboard
   return keyboard

