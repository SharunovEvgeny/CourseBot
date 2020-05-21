from django.utils import timezone
from bot.prediction.functions import get_last_games


async def team_info(team):
    last_games_text = ""
    for game in get_last_games(team, 3):
        last_games_text += (f"{game.team1}\n"
                            f"Счёт: <b>{game.team1_score}:{game.team2_score}</b>\n"
                            f"{game.team2}\n"
                            f"{game.tournament}\n"
                            f"Начало: {timezone.localtime(game.starttime).strftime('%d.%m.%Y %H-%M')}\n\n\n")

    return (f"<b>{team.name}</b>\n"
            f"<b>Сила:</b> {round(team.power,2)}\n\n"
            f"<b>Последние 3 матча:</b>\n\n"
            f"{last_games_text}")
