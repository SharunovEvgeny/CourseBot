import os
from aiogram import types
from .load_all import bot, dp
from bot.models import BotUser, Team
from .filters import *
from .fuctions import *

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
    players = Team.objects.get(id=1).players.all()
    await message.answer("\n".join(list(players)))
    text += f""", это бот для прогнозов на матчи по Dota 2
Всего пользователей {BotUser.objects.count()}
Вы можете позвать друзей по своей сслыке:
https://t.me/{(await bot.me).username}?start={BotUser.objects.get(tg_id=message.chat.id).id}
Посмотрите матчи на сегодня /matches"""
    await message.answer(text,
                         reply_markup=await get_inline_first_keyboard())  # вызвает первый тип инлайн клавиатуры из файла functions


# печатает реферальную ссылку
@dp.message_handler(commands=["link"])
async def check_referral_links(message: types.Message):
    await message.answer(f"""Вы можете позвать друзей по своей сслыке:
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

#@dp.message_handler(commands=['Mathes'])
#async def mathes_commands(message:types.Message):
   # text = await get_mathes_now()
#    await message.reply(text,reply=False)
