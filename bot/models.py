from django.db import models


class Tournament(models.Model):
    name = models.CharField("Название", max_length=100)
    tier = models.CharField("Tier", null=True, blank=True,max_length=50)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Турнир"
        verbose_name_plural = "Турниры"


class Game(models.Model):
    team1 = models.ForeignKey('Team', related_name='team1_game', on_delete=models.CASCADE, verbose_name="Команда 1")
    team2 = models.ForeignKey('Team', related_name='team2_game', on_delete=models.CASCADE, verbose_name="Команда 2")
    team1_score = models.SmallIntegerField("Очки первой команды", null=True, blank=True)
    team2_score = models.SmallIntegerField("Очки второй команды", null=True, blank=True)
    tournament = models.ForeignKey('Tournament',on_delete=models.CASCADE, verbose_name="Турнир", null=True, blank=True)
    format = models.CharField("формат", max_length=3, null=True, blank=True)
    starttime = models.DateTimeField("Время игры", null=True, blank=True)
    predict = models.SmallIntegerField("процент на победу первой команды", null=True, blank=True)

    def __str__(self):
        return f"{self.team1} X {self.team2}"

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"

class GameNow(models.Model):
    team1 = models.ForeignKey('Team', related_name='team1_now', on_delete=models.CASCADE, verbose_name="Команда 1")
    team2 = models.ForeignKey('Team', related_name='team2_now', on_delete=models.CASCADE, verbose_name="Команда 2")
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, verbose_name="Турнир", null=True, blank=True)
    format = models.CharField("формат", max_length=3, null=True, blank=True)
    starttime = models.DateTimeField("Время игры", null=True, blank=True)
    predict = models.SmallIntegerField("процент на победу первой команды", null=True, blank=True)

    def __str__(self):
        return f"{self.team1} X {self.team2}"

    class Meta:
        verbose_name = "Игра Сейчас"
        verbose_name_plural = "Игры Сейчас"


class Player(models.Model):
    full_name = models.CharField("Имя фамилия", max_length=255)
    nickname = models.CharField("Ник в игре", max_length=255)
    country = models.CharField("Страна", max_length=100)
    team = models.ForeignKey('Team', related_name='players', on_delete=models.CASCADE, verbose_name="Команда",
                             null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} {self.nickname}"

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"


class Team(models.Model):
    name = models.CharField("Название", max_length=250)
    link=models.CharField("Ссылка",max_length=60)
    power = models.FloatField("Сила", default=0)
    time_change_compound = models.DateTimeField("Время последнего изменения в составе команды", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"


class BotUser(models.Model):
    tg_id = models.BigIntegerField('id пользователя')
    referral = models.BigIntegerField("кто пригласил", null=True, blank=True)
    full_name = models.CharField('полное имя пользовотеля', max_length=100)
    username = models.CharField('имя пользователя', max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} {self.username}"

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"
