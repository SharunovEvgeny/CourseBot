from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


class KeyboardInline:
    def __init__(self, list_keyboard: list = None, inline_keyboard=None):
        self.list_keyboard = list_keyboard
        self.keyboard = inline_keyboard

    def make_inline_keyboard(self):
        self.keyboard = InlineKeyboardMarkup()
        for row in self.list_keyboard:
            self.keyboard.row_width = len(row)
            self.keyboard.add(*[InlineKeyboardButton(button,
                                                     callback_data=row[button] if not "url:" in row[button] else None,
                                                     url=row[button].replace("url:", "") if "url:" in row[
                                                         button] else None)
                                for button in row])

    def get(self):
        self.make_inline_keyboard()
        return self.keyboard


class KeyboardReply:
    def __init__(self, list_keyboard: list = None, reply_keyboard=None):
        self.list_keyboard = list_keyboard
        self.keyboard = reply_keyboard

    def make_reply_keyboard(self):
        self.keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        for row in self.list_keyboard:
            self.keyboard.row_width = len(row)
            self.keyboard.add(*[KeyboardButton(button, request_contact=True) if "телефон" in button else
                                KeyboardButton(button, request_location=True) if "геолокац" in button else
                                KeyboardButton(button) for button in row])

    def get(self):
        self.make_reply_keyboard()
        return self.keyboard
