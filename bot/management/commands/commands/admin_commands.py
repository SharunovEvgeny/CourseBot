from bot.models import Game, Tournament, Team, GameNow, Coefficient, BotUser
from aiogram import types
from bot.management.commands.load_all import dp
from bot.prediction.functions import game_predict, calculate_all_teams_power


async def is_admin(tg_id):
    return BotUser.objects.get(tg_id=tg_id).is_admin


@dp.message_handler(lambda message: is_admin(message.chat.id), commands=["power"])
async def calculate_power_(message: types.message):
    await calculate_all_teams_power()
    teams = Team.objects.all()
    for team in teams:
        await message.answer(f"{team.name}  {team.power}")


@dp.message_handler(lambda message: is_admin(message.chat.id), commands=["tournament"])
async def send_tournaments(message: types.message):
    tournaments = Tournament.objects.all()
    for tour in tournaments:
        await message.answer(f"{tour.name} {tour.tier}")


@dp.message_handler(lambda message: is_admin(message.chat.id), commands=["update_power"])
async def update_power(message: types.message):
    games = GameNow.objects.all()
    coef = Coefficient.objects.get(name='joint_games_cof')
    for game in games:
        game.predict = await game_predict(game, coef)
        game.save()
    await message.answer("Силы команд успешно обновлены")
