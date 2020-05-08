
import importlib

import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup

from ...load_all import bot, dp
from bot.models import BotUser, GameNow
from bot.management.commands.modules.filters import *
from datetime import timedelta
from django.utils import timezone

from .states import General

from ...app import Context
from ...modules.edit_or_send_message import edit_or_send_message

context = importlib.import_module('texts')
conkb = importlib.import_module('keyboards')
texts = Context(context)
kbs = Context(conkb)


os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


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
    text += texts.start

    await edit_or_send_message(bot, message, text=text, kb=kbs.start)


async def help_(msg_or_clb):
    await edit_or_send_message(bot, msg_or_clb, text=texts.help, kb=kbs.help)


async def link_(msg_or_clb):
    await edit_or_send_message(bot, msg_or_clb, text=texts.link, kb=kbs.link)


async def referrals_(msg_or_clb):
    cur_user_id = BotUser.objects.get(tg_id=msg_or_clb.chat.id).id
    n = '\n'
    text = f"Ваши реффералы:\n" \
           f"{f'{n}'.join([f'@{user.username}' for user in BotUser.objects.all() if user.referral == cur_user_id])}"
    await edit_or_send_message(bot, msg_or_clb, text=text, kb=kbs.referrals)


async def matches_(call, state: FSMContext):
    if isinstance(call, types.CallbackQuery) and call.data == "None":
        await call.answer()
        return
    game_id = (await state.get_data()).get('game_id')
    if not game_id:
        await state.set_data({'game_id': 0})
        game_id = 0
    games = GameNow.objects.all()
    game = games[game_id]
    start_game_id = game_id
    while game.starttime > timezone.now() + timedelta(hours=20) and start_game_id != game_id - 1 if isinstance(call,
                                                                                                               types.CallbackQuery) and call.data == 'next' else game_id + 1 if isinstance(
            call, types.CallbackQuery) and call.data == 'prev' else game_id - 1:
        game_id += 1 if isinstance(call, types.CallbackQuery) and call.data == 'next' else -1 if isinstance(call,
                                                                                                            types.CallbackQuery) and call.data == 'prev' else 1

        game = games[game_id]
    text = (f"{game.tournament.name if game.tournament else ''}"
            f"Начало: {timezone.localtime(game.starttime).strftime('%d.%m.%Y %H-%M')}"
            f"{game.team1} {game.format} {game.team2}")

    kb = kbs.matches([f"{game.predict}%", f"{game.format}", f"{100 - game.predict}%"])
    await edit_or_send_message(bot, call, text=text, kb=kb)
