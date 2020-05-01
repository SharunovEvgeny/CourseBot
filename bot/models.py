from django.db import models


class Tier(models.Model):
    name = models.CharField("Название", max_length=100)
    coefficient = models.FloatField("Коэффицент")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Тир турнира"
        verbose_plural = "Тиры турнира"


class Tournament(models.Model):
    name = models.CharField("Название", max_length=100)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, verbose_name="Статус")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Турнир"
        verbose_plural = "Турниры"

class Game(models.Model):
    team1 = models.ForeignKey('Team', related_name='team1_game', on_delete=models.CASCADE, verbose_name="Команда 1")
    team2 = models.ForeignKey('Team', related_name='team2_game', on_delete=models.CASCADE, verbose_name="Команда 2")
    team1_score = models.SmallIntegerField("Очки первой команды")
    team2_score = models.SmallIntegerField("Очки второй команды")
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, verbose_name="Турнир")
    format = models.CharField("формат",max_length=3)
    starttime = models.DateTimeField("Время игры")
    predict = models.SmallIntegerField("процент на победу")

    def __str__(self):
        return f"{self.team1} X {self.team2}"

    class Meta:
        verbose_name = "Игра"
        verbose_plural = "Игры"


class Player(models.Model):
    full_name = models.CharField("Имя фамилия", max_length=255)
    nickname = models.CharField("Ник в игре", max_length=255)
    country = models.CharField("Страна", max_length=100)
    team = models.ForeignKey('Team', related_name='players', on_delete=models.CASCADE, verbose_name="Команда",null=True,blank=True)

    def __str__(self):
        return f"{self.full_name} {self.nickname}"

    class Meta:
        verbose_name = "Игрок"
        verbose_plural = "Игроки"


class Team(models.Model):
    name = models.CharField("Название", max_length=250)
    power = models.FloatField("Сила",default=0)
    time_change_compound = models.DateTimeField("Время последнего изменения в составе команды", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


    class Meta:
        verbose_name = "Команда"
        verbose_plural = "Команды"


class BotUser(models.Model):
    tg_id = models.BigIntegerField('id пользователя')
    referral = models.BigIntegerField("кто пригласил",null=True,blank=True)
    full_name = models.CharField('полное имя пользовотеля', max_length=100)
    username = models.CharField('имя пользователя', max_length=50,null=True,blank=True)

    def __str__(self):
        return f"{self.full_name} {self.username}"

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_plural = "Пользователи бота"

