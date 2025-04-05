from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Создаем билдер для инлайн-клавиатуры
def get_main_inline_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Добавить ссылку", callback_data="add_link")
    builder.button(text="Удалить ссылку", callback_data="select_link_to_remove")
    builder.adjust(1)  # Располагаем кнопки в один столбец
    return builder.as_markup()


def generate_links_keyboard(user_links):
    buttons = []
    for link in user_links:
        # Важно: экранируем ссылку, если она содержит специальные символы
        callback_data = f"delete_{link.link}"
        buttons.append(
            InlineKeyboardButton(
                text=link.link,  # или более короткое описание
                callback_data=callback_data
            )
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return keyboard