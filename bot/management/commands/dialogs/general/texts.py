from django.utils import timezone


async def menu(BotUser, user, bot):
    return ("Это бот для <b>прогнозов на матчи по Dota 2 🥳</b>\n"
            f"Всего пользователей {BotUser.objects.count()}\n\n"
            "Вы можете позвать друзей по своей ссылке:\n"
            f"https://tele.gg/{(await bot.me).username}?start={user.id}\n")


async def info(number):
    return f"<b>Страница №{number}</b>"


async def matches(game):
    return (f"{game.team1} <b>{game.predict}%</b>\n"
            f"<b>Формат: {game.format}</b>\n"
            f"{game.team2} <b>{100 - game.predict}%</b>\n"
            f"{game.tournament.name}\n"
            f"Начало: {timezone.localtime(game.starttime).strftime('%d.%m.%Y %H-%M')}\n\n\n")


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
    return (f"🔷Всего:  {statistic.all_bet_successful} / {statistic.bet_all}  {all}%\n\n"
            f"🟢Надёжные:  {statistic.safe_bet_successful} / {statistic.safe_bet_all}  {safe}%\n\n"
            f"🟡Рискованные:  {statistic.risk_bet_successful} / {statistic.risk_bet_all}  {risk}%\n\n"
            f"🔴Непредсказуемые:  {statistic.unpredictable_bet_successful} / {statistic.unpredictable_bet_all}  {unpred}%\n\n")
