import os

from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv

@dataclass
class Bot():
    token: str

@dataclass
class AllowedId():
    telegram_id: int

@dataclass
class Config():
    bot: Bot
    allowed_user: AllowedId

async def load_config():
    find_dotenv()
    load_dotenv()
    return Config(Bot(token=os.getenv('BOT_TOKEN')), AllowedId(telegram_id=int(os.getenv("ALLOWED_ID"))))