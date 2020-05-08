import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
# from aiogram.contrib.fsm_storage.files import JSONStorage
from .config import TOKEN
from .modules.register_handlers import register_handlers
import inspect

"""
PATCHED_URL needs only if urs server is in Russia
# from aiogram.bot import api
# PATCHED_URL = "http://ec2-18-220-75-241.us-east-2.compute.amazonaws.com/tg/bot{token}/{method}"
# setattr(api, 'API_URL', PATCHED_URL)
"""

logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()
# storage = JSONStorage("states.json")
storage = RedisStorage2(host='redis')
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
for dialog in inspect.getmembers('dialogs', inspect.ismodule):
    register_handlers(dp, inspect.getmembers(f"{dialog}.handlers", inspect.isfunction))
