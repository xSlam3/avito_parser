from apscheduler.schedulers.asyncio import AsyncIOScheduler
from scheduler.notificator import check_new_items
from aiogram import Bot

class Scheduler:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()

    def start_scheduler(self):
        self.scheduler.add_job(check_new_items, 'interval', minutes=1, kwargs={'bot': self.bot})
        self.scheduler.start()
