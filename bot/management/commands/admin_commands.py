from django.db.models import F, Func

from bot.models import Game, Tournament, Team, GameNow
from aiogram import types
from .load_all import bot, dp
from .config import admin_id
from .fuctions import game_predict
from datetime import timedelta


@dp.message_handler(user_id=admin_id, commands=["power"])
async def calculate_power(message: types.message):
    games = Game.objects.all()
    Team.objects.all().update(power=0)
    for game in games:
        tier = game.tournament.tier
        point1 = game.team1_score
        point2 = game.team2_score
        if tier == "7Qualifier":
            game.team1.power += point1 * 2
            game.team2.power += point2 * 2
        elif tier == "5Monthly":
            game.team1.power += point1 * 1
            game.team2.power += point2 * 1
        elif tier == "7Showm." or tier == "6Weekly":
            game.team1.power += point1 * 0.5
            game.team2.power += point2 * 0.5
        elif tier == "Minor":
            game.team1.power += point1 * 5
            game.team2.power += point2 * 5
        elif tier == "Major":
            game.team1.power += point1 * 10
            game.team2.power += point2 * 10
        elif tier == "Premier":
            game.team1.power += point1 * 20
            game.team2.power += point2 * 20
        game.team1.save()
        game.team2.save()
    teams = Team.objects.order_by('power')
    for team in teams:
        try:
            team.power = team.power / (team.team1_game.count() + team.team2_game.count())
        except:
            team.power = team.power / 1
        team.save()
    teams = Team.objects.order_by('power')
    for team in teams:
        await message.answer(f"{team.name}  {team.power}")

@dp.message_handler(user_id=admin_id, commands=["tournament"])
async def calculate_power(message: types.message):
    tournaments = Tournament.objects.all()
    for tour in tournaments:
        await message.answer(f"{tour.name} {tour.tier}")


@dp.message_handler(user_id=admin_id, commands=["update_power"])
async def update_power(message: types.message):
    games = GameNow.objects.all()
    for game in games:
        game.predict = await game_predict(game)
        game.save()
    await message.answer("Силы команд успешно обновлены")
