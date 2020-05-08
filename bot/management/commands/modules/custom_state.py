from aiogram.dispatcher.filters.state import State, StatesGroup
from collections import defaultdict
import weakref

from aiogram.utils.exceptions import MessageNotModified


class CustomState_(State):
    __refs__ = defaultdict(list)

    def __init__(self):
        super().__init__()
        self.__refs__[self.__class__].append(weakref.ref(self))

    @classmethod
    def get_instances(cls):
        for inst_ref in cls.__refs__[cls]:
            inst = inst_ref()
            if inst is not None:
                yield inst


class CustomState(CustomState_):
    def __init__(self, message_text=None, kb=None, photo=None, document=None, geo=None, args=None, func=None, prev=None, next_=None):
        super(CustomState, self).__init__()
        self.message_text = message_text
        self.kb = kb
        self.photo = photo
        self.document = document
        self.geo = geo
        self.args = args
        self.func = func
        self.prev = prev
        self.next_ = next_

    def __str__(self):
        return self._state

    async def send_message(self, bot, message, parse_mode='HTML', kb=None, text=None):
        try:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.message_id,
                text=self.message_text if self.message_text and not callable(self.message_text) else text if text else self.message_text(0) if callable(self.message_text) else None,
                parse_mode=parse_mode,
                reply_markup=kb if kb else self.kb(0) if callable(self.kb) else self.kb
            )
        except Exception as e:
            if type(e) == MessageNotModified:
                pass
            else:
                await bot.send_message(
                    message.chat.id,
                    self.message_text if self.message_text and not callable(self.message_text) else text if text else self.message_text(0) if callable(self.message_text) else None,
                    parse_mode=parse_mode,
                    reply_markup=kb if kb else self.kb(0) if callable(self.kb) else self.kb
                )
        await self.set()

    async def back(self):
        self.prev.set()
        return self.prev
