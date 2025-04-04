from database.db import AvitoDatabase
from database.queries import AvitoQueries
from parser.parser import parse_page
from aiogram import Bot

async def check_new_items(bot: Bot):
    async with AvitoDatabase().session_maker() as session:
        queries = AvitoQueries(session)
        user_links = await queries.get_all_user_links()

        for user_link in user_links:
            new_items = []
            parsed_items = parse_page(user_link.link)

            for item in parsed_items:
                if not await queries.get_item(item['avito_id']):
                    await queries.add_or_update_item(
                        avito_id=item['avito_id'],
                        name=item['name'],
                        price=item['price'],
                        link=item['link']
                    )
                    new_items.append(item)

            if new_items:
                message = "Найдены новые товары:\n"
                for item in new_items:
                    message += f"{item['name']} - {item['price']} руб.\n{item['link']}\n\n"
                    await bot.send_message(user_link.telegram_id, message)
