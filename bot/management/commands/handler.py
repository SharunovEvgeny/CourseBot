import os
from aiogram import types
from .load_all import bot, dp
from bot.models import BotUser
from .keyboards import ListOfButtons
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


@dp.message_handler(commands=["start"])
async def register_user(message: types.Message):
    user,is_created_now=BotUser.objects.get_or_create(tg_id=message.chat.id)
    if is_created_now:
        user.referral = BotUser.objects.get(id=message.get_args()) if message.get_args() else None
        user.username= message.from_user.username
        user.full_name = message.from_user.full_name
        user.language = "ru"

        user.save()
        await message.answer("Здраствуйте, мы вас ждали")
    else:
        await message.answer("С возвращением")
