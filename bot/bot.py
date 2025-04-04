from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from bot.config_data.config import Config, load_config
from bot.filters.allowed_user import IsAllowedUser
from bot.handlers import commands
from database.db import AvitoDatabase
from scheduler.scheduler import Scheduler


async def start_bot():
    config: Config = await load_config()

    bot = Bot(token=config.bot.token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    db = AvitoDatabase()

    await db.create_tables()

    scheduler = Scheduler(bot)
    scheduler.start_scheduler()

    dp.include_router(commands.router)
    dp.message.filter(IsAllowedUser(config.allowed_user.telegram_id))
    dp.callback_query.filter(IsAllowedUser(config.allowed_user.telegram_id))

    await bot.delete_webhook(drop_pending_updates=True)


    await dp.start_polling(bot)