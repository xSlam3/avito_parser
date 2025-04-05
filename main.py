import asyncio
import logging

from bot.bot import TgBot
from bot.config_data.config import Config, load_config
from database.db import AvitoDatabase

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logging.getLogger("sqlalchemy.engine.Engine").handlers = [logging.NullHandler()]


async def main():
    config: Config = await load_config()
    bot = TgBot(bot_token=config.bot.token, allowed_id=config.allowed_user.telegram_id)
    db = AvitoDatabase()

    await db.create_tables()
    await bot.start_bot()



if __name__ == "__main__":
    asyncio.run(main())
