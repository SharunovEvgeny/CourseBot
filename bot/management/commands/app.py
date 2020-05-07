from aiogram import executor
from django.core.management import BaseCommand
from django.conf import settings

from .load_all import bot
from ...models import BotUser, Game


async def on_shutdown(dp):
    await bot.close()


async def on_startup(dp):
    admins = BotUser.objects.filter(is_admin=True)
    for admin in admins:
        await bot.send_message(admin.tg_id, "Bot is running!")


class Command(BaseCommand):
    def handle(self, *args, **options):
        from .load_all import dp

        from bot.parser.liquipediaParser import LiquidpediaDotaParser
        lp = LiquidpediaDotaParser(settings.PROJECT_DESCRIPTION)
        if Game.objects.all().count()==0:
            lp.update_teams()
            lp.update_played_games()
        else:
            lp.check_games()
        lp.update_ongoing_and_upcoming_games()
        executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup, skip_updates=True)
