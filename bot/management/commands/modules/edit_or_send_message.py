from aiogram import types
from aiogram.utils.exceptions import MessageNotModified


async def edit_or_send_message(bot, message_or_call, parse_mode='HTML', kb=None, text=None):
    message = message_or_call if isinstance(message_or_call, types.Message) else message_or_call.message
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=text,
            parse_mode=parse_mode,
            reply_markup=kb,
        )
    except Exception as e:
        if type(e) == MessageNotModified:
            pass
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=text,
                parse_mode=parse_mode,
                reply_markup=kb,
            )
