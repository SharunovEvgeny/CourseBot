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
    a = len(f"{game.team1.name}") - 2
    b = len(f"{game.team2.name}") - 2
    texta = "\t" * a
    textb = "\t" * b
    return (f"<code>{game.team1} {game.format} {game.team2}\n</code>"
            f"<code>{game.predict}%{texta}{game.format}{textb}{100 - game.predict}%\n</code>"
            f"<code>{game.tournament.name}\n</code>"
            f"<code>Начало: {timezone.localtime(game.starttime).strftime('%d.%m.%Y %H-%M')}\n\n\n</code>")


async def stat(Statistic):
    statistic = Statistic.objects.get()
    safe, risk, unpred, all = 0, 0, 0, 0
    if statistic.bet_all != 0:
        all = ((statistic.all_bet_successful / statistic.bet_all) * 100) // 1
    if statistic.safe_bet_all != 0:
        safe = ((statistic.safe_bet_successful / statistic.safe_bet_all) * 100) // 1
    if statistic.risk_bet_all != 0:
        risk = ((statistic.risk_bet_successful / statistic.risk_bet_all) * 100) // 1
    if statistic.unpredictable_bet_all != 0:
        unpred = ((statistic.unpredictable_bet_successful / statistic.unpredictable_bet_all) * 100) // 1
    return (f"Всего ставок:                            {statistic.all_bet_successful} / {statistic.bet_all} {all}%\n"
            f"Надёжные ставки:                  {statistic.safe_bet_successful} / {statistic.safe_bet_all} {safe}%\n"
            f"Рискованных ставки:            {statistic.risk_bet_successful} / {statistic.risk_bet_all} {risk}%\n"
            f"Непредсказуемые ставки: {statistic.unpredictable_bet_successful} / {statistic.unpredictable_bet_all} {unpred}%\n")
