from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot.keyboards.inline import get_main_inline_keyboard
from database.db import AvitoDatabase
from database.queries import AvitoQueries
from bot.middlewares.db_middleware import DBMiddleware

router = Router()

avito_db = AvitoDatabase()
db_middleware = DBMiddleware(avito_db)
router.message.middleware(db_middleware)

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

# Обработчик нажатия кнопки "Удалить ссылку"
@router.callback_query(lambda c: c.data == "delete_link")
async def process_delete_link(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Пожалуйста, отправьте ссылку, которую хотите удалить.")
    await state.set_state(LinkStates.deleting)
    await callback_query.answer()

# Обработчик ввода ссылки для добавления
@router.message(LinkStates.adding)
async def add_link(message: types.Message, state: FSMContext, queries: AvitoQueries):
    link = message.text
    telegram_id = message.from_user.id
    await queries.add_user_link(telegram_id=telegram_id, link=link)
    await message.answer(f"Ссылка '{link}' успешно добавлена.")
    await state.clear()

# Обработчик ввода ссылки для удаления
@router.message(LinkStates.deleting)
async def delete_link(message: types.Message, state: FSMContext, queries: AvitoQueries):
    link = message.text
    telegram_id = message.from_user.id
    user_links = await queries.get_user_links(telegram_id=telegram_id)
    link_to_delete = next((ul for ul in user_links if ul.link == link), None)
    if link_to_delete:
        await queries.delete_user_link(link_to_delete.id)
        await message.answer(f"Ссылка '{link}' успешно удалена.")
    else:
        await message.answer(f"Ссылка '{link}' не найдена среди ваших ссылок.")
    await state.clear()