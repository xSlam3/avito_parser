import re

import requests
import logging
from bs4 import BeautifulSoup
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_soup(url: str) -> Optional[BeautifulSoup]:
    """Получает HTML-страницу и парсит её с помощью BeautifulSoup."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка запроса: {e}")
        return None


def find_item_tags(soup: BeautifulSoup):
    """Находит все теги товаров на странице."""
    return soup.find_all('div', class_='iva-item-root-Se7z4')


def find_item_name(item: BeautifulSoup) -> Optional[str]:
    """Извлекает название товара."""
    name_tag = item.find('h3', {'itemprop': 'name'})
    return name_tag.get_text(strip=True) if name_tag else None


def find_item_link(item: BeautifulSoup) -> Optional[str]:
    """Извлекает ссылку на товар."""
    link_tag = item.find('a', {'itemprop': 'url', 'data-marker': 'item-title'})
    return f"https://www.avito.ru{link_tag['href']}" if link_tag and link_tag.has_attr('href') else None


def find_item_price(item: BeautifulSoup) -> Optional[str]:
    """Извлекает цену товара."""
    price_tag = item.find('meta', {'itemprop': 'price'})
    return price_tag["content"] if price_tag and price_tag.has_attr("content") else None


def extract_avito_id(link: Optional[str]) -> Optional[str]:
    """
    Извлекает ID объявления из ссылки на Avito.
    Пример:
      https://www.avito.ru/..._1234567890?context=... -> 1234567890
    Новое регулярное выражение ищет 10-значное число, предваряемое символом '_' или '/'.
    """
    if not link:
        return None

    pattern = r'[_/](\d{10})(?:\?|$)'
    match = re.search(pattern, link)
    if match:
        avito_id = match.group(1)
        logging.debug("Извлечен ID %s из ссылки: %s", avito_id, link)
        return avito_id
    logging.warning("Не удалось извлечь ID из ссылки: %s", link)
    return None

def parse_page(url: str) -> List[Dict[str, Optional[str]]]:
    """Парсит одну страницу и собирает товары."""
    all_items = []

    if not url or "avito.ru" not in url:
        logging.error("Некорректный URL: %s", url)
        return all_items

    try:
        soup = get_soup(url)
        if not soup:
            return all_items

        items = find_item_tags(soup)
        parsed_items = []

        for item in items:
            try:
                parsed_items.append({
                    'name': find_item_name(item),
                    'link': find_item_link(item),
                    'price': find_item_price(item),
                    'avito_id': extract_avito_id(find_item_link(item))
                })
            except Exception as e:
                logging.error(f"Ошибка парсинга элемента: {e}")
                continue

        all_items.extend(parsed_items)
        logging.info(f"Спарсено {len(parsed_items)} товаров с {url}")

    except Exception as e:
        logging.error(f"Ошибка парсинга страницы: {e}")

    return all_items