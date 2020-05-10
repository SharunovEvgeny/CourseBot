# Generated by Django 3.0.6 on 2020-05-08 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_id', models.BigIntegerField(verbose_name='id пользователя')),
                ('referral', models.BigIntegerField(blank=True, null=True, verbose_name='кто пригласил')),
                ('full_name', models.CharField(max_length=100, verbose_name='полное имя пользовотеля')),
                ('username', models.CharField(blank=True, max_length=50, null=True, verbose_name='имя пользователя')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Админ ли?')),
            ],
            options={
                'verbose_name': 'Пользователь бота',
                'verbose_name_plural': 'Пользователи бота',
            },
        ),
        migrations.CreateModel(
            name='Coefficient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Тир')),
                ('value', models.FloatField(verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Коэфицент',
                'verbose_name_plural': 'Коэфиценты',
            },
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('risk_bet_successful', models.IntegerField(default=0, verbose_name='количество успешных рискованных ставок')),
                ('risk_bet_all', models.IntegerField(default=0, verbose_name='всего количетсво рискованных ставок')),
                ('safe_bet_successful', models.IntegerField(default=0, verbose_name='количество успешных сейвовых ставок')),
                ('safe_bet_all', models.IntegerField(default=0, verbose_name='всего количетсво сейвовых ставок')),
                ('unpredictable_bet_successful', models.IntegerField(default=0, verbose_name='количество непредсказуемых рискованных ставок')),
                ('unpredictable_bet_all', models.IntegerField(default=0, verbose_name='всего непредсказуемых рискованных ставок')),
                ('all_bet_successful', models.IntegerField(default=0, verbose_name='количество успешных ставок всего')),
                ('bet_all', models.IntegerField(default=0, verbose_name='всего количетсво  ставок')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название')),
                ('link', models.CharField(max_length=60, verbose_name='Ссылка')),
                ('power', models.FloatField(default=0, verbose_name='Сила')),
                ('time_change_compound', models.DateTimeField(blank=True, null=True, verbose_name='Время последнего изменения в составе команды')),
            ],
            options={
                'verbose_name': 'Команда',
                'verbose_name_plural': 'Команды',
            },
        ),
        migrations.CreateModel(
            name='Tier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Тир')),
                ('coefficient', models.FloatField(blank=True, default=1, null=True, verbose_name='Коэфицент тира')),
            ],
            options={
                'verbose_name': 'Тир',
                'verbose_name_plural': 'Тиры',
            },
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('tier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bot.Tier')),
            ],
            options={
                'verbose_name': 'Турнир',
                'verbose_name_plural': 'Турниры',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='Имя фамилия')),
                ('nickname', models.CharField(max_length=255, verbose_name='Ник в игре')),
                ('country', models.CharField(max_length=100, verbose_name='Страна')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='players', to='bot.Team', verbose_name='Команда')),
            ],
            options={
                'verbose_name': 'Игрок',
                'verbose_name_plural': 'Игроки',
            },
        ),
        migrations.CreateModel(
            name='GameNow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('format', models.CharField(blank=True, max_length=3, null=True, verbose_name='формат')),
                ('starttime', models.DateTimeField(blank=True, null=True, verbose_name='Время игры')),
                ('predict', models.SmallIntegerField(blank=True, null=True, verbose_name='процент на победу первой команды')),
                ('team1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team1_now', to='bot.Team', verbose_name='Команда 1')),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team2_now', to='bot.Team', verbose_name='Команда 2')),
                ('tournament', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bot.Tournament', verbose_name='Турнир')),
            ],
            options={
                'verbose_name': 'Игра Сейчас',
                'verbose_name_plural': 'Игры Сейчас',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team1_score', models.SmallIntegerField(blank=True, null=True, verbose_name='Очки первой команды')),
                ('team2_score', models.SmallIntegerField(blank=True, null=True, verbose_name='Очки второй команды')),
                ('format', models.CharField(blank=True, max_length=3, null=True, verbose_name='формат')),
                ('starttime', models.DateTimeField(blank=True, null=True, verbose_name='Время игры')),
                ('predict', models.SmallIntegerField(blank=True, null=True, verbose_name='процент на победу первой команды')),
                ('team1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team1_game', to='bot.Team', verbose_name='Команда 1')),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team2_game', to='bot.Team', verbose_name='Команда 2')),
                ('tournament', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bot.Tournament', verbose_name='Турнир')),
            ],
            options={
                'verbose_name': 'Игра',
                'verbose_name_plural': 'Игры',
            },
        ),
    ]
