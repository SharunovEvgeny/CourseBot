import importlib
import inspect

import os
import sys

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup

from . import texts, keyboards
from ...load_all import bot, dp
from bot.models import BotUser, GameNow, Game,Statistic
from bot.management.commands.modules.filters import *
from datetime import timedelta
from django.utils import timezone

from ...modules.edit_or_send_message import edit_or_send_message

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


@dp.message_handler(commands=['start'])
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


@dp.message_handler(commands=['help'])
async def help_(message: types.Message):
    await edit_or_send_message(bot, message, text=await texts.help(), kb=keyboards.help)


@dp.message_handler(commands=['link'])
async def link_(msg: types.Message):
    await edit_or_send_message(bot, msg, text=await texts.link(BotUser, bot, msg))


@dp.message_handler(commands=['referrals'])
async def referrals_(msg):
    cur_user_id = BotUser.objects.get(tg_id=msg.chat.id).id
    n = '\n'
    text = f"Ваши реффералы:\n" \
           f"{f'{n}'.join([f'@{user.username}' for user in BotUser.objects.all() if user.referral == cur_user_id])}"
    await edit_or_send_message(bot, msg, text=text)

@dp.callback_query_handler(Button("stat"))
async def statistic(call):
    await edit_or_send_message(bot, call, text=await texts.stat(Statistic))

@dp.callback_query_handler(Button("matches"))
async def matches_(call, state: FSMContext):
    if call.data == "None":
        await call.answer()
        return
    game_id = (await state.get_data()).get('game_id')
    if not game_id:
        await state.set_data({'game_id': 0})
        game_id = 0
    games = GameNow.objects.all()
    game = games[game_id]
    start_game_id = game_id
    game_id += 1 if call.data == 'next' else -1 if call.data == 'prev' else 1
    text = ""
    for number, game in enumerate(games):
        if game.starttime < timezone.now() + timedelta(hours=20):
            text += await texts.matches(game)
        if number % 3 == 0 and number > 0:
            await edit_or_send_message(bot, call, text=text)
            text = ""
