import os
from .celery import celery_app
from django.conf import settings
from bot.parser.liquipediaParser import LiquidpediaDotaParser

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


@celery_app.task
def check_is_games_end(**kwargs):
    lp = LiquidpediaDotaParser(settings.PROJECT_DESCRIPTION)
    lp.check_games()
    lp.update_ongoing_and_upcoming_games()
    return {"status": True}



@celery_app.task
def update_played_games(**kwargs):
    lp = LiquidpediaDotaParser(settings.PROJECT_DESCRIPTION)
    lp.update_played_games()
    return {"status": True}


@celery_app.task
def update_teams(**kwargs):
    lp = LiquidpediaDotaParser(settings.PROJECT_DESCRIPTION)
    lp.update_teams()
    return {"status": True}

