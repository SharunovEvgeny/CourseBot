from django.db import models


class Tier(models.Model):
    name = models.CharField("Название", max_length=100)
    coefficient = models.FloatField("Коэффицент")

    def __str__(self):
        return f"{self.name}"


class Tournament(models.Model):
    name = models.CharField("Название", max_length=100)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, verbose_name="Статус")


class Game(models.Model):
    team1 = models.ForeignKey('Team', related_name='team1', on_delete=models.CASCADE, verbose_name="Команда 1")
    team2 = models.ForeignKey('Team', related_name='team2', on_delete=models.CASCADE, verbose_name="Команда 2")
    team1_score = models.SmallIntegerField()
    team2_score = models.SmallIntegerField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, verbose_name="Турнир")


class Player(models.Model):
    full_name = models.CharField("Имя фамилия", max_length=255)
    nickname = models.CharField("Ник в игре", max_length=255)
    country = models.CharField("Страна", max_length=100)
    team = models.ForeignKey('Team', related_name='players', on_delete=models.CASCADE, verbose_name="Команда")


class Team(models.Model):
    name = models.CharField("Название", max_length=50)
    power = models.FloatField("Сила")
    time_change_compound = models.DateTimeField("Время последнего изменения в составе команды", null=True, blank=True)


class BotUser(models.Model):
    language = models.CharField('язык пользовотеля', max_length=2)
    tg_id = models.BigIntegerField('id пользователя')
    referral = models.BigIntegerField("кто пригласил",null=True,blank=True)
    full_name = models.CharField('полное имя пользовотеля', max_length=100)
    username = models.CharField('имя пользователя', max_length=50,null=True,blank=True)
