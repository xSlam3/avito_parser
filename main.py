import asyncio
import logging

from bot.bot import start_bot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logging.getLogger("sqlalchemy.engine.Engine").handlers = [logging.NullHandler()]



if __name__ == "__main__":
    asyncio.run(start_bot())