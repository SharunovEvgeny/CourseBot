from aiogram import executor
from django.core.management import BaseCommand
from django.conf import settings

from .load_all import bot
from ...models import BotUser


async def on_shutdown(dp):
    await bot.close()


async def on_startup(dp):
    admins = BotUser.objects.filter(is_admin=True)
    for admin in admins:
        await bot.send_message(admin.tg_id, "Bot is running!")


class Command(BaseCommand):
    def handle(self, *args, **options):
        from .load_all import dp

        """
        Comment on, if you are starting bot at the first time,
        then comment off, when bot started.
        
        """
        from bot.parser.liquipediaParser import LiquidpediaDotaParser
        lp = LiquidpediaDotaParser(settings.PROJECT_DESCRIPTION)
        lp.update_teams()
        lp.update_played_games()
        # lp.check_games()
        lp.update_ongoing_and_upcoming_games()
        executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup, skip_updates=True)
