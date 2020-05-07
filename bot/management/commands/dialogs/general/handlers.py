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
from ...modules.custom_state import CustomState

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


# Обработчик команды старт
@dp.message_handler(commands=["start"], state='*')
async def register_user(message: types.Message):
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
    text += f", это бот для <b>прогнозов на матчи по Dota 2 🥳</b>\n" \
            f"Всего пользователей {BotUser.objects.count()}\n" \
            f"Вы можете позвать друзей по своей ссылке:\n" \
            f"[Ваша ссылка...](https://t.me/{(await bot.me).username}?start={user.id})\n\n" \
            f"Посмотрите матчи на сегодня: /matches"

    """
    keyboard v 1.0

    :List of :Dicts where first is :Str name, last is :Str callback.
    """
    await General.start.send_message(bot, message, text=text)


@dp.message_handler(commands=["help"], custom_state='*', state='*')
async def help_commands(message: types.Message):
    await General.help.send_message(bot, message)


@dp.callback_query_handler(Button("help"), custom_state='*', state='*')
async def help_inline_button(call: CallbackQuery):
    await General.help.send_message(bot, call.message)
    await call.message.edit_reply_markup()


@dp.message_handler(commands=["link"], custom_state='*', state='*')
async def get_referral_links(message: types.Message):
    user = BotUser.objects.get(tg_id=message.chat.id)
    text = f"Вы можете позвать друзей по своей ссылке:\n" \
           f"https://t.me/{(await bot.me).username}?start={user.id}"
    await General.link.send_message(bot, message, text=text)


@dp.message_handler(commands=["referrals"], custom_state='*', state='*')
async def get_referrals(message: types.Message):
    cur_user_id = BotUser.objects.get(tg_id=message.chat.id).id
    n = '\n'
    text = f"Ваши реффералы:\n" \
           f"{f'{n}'.join([f'@{user.username}' for user in BotUser.objects.all() if user.referral == cur_user_id])}"
    await General.referrals.send_message(bot, message, text=text)


@dp.callback_query_handler(Button('matches'), custom_state='*', state='*')
async def matches_commands(call, state: FSMContext):
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
    while game.starttime > timezone.now() + timedelta(hours=20) and start_game_id != game_id-1 if isinstance(call, types.CallbackQuery) and call.data == 'next' else game_id+1 if isinstance(call, types.CallbackQuery) and call.data == 'prev' else game_id-1:
        game_id += 1 if isinstance(call, types.CallbackQuery) and call.data == 'next' else -1 if isinstance(call, types.CallbackQuery) and call.data == 'prev' else 1
        game = games[game_id]
    text = (f"{game.tournament.name if game.tournament else ''}"
            f"Начало: {timezone.localtime(game.starttime).strftime('%d.%m.%Y %H-%M')}"
            f"{game.team1} {game.format} {game.team2}")
    kb = General.matches.kb([f"{game.predict}%", f"{game.format}", f"{100 - game.predict}%"])
    await General.matches.send_message(bot, call.message, text=text, kb=kb)


@dp.message_handler(commands=['matches'], custom_state='*', state='*')
async def matches_commands_message(message: types.Message, state: FSMContext):
    await matches_commands(message, state)


@dp.callback_query_handler(Button("back"), custom_state='*', state='*')
async def back(call: CallbackQuery, custom_state: CustomState):
    new_state = await custom_state.back()
    if new_state.func:
        await new_state.func(call.message)
    else:
        await new_state.send_message(bot, call.message)
