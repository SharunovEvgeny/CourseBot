from .keyboards import ListOfButtons
from bot.models import GameNow, Team, Game


async def get_text_help():
    text = f"""Вы можете:
    1)Посмотреть комнады для управления: /help

    2)Матчи на сегодня /matches

    3)Посмотреть статистику /statistics(не работает)

    4)Приглашённые друзей: /referrals

    5)Ваша ссылка для приглашений /link
"""
    return text


async def get_inline_first_keyboard():
    keyboard = ListOfButtons(
        text=["Matches", "Help", "Statistics"],
        callback=["matches", "help", "stat"],
        align=[1, 2]
    ).inline_keyboard
    return keyboard


async def game_predict(game: GameNow):
    first_joint_games = game.team1.team1_game.filter(team2=game.team2)
    second_joint_games = game.team2.team2_game.filter(team2=game.team1)
    joint_games_cof = 0
    score1 = 0
    score2 = 0
    for gm in first_joint_games:
        score1 += gm.team1_score
        score2 += gm.team2_score
    for gm in second_joint_games:
        score1 += gm.team2_score
        score2 += gm.team1_score
    try:
        joint_games_cof = (score1 / (score1 + score2)) * 15
    except:
        joint_games_cof=0
    if score2 > score1:
        joint_games_cof *= (-1)
    elif score2 == score1:
        joint_games_cof = 0
    predict = ((game.team1.power / (game.team1.power + game.team2.power) * 100) + joint_games_cof) // 1
    return predict
