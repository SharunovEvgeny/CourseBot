import time

from django.utils import timezone
from liquipediapy import dota, liquipediapy
from django.conf import settings
from bot.models import Player, Team, Game, Tournament, GameNow, Tier, Coefficient
from datetime import timedelta, datetime
import logging
from bot.prediction.functions import calculate_team_power, calculate_all_teams_power, game_predict, \
    statistics_collection


def make_dt(dt_str):
    from django.utils.timezone import get_current_timezone
    tz = get_current_timezone()
    return tz.localize(datetime.strptime(dt_str, '%B %d, %Y - %H:%M %Z'))


def make_dt_game(dt_str):
    from django.utils.timezone import get_current_timezone
    tz = get_current_timezone()
    return tz.localize(datetime.strptime(dt_str, '%Y-%m-%d %H:%M %Z'))


class LiquidpediaDotaParser:
    def __init__(self, app_name):
        self.app_name = app_name
        self.dota_p = dota(self.app_name)
        self.lp = liquipediapy(self.app_name, 'dota2')

    def update_teams(self):
        Team.objects.all().delete()
        time.sleep(2.3)
        soup, _ = self.lp.parse("Portal:Teams")
        ts = soup.find_all(["span class", "a", "href"])
        for i, y in enumerate(ts[24::2]):
            if y.text == "Veteran":
                break
            if (sum(1 for i in y.get('href') if i == "/")) == 3:
                continue
            team, _ = Team.objects.get_or_create(name=y.get("title"), link=y.get('href')[7:])
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
                flag = 0
                for i, td in enumerate(tds):
                    print(data['start_time'], flush=True)
                    if i == 0:
                        text = td.text[:4]
                        if text == "":
                            flag = 1
                            continue
                        if int(text) < datetime.now().year:
                            break
                        data['start_time'] += td.text + " "
                    elif i == 1:
                        data['start_time'] += td.text
                        try:
                            make_dt_game(data['start_time'])
                        except:
                            flag = 1
                            break
                        data['start_time'] = make_dt_game(data['start_time'])

                    elif i == 2:
                        data['tier'] = td.text[2:]
                    elif i == 3 and int(text) >= datetime.now().year:
                        tier, _ = Tier.objects.get_or_create(name=data['tier'])
                        data['tournament'], p = Tournament.objects.get_or_create(name=td.text, tier=tier)
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
                            data['score'][1] = 1
                    elif i == 6:
                        temp = list(td.find_all('a', href=True))[0].get('href')[7:]
                        try:
                            data['team2'] = Team.objects.get(link=temp)
                        except:
                            flag = 1
                            break
                if flag == 0:
                    if int(text) >= datetime.now().year:
                        if Game.objects.filter(starttime=data['start_time'], team2=team).count() == 0:
                            game = Game.objects.create(team1=team, team2=data['team2'],
                                                       team1_score=data['score'][0], team2_score=data['score'][1],
                                                       tournament=data['tournament'], starttime=data['start_time'])
        calculate_all_teams_power()

    def check_games(self):
        games = GameNow.objects.all()
        was_there_a_new_game = False
        for game in games:
            if timezone.now() > game.starttime + timedelta(hours=3):
                time.sleep(40)
                if timezone.now() > game.starttime + timedelta(hours=27):
                    GameNow.objects.filter(starttime=game.starttime, team1=game.team1, team2=game.team2).delete()
                is_second_link = False
                try:
                    soup, _ = self.lp.parse(f'{game.team1.link}/Played_Matches')
                except:
                    try:
                        soup, _ = self.lp.parse(f'{game.team2.link}/Played_Matches')
                        is_second_link = True
                    except:
                        GameNow.objects.filter(starttime=game.starttime, team1=game.team1, team2=game.team2).delete()
                        continue
                trs = soup.find_all('tr')
                logging.info(f"Start {game.team1}")
                for tr in trs:
                    tds = tr.find_all('td')
                    data = {'start_time': "", "tier": None, 'tournament': None, 'score': [], 'team2': ""}
                    year = 0
                    has_game_errors = False
                    logging.info("Mathes NEW")
                    for i, td in enumerate(tds):
                        if i == 0:
                            year = td.text[:4]
                            if year == "":
                                has_game_errors = True
                                continue
                            if int(year) < datetime.now().year:
                                break
                            data['start_time'] += td.text + " "
                        elif i == 1:
                            data['start_time'] += td.text
                            try:
                                make_dt_game(data['start_time'])
                                logging.info("try make dt")
                            except:
                                has_game_errors = True
                                logging.info("not make dt game")
                                break
                            data['start_time'] = make_dt_game(data['start_time'])
                            if game.starttime != data["start_time"]:
                                has_game_errors = True
                                logging.info("not true data")
                                break

                        elif i == 2:
                            data['tier'] = td.text[2:]
                        elif i == 3 and int(year) >= datetime.now().year:
                            tier, _ = Tier.objects.get_or_create(name=data['tier'])
                            data['tournament'], p = Tournament.objects.get_or_create(name=td.text)
                            data['tournament'].tier = tier
                            data['tournament'].save()
                            logging.info("get or create Tournament")
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
                                data['score'][1] = 1
                        elif i == 6:
                            temp = list(td.find_all('a', href=True))[0].get('href')[7:]
                            try:
                                data['team2'] = Team.objects.get(link=temp)
                            except:
                                has_game_errors = True
                                logging.info("team2 not find")
                                break
                    if not has_game_errors:
                        if int(year) >= datetime.now().year:
                            if (Game.objects.filter(starttime=data['start_time'],
                                                    team2=game.team1).count() + Game.objects.filter(
                                starttime=data['start_time'],
                                team1=game.team1).count() == 0 and is_second_link == False) or (
                                    Game.objects.filter(starttime=data['start_time'],
                                                             team2=game.team2).count() + Game.objects.filter(starttime=data['start_time'], team1=game.team2).count()==0 and is_second_link == True):
                                game_new, is_created_now = Game.objects.get_or_create(team1=game.team1,
                                                                                      team2=game.team2,
                                                                                      team1_score=data['score'][0],
                                                                                      team2_score=data['score'][1],
                                                                                      tournament=data['tournament'],
                                                                                      starttime=data['start_time'],
                                                                                      predict=game.predict)
                                if is_created_now:
                                    calculate_team_power(game_new.team1)
                                    calculate_team_power(game_new.team2)
                                    statistics_collection(game_new)
                                    was_there_a_new_game = True
                                    GameNow.objects.filter(starttime=game.starttime, team1=game.team1,
                                                           team2=game.team2).delete()
        if was_there_a_new_game:
            self.update_ongoing_and_upcoming_games()

    def update_ongoing_and_upcoming_games(self):
        time.sleep(40)
        games = self.dota_p.get_upcoming_and_ongoing_games()
        for game in games:
            try:
                team1 = Team.objects.get(name=game['team1'])
                team2 = Team.objects.get(name=game['team2'])
            except:
                continue
            GameNow.objects.filter(team1=team1,
                                   team2=team2,
                                   starttime__range=(make_dt(game['start_time']) - timedelta(hours=3),
                                                     make_dt(game['start_time']) + timedelta(hours=3))).delete()

            game_obj, g = GameNow.objects.get_or_create(team1=team1,
                                                        team2=team2,
                                                        format=game['format'],
                                                        starttime=make_dt(game['start_time']))

            game_obj.tournament, t = Tournament.objects.get_or_create(name=game['tournament'])
            game_obj.save()
            game_obj.predict = game_predict(game_obj)
            game_obj.save()


if __name__ == "__main__":
    pass
