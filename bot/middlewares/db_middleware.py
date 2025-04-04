from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Dict, Any
from aiogram.types import TelegramObject
from database.db import AvitoDatabase
from database.queries import AvitoQueries


class DBMiddleware(BaseMiddleware):
    def __init__(self, db: AvitoDatabase):
        self.db = db

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with self.db.session_maker() as session:
            data["queries"] = AvitoQueries(session)
            return await handler(event, data)