from liquipediapy import dota, counterstrike

from bot.models import Player, Team

dota_p = dota("parser")


def update_players_and_teams():
    players = dota_p.get_players()
    for player in players:
        user, _ = Player.objects.get_or_create(nickname=player['ID'], full_name=player['Name'], country=player['country'])
        if _ or user.team == None:
            user.team, _ = Team.objects.get_or_create(name=player['Team'])
            if _:
                user.team.power = 0
                user.team.save()
        user.save()


if __name__ == "__main__":
    update_players_and_teams()
