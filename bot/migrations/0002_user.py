# Generated by Django 3.0.5 on 2020-04-29 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=2, verbose_name='язык пользовотеля')),
                ('full_name', models.CharField(max_length=100, verbose_name='полное имя пользовотеля')),
                ('username', models.CharField(max_length=50, verbose_name='имя пользователя')),
            ],
        ),
    ]