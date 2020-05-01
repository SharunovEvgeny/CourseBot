import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.bot import api
from .config import TOKEN
PATCHED_URL = "http://ec2-18-220-75-241.us-east-2.compute.amazonaws.com/tg/bot{token}/{method}"
setattr(api, 'API_URL', PATCHED_URL)
# from aiogram.contrib.fsm_storage.redis import RedisStorage2
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)
loop = asyncio.get_event_loop()
# Set up storage (either in Redis or Memory)
storage = JSONStorage("states.json")
# storage = RedisStorage2()
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
