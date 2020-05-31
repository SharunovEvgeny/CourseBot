import importlib
import inspect

import os
import random
import sys

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup
from django.db.models import F

from . import texts, keyboards
from ...load_all import bot, dp
from bot.models import BotUser, GameNow, Game, Statistic, Team
from bot.management.commands.modules.filters import *
from datetime import timedelta
from django.utils import timezone

from ...modules.edit_or_send_message import edit_or_send_message

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
OFFSET = 3

photos = ['http://images.vfl.ru/ii/1590104410/94ebcbe6/30582958.gif',
          'http://images.vfl.ru/ii/1590104482/f3c45b80/30582959.gif',
          'http://images.vfl.ru/ii/1590104502/9f07de2e/30582960.gif',
          'http://images.vfl.ru/ii/1590104525/89eb79c7/30582963.gif',
          'http://images.vfl.ru/ii/1590104540/bb79d252/30582964.gif']


@dp.message_handler(commands=['start'], state='*')
async def start_(message: types.Message):
    user, is_created_now = BotUser.objects.get_or_create(tg_id=message.chat.id)
    text = ""
    # Если пользователь новый то создаёт его в базе данных
    if is_created_now:
        user.referral = message.get_args() if message.get_args() else None
        user.username = message.from_user.username
        user.full_name = message.from_user.full_name
        user.save()
        text += f"Здраствуйте! {user.full_name}\n"
    else:
        text += f"С возвращением! {user.full_name}\n"
    text += await texts.menu(BotUser, user, bot)
    await edit_or_send_message(bot, message, text=text, kb=keyboards.menu, photo=random.choice(photos), disable_web=True)


@dp.callback_query_handler(Button("menu"), state='*')
async def menu_(call: CallbackQuery):
    await edit_or_send_message(bot, call,
                               text=await texts.menu(BotUser, BotUser.objects.get(tg_id=call.message.chat.id), bot),
                               kb=keyboards.menu,
                               photo=random.choice(photos),
                               disable_web=True)


@dp.callback_query_handler(Button("info"), state='*')
async def info_(call: CallbackQuery, state: FSMContext, teams=None, team_id=None):
    if not teams:
        teams = Team.objects.order_by('-power')
    if not team_id:
        team_id = 0
    await edit_or_send_message(bot, call, text=await texts.info(team_id // 9 + 1),
                               kb=await keyboards.info(teams, team_id))
    await call.answer()


@dp.callback_query_handler(Button("ref"), state='*')
async def referrals_(call: CallbackQuery):
    cur_user_id = BotUser.objects.get(tg_id=call.message.chat.id).id
    n = '\n'
    text = f"Ваши реффералы:\n" \
           f"{f'{n}'.join([f'@{user.username}' if user.username else user.full_name for user in BotUser.objects.all() if user.referral == cur_user_id])}"
    await edit_or_send_message(bot, call, text=text, kb=keyboards.back)
    await call.answer()


@dp.callback_query_handler(Button("stat"), state='*')
async def statistic(call: CallbackQuery):
    await edit_or_send_message(bot, call, text=await texts.stat(Statistic), kb=keyboards.back)
    await call.answer()


async def get_game_id(state):
    game_id = (await state.get_data()).get('game_id')
    if not game_id:
        await state.set_data({'game_id': 0})
        game_id = 0
    return game_id


def get_games_now(game_id):
    return GameNow.objects.filter(starttime__range=(timezone.now() - timedelta(hours=5),
                                                    timezone.now() + timedelta(hours=20))).order_by('starttime')


@dp.callback_query_handler(Button("matches"), state='*')
async def matches_(call, state: FSMContext, games=None):
    game_id = await get_game_id(state)
    games = get_games_now(game_id)[game_id:][:OFFSET] if not games else games[game_id:][:OFFSET]
    text = f"<b>Страница №{(game_id // OFFSET) + 1}</b>\n"
    text += "".join([await texts.matches(game) for game in games])
    await edit_or_send_message(bot, call, text=text, kb=keyboards.matches)
    await call.answer()


@dp.callback_query_handler(Button("next"), state='*')
async def next_(call, state: FSMContext):
    game_id = await get_game_id(state)
    games = get_games_now(game_id)
    game_id = game_id + OFFSET if game_id < len(games) - OFFSET else 0
    await state.set_data({'game_id': game_id})
    await matches_(call, state, games)
    await call.answer()


@dp.callback_query_handler(Button("prev"), state='*')
async def prev_(call, state: FSMContext):
    game_id = await get_game_id(state)
    games = get_games_now(game_id)
    game_id = game_id - OFFSET if game_id - OFFSET >= 0 else len(games) - 1 - (len(games) - 1) % OFFSET
    await state.set_data({'game_id': game_id})
    await matches_(call, state, games)
    await call.answer()


@dp.message_handler()
async def delete_any_msg(message: types.Message):
    await message.delete()
