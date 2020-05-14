from django.utils import timezone

async def menu(BotUser, user, bot):
    return ("Это бот для <b>прогнозов на матчи по Dota 2 🥳</b>\n"
            f"Всего пользователей {BotUser.objects.count()}\n"
            "Посмотрите матчи на сегодня по кнопке <b>Матчи</b>\n"
            "Посмотрите статистику бота по кнопке <b>Статистика</b>\n"
            "Вы можете позвать друзей по своей ссылке:\n"
            f"https://t.me/{(await bot.me).username}?start={user.id}\n"
            f"Посмотрите реферралов по кнопке <b>Реферралы</b>")



async def link(BotUser, bot, call):
    return (f"Вы можете позвать друзей по своей ссылке:\n"
            f"https://t.me/{(await bot.me).username}?start={BotUser.objects.get(tg_id=call.message.chat.id).id}")


async def matches(game):
    return (f"{game.team1} <b>{game.predict}%</b>\n"
            f"<b>ФОРМАТ: {game.format}</b>\n"
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
    return (f"Всего ставок:  {statistic.all_bet_successful} / {statistic.bet_all}  {all}%\n\n"
            f"Надёжные ставки:  {statistic.safe_bet_successful} / {statistic.safe_bet_all}  {safe}%\n\n"
            f"Рискованные ставки:  {statistic.risk_bet_successful} / {statistic.risk_bet_all}  {risk}%\n\n"
            f"Непредсказуемые ставки:  {statistic.unpredictable_bet_successful} / {statistic.unpredictable_bet_all}  {unpred}%\n\n")
