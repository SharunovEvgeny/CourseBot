from aiogram import types
from aiogram.utils.exceptions import MessageNotModified


async def edit_or_send_message(bot, message_or_call, parse_mode='HTML', kb=None, text=None, photo=None, disable_web=False):
    message = message_or_call if isinstance(message_or_call, types.Message) else message_or_call.message
    if photo:
        try:
            await bot.edit_message_caption(
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
                await bot.send_animation(
                    chat_id=message.chat.id,
                    animation=photo,
                    caption=text,
                    parse_mode=parse_mode,
                    reply_markup=kb,
                )
    else:
        try:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.message_id,
                text=text,
                parse_mode=parse_mode,
                reply_markup=kb,
                disable_web_page_preview=disable_web
            )
        except Exception as e:
            if type(e) == MessageNotModified:
                pass
            else:
                await message.delete()
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=text,
                    parse_mode=parse_mode,
                    reply_markup=kb,
                    disable_web_page_preview=disable_web
                )
