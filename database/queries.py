from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models import Items, UserLinks


class AvitoQueries:
    def __init__(self, session: AsyncSession):
        self.session = session

    # Items operations
    async def add_or_update_item(self, avito_id: int, name: str, price: int, link: str) -> Items:
        """Добавление или обновление товара (upsert)"""
        item = await self.session.get(Items, avito_id)
        if item:
            item.name = name
            item.price = price
            item.link = link
        else:
            item = Items(avito_id=avito_id, name=name, price=price, link=link)
            self.session.add(item)

        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def get_item(self, avito_id: int) -> Items | None:
        """Получение товара по avito_id"""
        return await self.session.get(Items, avito_id)

    async def delete_item(self, avito_id: int) -> bool:
        """Удаление товара"""
        item = await self.session.get(Items, avito_id)
        if item:
            await self.session.delete(item)
            await self.session.commit()
            return True
        return False

    async def get_all_items(self) -> list[Items]:
        """Получение всех товаров"""
        result = await self.session.execute(select(Items))
        return result.scalars().all()

    # UserLinks operations
    async def add_user_link(self, telegram_id: int, link: str) -> UserLinks:
        """Добавление новой ссылки пользователя"""
        user_link = UserLinks(telegram_id=telegram_id, link=link)
        self.session.add(user_link)
        await self.session.commit()
        await self.session.refresh(user_link)
        return user_link

    async def get_user_link_by_id(self, link_id: int) -> UserLinks | None:
        """Получение ссылки по ID"""
        return await self.session.get(UserLinks, link_id)

    async def get_user_links(self, telegram_id: int) -> list[UserLinks]:
        """Получение всех ссылок пользователя"""
        result = await self.session.execute(
            select(UserLinks)
            .where(UserLinks.telegram_id == telegram_id)
            .order_by(UserLinks.id)
        )
        return result.scalars().all()

    async def get_all_user_links(self) -> list[UserLinks]:
        """Получение всех ссылок всех пользователей"""
        result = await self.session.execute(
            select(UserLinks)
            .order_by(UserLinks.telegram_id, UserLinks.id)
        )
        return result.scalars().all()

    async def delete_user_link(self, link_id: int) -> bool:
        """Удаление ссылки пользователя по ID"""
        user_link = await self.session.get(UserLinks, link_id)
        if user_link:
            await self.session.delete(user_link)
            await self.session.commit()
            return True
        return False

    async def delete_user_links(self, telegram_id: int) -> int:
        """Удаление всех ссылок пользователя"""
        result = await self.session.execute(
            delete(UserLinks)
            .where(UserLinks.telegram_id == telegram_id)
        )
        await self.session.commit()
        return result.rowcount