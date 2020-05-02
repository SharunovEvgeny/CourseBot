import time

from django.utils import timezone
from liquipediapy import dota, counterstrike, liquipediapy

from bot.models import Player, Team, Game, Tournament, Tier
import requests
from bs4 import BeautifulSoup, NavigableString
import datetime


def make_dt(dt_str):
    from django.utils.timezone import get_current_timezone
    from datetime import datetime
    tz = get_current_timezone()
    return tz.localize(datetime.strptime(dt_str, '%B %d, %Y - %H:%M %Z'))


def make_dt_game(dt_str):
    from django.utils.timezone import get_current_timezone
    from datetime import datetime
    tz = get_current_timezone()
    return tz.localize(datetime.strptime(dt_str, '%Y-%m-%d %H:%M %Z'))


class LiquidpediaDotaParser:
    def __init__(self, app_name):
        self.app_name = app_name
        self.dota_p = dota(self.app_name)
        self.lp = liquipediapy(self.app_name, 'dota2')

    def update_players_and_teams(self):
        players = self.dota_p.get_players()
        for player in players:
            user, _ = Player.objects.get_or_create(nickname=player['ID'], full_name=player['Name'], country=player['country'])
            if _ or user.team == None:
                user.team, _ = Team.objects.get_or_create(name=player['Team'])
                if _:
                    user.team.power = 0
                    user.team.save()
            user.save()

    def parse_tournaments(self):
        tournaments = self.dota_p.get_tournaments()
        for tournament in tournaments:
            tier, _ = Tier.objects.get_or_create(name=tournament['tier'])
            Tournament.objects.get_or_create(tier=tier, name=tournament['name'])

    def update_played_games(self):
        teams = Team.objects.all()
        time.sleep(2.1)
        for team in teams:
            soup, _ = self.lp.parse(f'{team.name}/Played_Matches')
            trs = soup.find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                data = {'start_time': "", "tier": "", 'tournament': None, 'score': [], 'team2': ""}
                for i, td in enumerate(tds):
                    if i == 0:
                        data['start_time'] += td.text + " "
                    elif i == 1:
                        data['start_time'] += td.text
                        data['start_time'] = make_dt_game(data['start_time'])
                    elif i == 2:
                        data['tier'] = td.text[2:]
                    elif i == 3:
                        data['tournament'] = Tournament.objects.get_or_create(name=td.text, tier=data['tier'])
                    # No, i don't forget i == 4, that is duplication!!!
                    elif i == 5:
                        x = td.text.split()
                        data['score'] = [x[0], x[2]]
                    elif i == 6:
                        data['team2'] = td.text
                if Game.objects.filter(starttime=data['start_time'], team2=team).count() == 0:
                    Game.objects.create(team1=team, team2=Team.objects.get(name=data['team2']),
                                        team1_score=data['score'][0], team2_score=data['score'][1],
                                        tournament=data['tournament'], starttime=data['start_time'])


    def update_ongoing_and_upcoming_games(self):
        games = self.dota_p.get_upcoming_and_ongoing_games()
        for game in games:
            game_obj, g = Game.objects.get_or_create(team1=Team.objects.get(name=game['team1']), team2=Team.objects.get(name=game['team2']),
                                                     format=game['format'], starttime=make_dt(game['start_time']))
            game_obj.tournament, t = Tournament.objects.get_or_create(name=game['tournament'])
            game_obj.save()

if __name__ == "__main__":
    pass
