from aiogram import executor
from django.core.management import BaseCommand

from .load_all import bot
from .config import admin_id


async def on_shutdown(dp):
    await bot.close()


async def on_startup(dp):
    await bot.send_message(admin_id, "Bot is running!")


class Command(BaseCommand):
    def handle(self, *args, **options):
        from .handler import dp
        executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup, skip_updates=True)
