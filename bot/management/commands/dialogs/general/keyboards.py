from bot.management.commands.modules.keyboard import KeyboardInline, KeyboardReply
from bot.models import Game

"""
keyboard v 1.0

:List of :Dicts where first is :Str name, last is :Str callback.
"""

help = KeyboardInline([{"Матчи": "matches", "Статистика": "stat"},
                       {"Помощь": "help"}]).get()

matches = KeyboardInline([{"<-": "prev", "->": "next"},
                          {"Меню": "menu"}]).get()

# link = KeyboardInline([{"Назад": "back"}]).get()
# referrals = link
