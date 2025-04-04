from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

# Создаем билдер для инлайн-клавиатуры
def get_main_inline_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Добавить ссылку", callback_data="add_link")
    builder.button(text="Удалить ссылку", callback_data="delete_link")
    builder.adjust(1)  # Располагаем кнопки в один столбец
    return builder.as_markup()
