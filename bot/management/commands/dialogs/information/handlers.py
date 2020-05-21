import importlib
import inspect

import os
import re
import sys

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup

from . import texts, keyboards
from ..general.handlers import info_
from ...load_all import bot, dp
from bot.models import BotUser, GameNow, Game, Statistic, Team
from bot.management.commands.modules.filters import *
from datetime import timedelta
from django.utils import timezone

from ...modules.edit_or_send_message import edit_or_send_message

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
OFFSET = 9


async def get_team_id(state):
    team_id = (await state.get_data()).get('team_id')
    if not team_id:
        await state.set_data({'team_id': 0})
        team_id = 0
    return team_id


@dp.callback_query_handler(lambda call: re.search(r"team:[\d]+", call.data), state='*')
async def team_info(call, state: FSMContext):
    team = Team.objects.get(id=call.data.replace("team:", ""))
    await edit_or_send_message(bot, call, text=await texts.team_info(team), kb=keyboards.team_info)
    await call.answer()


@dp.callback_query_handler(Button("team:back"), state='*')
async def team_back(call, state: FSMContext):
    await info_(call, state, team_id=await get_team_id(state))


@dp.callback_query_handler(Button("team:next"), state='*')
async def next_(call, state: FSMContext):
    team_id = await get_team_id(state)
    teams = Team.objects.order_by('-power')
    team_id = team_id + OFFSET if team_id < len(teams) - OFFSET else 0
    await state.set_data({'team_id': team_id})
    await info_(call, state, teams, team_id)


@dp.callback_query_handler(Button("team:prev"), state='*')
async def prev_(call, state: FSMContext):
    team_id = await get_team_id(state)
    teams = Team.objects.order_by('-power')
    team_id = team_id - OFFSET if team_id - OFFSET >= 0 else len(teams) - 1 - (len(teams) - 1) % OFFSET
    await state.set_data({'team_id': team_id})
    await info_(call, state, teams, team_id)


