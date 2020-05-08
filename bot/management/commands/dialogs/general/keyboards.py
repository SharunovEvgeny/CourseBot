from bot.management.commands.modules.keyboard import KeyboardInline, KeyboardReply

"""
keyboard v 1.0

:List of :Dicts where first is :Str name, last is :Str callback.
"""

start = KeyboardInline([{"Матчи": "matches", "Статистика": "stat"},
                        {"Помощь": "help"}]).get()
help = start
link = KeyboardInline([{"Назад": "back"}]).get()
referrals = link
matches = lambda x: KeyboardInline([{f"{x[0]}": "None"}, {f"{x[1]}": "None"}, {f"{x[2]}": "None"},
                                    {"<-": "prev", "->": "next"},
                                    {"Назад": "back"}]).get(),
