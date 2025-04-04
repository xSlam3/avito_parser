from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker

from database.models import Base



class AvitoDatabase():
    def __init__(self):
        self.db_url = "sqlite+aiosqlite:///./test.db"
        self.engine: AsyncEngine = create_async_engine(self.db_url, echo=True)
        self.session_maker = async_sessionmaker(bind=self.engine, expire_on_commit=False)

    async def create_tables(self):
        """Создание всех таблиц"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self):
        """Удаление всех таблиц"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)