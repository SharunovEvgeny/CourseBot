from django.utils import timezone

from bot.models import Team
from bot.prediction.functions import get_last_games


async def team_info(team):
    last_games_text = ""
    for game in get_last_games(team, 3):
        last_games_text += (f"{game.team1}\n"
                            f"Счёт: <b>{game.team1_score}:{game.team2_score}</b>\n"
                            f"{game.team2}\n"
                            f"{'⭕️ Ставки нет.' if not game.predict else '✅ Ставка сыграла.' if (game.team1_score > game.team2_score and game.predict>50) or (game.team1_score < game.team2_score and game.predict<50) or (game.team1_score == game.team2_score and game.predict==50) else '❌ Ставка проиграна.'}\n"
                            f"{game.tournament}\n"
                            f"Начало: {timezone.localtime(game.starttime).strftime('%d.%m.%Y %H-%M')}\n\n\n")

    team_power_id = list(Team.objects.all().order_by('-power')).index(team) + 1

    return (f"<b>{team.name}</b>\n"
            f"Место команды по силе: <b>{team_power_id}</b>\n"
            f"<b>Сила:</b> {round(team.power,2)}\n\n"
            f"<b>Последние 3 матча:</b>\n\n"
            f"{last_games_text}")
