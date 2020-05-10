from django.utils import timezone


async def start(BotUser, user, bot):
    return (", это бот для <b>прогнозов на матчи по Dota 2 🥳</b>\n"
            f"Всего пользователей {BotUser.objects.count()}\n"
            "Вы можете позвать друзей по своей ссылке:\n"
            f"https://t.me/{(await bot.me).username}?start={user.id}\n\n"
            "Посмотрите матчи на сегодня: /matches")


async def help():
    return ("Вы можете:\n"
            "1)Посмотреть команды для управления: /help\n\n"
            "2)Матчи на сегодня: /matches\n\n"
            "3)Посмотреть статистику: /statistics(не работает)\n\n"
            "4)Приглашённые друзей: /referrals\n\n"
            "5)Ваша ссылка для приглашений: /link")


async def link(BotUser, bot, msg_or_clb):
    return (f"Вы можете позвать друзей по своей ссылке:\n"
            f"https://t.me/{(await bot.me).username}?start={BotUser.objects.get(tg_id=msg_or_clb.chat.id).id}")


async def matches(game):
    return (f"{game.tournament.name}\n"
            f"Начало: {timezone.localtime(game.starttime).strftime('%d.%m.%Y %H-%M')}\n"
            f"{game.team1} {game.format} {game.team2}\n"
            f"{game.predict}%   {game.format}   {100 - game.predict}%\n\n\n")
