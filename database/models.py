from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Items(Base):
    __tablename__ = 'items'

    avito_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(150))
    price: Mapped[int] = mapped_column(Integer)
    link: Mapped[str] = mapped_column(Text)

class UserLinks(Base):
    __tablename__ = 'user_links'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer)
    link: Mapped[str] = mapped_column(Text)