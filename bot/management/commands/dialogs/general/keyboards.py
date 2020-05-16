from bot.management.commands.modules.keyboard import KeyboardInline, KeyboardReply
from bot.models import Game, Team

"""
keyboard v 1.0

:List of :Dicts where first is :Str name, last is :Str callback.
"""

menu = KeyboardInline([{"Матчи": "matches", "Статистика": "stat"},
                       {"Информация": "info", "Рефераллы": "ref"}]).get()

matches = KeyboardInline([{"<-": "prev", "->": "next"},
                          {"Меню": "menu"}]).get()

back = KeyboardInline([{"Меню": "menu"}]).get()


async def info(teams_db, team_id):
    teams = []
    tmp = {}
    for i, team in enumerate(teams_db[team_id:][:9]):
        tmp.update({team.name: f"team:{team.id}"})
        if i % 3 == 0 and i != 0:
            teams.append(tmp)
            tmp = {}
    teams.append({"<-": "team:prev", "->": "team:next"})
    teams.append({"Меню": "menu"})
    return KeyboardInline(teams).get()
