import os
from aiogram import types
from .load_all import bot, dp
from bot.models import BotUser, Team,GameNow,Game
from .filters import *
from .fuctions import *
from datetime import timedelta, datetime
from django.utils import timezone
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


# Обработчик команды старт
@dp.message_handler(commands=["start"])
async def register_user(message: types.Message):
    user, is_created_now = BotUser.objects.get_or_create(tg_id=message.chat.id)
    text = ""
    if is_created_now:  # Если пользователь новый то создаёт его в базе данных
        user.referral = message.get_args() if message.get_args() else None
        user.username = message.from_user.username
        user.full_name = message.from_user.full_name
        user.save()
        text += "Здраствуйте"
    else:
        text += "С возвращением"
    text += f""", это бот для прогнозов на матчи по Dota 2
Всего пользователей {BotUser.objects.count()}
Вы можете позвать друзей по своей ссылке:
https://t.me/{(await bot.me).username}?start={BotUser.objects.get(tg_id=message.chat.id).id}
Посмотрите матчи на сегодня /matches"""
    await message.answer(text,
                         reply_markup=await get_inline_first_keyboard())  # вызвает первый тип инлайн клавиатуры из файла functions


# печатает реферальную ссылку
@dp.message_handler(commands=["link"])
async def check_referral_links(message: types.Message):
    await message.answer(f"""Вы можете позвать друзей по своей ссылке:
https://t.me/{(await bot.me).username}?start={BotUser.objects.get(tg_id=message.chat.id).id}""")


# печатает рефераллов
@dp.message_handler(commands=["referrals"])
async def check_referrals(message: types.Message):
    text = f"Your referrals: "
    id = BotUser.objects.get(tg_id=message.chat.id).id
    for num in list(BotUser.objects.all()):
        if id == num.referral:
            text += (await bot.get_chat(num.tg_id)).get_mention(as_html=True) + f" "
    await message.answer(text)


# inline кнопка help
@dp.callback_query_handler(Button("help"))
async def help_inline_button(call: CallbackQuery):
    text = await get_text_help()
    await call.message.edit_reply_markup()
    await call.message.reply(text=text, reply=False, reply_markup=await get_inline_first_keyboard())


# комманды help
@dp.message_handler(commands=["help"])
async def help_commands(message: types.Message):
    text = await get_text_help()
    await message.reply(text=text, reply=False)

@dp.message_handler(commands=['matches'])
async def mathes_commands(message:types.Message):
    games=GameNow.objects.all()
    time = timezone.now() + timedelta(hours=20)
    for game in games:
        if game.starttime < time:
            await message.reply(f"""{game.team1} {game.format} {game.team2} 
Название турнира: {game.tournament.name}
Начало игры: {timezone.localtime(game.starttime).strftime("%d.%m.%Y %H-%M")}
Первая команды победит с шансом: {game.predict}%""", reply=False)



