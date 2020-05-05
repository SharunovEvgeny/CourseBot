import time

from django.utils import timezone
from liquipediapy import dota, counterstrike, liquipediapy

from bot.models import Player, Team, Game, Tournament,GameNow
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

    def update_teams(self):
        time.sleep(2.3)
        soup, _ = self.lp.parse("Portal:Teams")
        ts = soup.find_all(["span class", "a", "href"])
        for i, y in enumerate(ts[24::2]):
            if y.text == "Veteran":
                break
            if (sum(1 for i in y.get('href') if i == "/")) == 3:
                continue
            team, _= Team.objects.get_or_create(name=y.get("title"), link=y.get('href')[7:])
            team.save()


    def update_played_games(self):
        teams = Team.objects.all()
        time.sleep(30)
        for team in teams:
            time.sleep(40)
            try:
                soup, _ = self.lp.parse(f'{team.link}/Played_Matches')
            except:
                continue
            trs = soup.find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                data = {'start_time': "", "tier": None, 'tournament': None, 'score': [], 'team2': ""}
                text = 0
                data_t = Tournament()
                flag=0
                for i, td in enumerate(tds):
                    if i == 0:
                        text = td.text[:4]
                        if text=="":
                            flag=1
                            continue
                        if int(text) < 2020:
                            break
                        data['start_time'] += td.text + " "
                    elif i == 1:
                        data['start_time'] += td.text
                        try:
                            make_dt_game(data['start_time'])
                        except:
                            flag=1
                            break
                        data['start_time'] = make_dt_game(data['start_time'])

                    elif i == 2:
                        data['tier'] = td.text[2:]
                    elif i == 3 and int(text) >= 2020:
                        data['tournament'], p = Tournament.objects.get_or_create(name=td.text, tier=data['tier'])
                    # No, i don't forget i == 4, that is duplication!!!
                    elif i == 5:
                        x = td.text.split()
                        data['score'] = [x[0], x[2]]
                        if data['score'][0] == 'W':
                            data['score'][0] = 1
                        if data['score'][1] == "FF":
                            data['score'][1] = 0
                        if data['score'][0] == "FF":
                            data['score'][0] = 0
                        if data['score'][1] == "W":
                            data['score'][1] = 0
                    elif i == 6:
                        temp=list(td.find_all('a',href=True))[0].get('href')[7:]
                        try:
                            data['team2'] = Team.objects.get(link=temp)
                        except:
                            flag=1
                            break
                if flag==0:
                    if int(text) >= 2020:
                     if Game.objects.filter(starttime=data['start_time'], team2=team).count()==0:
                            Game.objects.create(team1=team, team2=data['team2'],
                                                        team1_score=data['score'][0], team2_score=data['score'][1],
                                                        tournament=data['tournament'], starttime=data['start_time'])

    def update_ongoing_and_upcoming_games(self):
        GameNow.objects.all().delete()
        games = self.dota_p.get_upcoming_and_ongoing_games()
        for game in games:
            try:
                name1=Team.objects.get(name=game['team1'])
                name2=Team.objects.get(name=game['team2'])
            except:
                continue
            game_obj, g = GameNow.objects.get_or_create(team1=Team.objects.get(name=game['team1']),
                                                        team2=Team.objects.get(name=game['team2']),
                                                        format=game['format'], starttime=make_dt(game['start_time']))
            game_obj.tournament, t = Tournament.objects.get_or_create(name=game['tournament'])
            game_obj.save()


if __name__ == "__main__":
    pass
