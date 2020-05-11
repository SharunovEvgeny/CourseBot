import importlib
import inspect

import os
import sys

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup

from . import texts, keyboards
from ...load_all import bot, dp
from bot.models import BotUser, GameNow, Game, Statistic
from bot.management.commands.modules.filters import *
from datetime import timedelta
from django.utils import timezone

from ...modules.edit_or_send_message import edit_or_send_message

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
OFFSET = 3


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
        text += f"Здраствуйте, {user.full_name}"
    else:
        text += f"С возвращением, {user.full_name}"
    text += await texts.start(BotUser, user, bot)
    await edit_or_send_message(bot, message, text=text, kb=keyboards.help)


@dp.callback_query_handler(Button("menu"), state='*')
async def prev_(call):
    await start_(call.message)


@dp.message_handler(commands=['help'], state='*')
async def help_(message: types.Message):
    await edit_or_send_message(bot, message, text=await texts.help(), kb=keyboards.help)


@dp.message_handler(commands=['link'], state='*')
async def link_(msg: types.Message):
    await edit_or_send_message(bot, msg, text=await texts.link(BotUser, bot, msg))


@dp.message_handler(commands=['referrals'], state='*')
async def referrals_(msg):
    cur_user_id = BotUser.objects.get(tg_id=msg.chat.id).id
    n = '\n'
    text = f"Ваши реффералы:\n" \
           f"{f'{n}'.join([f'@{user.username}' for user in BotUser.objects.all() if user.referral == cur_user_id])}"
    await edit_or_send_message(bot, msg, text=text)


@dp.callback_query_handler(Button("stat"), state='*')
async def statistic(call: CallbackQuery):
    await edit_or_send_message(bot, call, text=await texts.stat(Statistic))


def get_game_id(state):
    game_id = (await state.get_data()).get('game_id')
    if not game_id:
        await state.set_data({'game_id': 0})
        game_id = 0
    return game_id


@dp.callback_query_handler(Button("matches"), state='*')
async def matches_(call, state: FSMContext, games=None):
    game_id = get_game_id(state)
    games = GameNow.objects.filter(starttime__lt=timezone.now() + timedelta(hours=20))[game_id:][:OFFSET] if not games else games
    text = "".join([await texts.matches(game) for game in games])
    await edit_or_send_message(bot, call, text=text, kb=keyboards.matches)


@dp.callback_query_handler(Button("next"), state='*')
async def next_(call, state: FSMContext):
    game_id = get_game_id(state)
    games = GameNow.objects.filter(starttime__lt=timezone.now() + timedelta(hours=20))
    game_id = game_id + OFFSET if game_id < len(games) - 1 - OFFSET else 0
    await state.set_data({'game_id': game_id})
    await matches_(call, state, games)


@dp.callback_query_handler(Button("prev"), state='*')
async def prev_(call, state: FSMContext):
    game_id = get_game_id(state)
    games = GameNow.objects.filter(starttime__lt=timezone.now() + timedelta(hours=20))
    game_id = game_id - OFFSET if game_id - OFFSET > 0 else len(games) - 1
    await state.set_data({'game_id': game_id})
    await matches_(call, state, games)
