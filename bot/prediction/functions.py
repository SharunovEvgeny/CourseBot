
from bot.models import GameNow, Team, Game, Statistic


def game_predict(game: GameNow, coef: float):
    first_joint_games = game.team1.team1_game.filter(team2=game.team2)
    second_joint_games = game.team2.team2_game.filter(team2=game.team1)
    score1 = 0
    score2 = 0
    for gm in first_joint_games:
        score1 += gm.team1_score
        score2 += gm.team2_score
    for gm in second_joint_games:
        score1 += gm.team2_score
        score2 += gm.team1_score
    try:
        joint_games_cof = (score1 / (score1 + score2)) * coef
    except:
        joint_games_cof = 0
    if score2 > score1:
        joint_games_cof *= (-1)
    elif score2 == score1:
        joint_games_cof = 0
    predict = ((game.team1.power / (game.team1.power + game.team2.power) * 100) + joint_games_cof) // 1
    return predict


def calculate_power_cur_games(games):
    for game in games:
        tier = game.tournament.tier
        game.team1.power += game.team1_score * tier.coefficient
        game.team2.power += game.team2_score * tier.coefficient
        game.team1.save()
        game.team2.save()


def calculate_team_power(team):
    games1 = Game.objects.filter(team1=team)
    games2 = Game.objects.filter(team2=team)
    calculate_power_cur_games(games1)
    calculate_power_cur_games(games2)
    try:
        team.power = team.power / (team.team1_game.count() + team.team2_game.count())
    except:
        team.power = team.power / 1
    team.save()


def calculate_all_teams_power():
    games = Game.objects.all()
    Team.objects.all().update(power=0)
    calculate_power_cur_games(games)
    teams = Team.objects.order_by('power')
    for team in teams:
        try:
            team.power = team.power / (team.team1_game.count() + team.team2_game.count())
        except:
            team.power = team.power / 1
        team.save()

def statistics_collection(game: Game):
    win = game.team1
    predict = game.team1
    statistic, _ = Statistic.objects.get_or_create(id=1)
    if game.predict < 50:
        predict = game.team2
    if game.team1_score < game.team2_score:
        win = game.team2
    elif game.team1_score == game.team2_score:
        statistic.bet_all += 1
        statistic.unpredictable_bet_all += 1
        if predict == 50:
            statistic.unpredictable_bet_successful += 1
            statistic.all_bet_successful += 1
        return
    success = True
    if win != predict:
        success = False
    if 45 < game.predict < 55:
        statistic.unpredictable_bet_all += 1
        if success:
            statistic.unpredictable_bet_successful += 1
    elif (55 <= game.predict <= 65) or (35 <= game.predict <= 45):
        statistic.risk_bet_all += 1
        if success:
            statistic.risk_bet_successful += 1
    else:
        statistic.safe_bet_all += 1
        if success:
            statistic.safe_bet_successful += 1
    statistic.bet_all += 1
    if success:
        statistic.all_bet_successful += 1
