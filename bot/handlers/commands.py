import logging

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline import get_main_inline_keyboard, generate_links_keyboard
from database.db import AvitoDatabase
from database.queries import AvitoQueries
from bot.middlewares.db_middleware import DBMiddleware

router = Router()

avito_db = AvitoDatabase()
db_middleware = DBMiddleware(avito_db)
router.message.middleware(db_middleware)
router.callback_query.middleware(db_middleware)


# Определение состояний для добавления и удаления ссылок
class LinkStates(StatesGroup):
    adding = State()
    deleting = State()


# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=get_main_inline_keyboard())


# Обработчик нажатия кнопки "Добавить ссылку"
@router.callback_query(lambda c: c.data == "add_link")
async def process_add_link(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Пожалуйста, отправьте ссылку, которую хотите добавить.")
    await state.set_state(LinkStates.adding)
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "select_link_to_remove")
async def process_add_link(callback_query: CallbackQuery, state: FSMContext, queries: AvitoQueries):
    telegram_id = callback_query.from_user.id
    user_links = await queries.get_user_links(telegram_id=telegram_id)

    if not user_links:
        await callback_query.message.answer("У вас нет сохранённых ссылок.")
        return

    keyboard = generate_links_keyboard(user_links)
    await callback_query.message.answer("Выберите ссылку для удаления:", reply_markup=keyboard)
    await state.set_state(LinkStates.choosing)


# Обработчик ввода ссылки для добавления
@router.message(LinkStates.adding)
async def add_link(message: types.Message, state: FSMContext, queries: AvitoQueries):
    link = message.text
    telegram_id = message.from_user.id
    await queries.add_user_link(telegram_id=telegram_id, link=link)
    await message.answer(f"Ссылка '{link}' успешно добавлена.")
    await state.clear()


# Обработчик нажатия на кнопку удаления ссылки
@router.callback_query(lambda c: c.data.startswith("delete_"))
async def process_delete_link_callback(
        callback_query: CallbackQuery,
        state: FSMContext,
        queries: AvitoQueries
):
    try:
        # Извлекаем ссылку из callback_data (формат "delete_https://www.avito.ru/...")
        link = callback_query.data.split("_", 1)[1]
        telegram_id = callback_query.from_user.id

        # Получаем все ссылки пользователя
        user_links = await queries.get_user_links(telegram_id=telegram_id)

        # Ищем ссылку для удаления
        link_to_delete = next((ul for ul in user_links if ul.link == link), None)

        if link_to_delete:
            # Удаляем по ID найденной записи
            await queries.delete_user_link(link_to_delete.id)
            await callback_query.message.edit_text(
                f"Ссылка '{link_to_delete.link}' успешно удалена."
            )
        else:
            await callback_query.message.edit_text(
                "Не удалось найти ссылку для удаления."
            )

        await state.clear()
        await callback_query.answer()

    except Exception as e:
        await callback_query.answer(
            "Произошла ошибка при удалении ссылки",
            show_alert=True
        )
        logging.error(f"Error deleting link: {e}")
