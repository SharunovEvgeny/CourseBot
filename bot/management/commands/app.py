import inspect
import os

from aiogram import executor
from django.core.management import BaseCommand
from django.conf import settings
import logging
from .load_all import bot

from ...models import BotUser, Game, Coefficient
from ...prediction.functions import calculate_all_teams_power
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"



async def on_shutdown(dp):
    await bot.close()


async def on_startup(dp):
    admins = BotUser.objects.filter(is_admin=True)
    for admin in admins:
        await bot.send_message(admin.tg_id, "Bot is running!")


class Command(BaseCommand):
    def handle(self, *args, **options):
        from .dialogs.general.handlers import dp
        """
        Comment on, if you are starting bot at the first time,
        then comment off, when bot started.
        
        """
        from bot.parser.liquipediaParser import LiquidpediaDotaParser
        lp = LiquidpediaDotaParser(settings.PROJECT_DESCRIPTION)

        if Game.objects.all().count() == 0:
            logging.info("Starting updating games...")
            lp.update_teams()
            lp.update_played_games()
            Coefficient.objects.get_or_create(name='joint_games_cof', value=15)
            Coefficient.objects.get_or_create(name='format_cof', value=5)
            logging.info("Done updating games!")
        calculate_all_teams_power()
        logging.info("Starting checking games...")
        lp.check_games()
        logging.info("Done checking games!")
        lp.update_ongoing_and_upcoming_games()
        executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup, skip_updates=True)
