import os
import sqlite3
import sys
import asyncio
from typing import List, Dict, Optional

from aiogram.types import Message
import requests
from dotenv import load_dotenv

from exception_handling import check_each_token, check_response_status
from exceptions import TokensNotPresentError, SelectUserCryptoError
from constants.constants_coinmarket import (API_KEY, HEADERS_COINMARKET,
                                            QUOTES_ENDPOINT)
from constants.constants_telegram import PRICE_FOUND
from constants.constants_queries import SELECT_USER_CRYPTO
from logging_crypto import log_handler
from sqlite_tables.create_sql_tables import sql_main
from crypto_bot.telegram_handler import bot, get_username

load_dotenv()

DURATION_IN_SECONDS = 60

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def check_tokens():
    """Проверяет наличие необходимых токенов."""
    try:
        check_each_token((API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID))
    except TokensNotPresentError as err:
        log_handler.logger.critical(err)
        sys.exit()


async def send_telegram_message(chat_id, message_text):
    await bot.send_message(chat_id, message_text)


def select_user_crypto(user: str) -> Dict:
    try:
        with sqlite3.connect('crypto_checker.db') as con:
            cur = con.cursor()
            cur.execute(SELECT_USER_CRYPTO, (user,))
            rows = cur.fetchall()
            user_data_dict = {crypto[0]: (crypto[1], crypto[2])
                              for crypto in rows}
            return user_data_dict
    except sqlite3.Error as err:
        raise SelectUserCryptoError(f'Ошибка при получении данных из бд '
                                    f'о криптовалюте от пользователя') from err


def get_crypto(users_crypto_names: str) -> Dict:
    params = {'slug': users_crypto_names}
    response = requests.get(QUOTES_ENDPOINT, headers=HEADERS_COINMARKET,
                            params=params)
    crypto = check_response_status(response=response)
    return crypto


def parse_crypto(quotes: Dict) -> List:
    result = []
    crypto_data = quotes.get('data')

    for crypto in crypto_data.values():
        slug = crypto.get('slug')

        price = crypto.get('quote').get('USD').get('price')
        result.append({'slug': slug, 'price': price})
    return result


async def main():
    await asyncio.to_thread(check_tokens)

    try:
        await asyncio.to_thread(sql_main)
    except Exception as err:
        log_handler.logger.critical(err)

    while True:
        try:
            username = get_username()
            current_user_data = select_user_crypto(username)

            if not current_user_data:
                continue

            users_crypto_names = current_user_data.keys()

            crypto_names_str = ','.join(users_crypto_names)
            coinmarketcap_data = get_crypto(crypto_names_str)
            parsed_crypto = parse_crypto(coinmarketcap_data)

            for crypto in parsed_crypto:
                price = crypto.get('price')
                parsed_name = crypto.get('slug')

                if parsed_name in current_user_data:
                    max_value, min_value = current_user_data[parsed_name]
                    if min_value <= price <= max_value:
                        message = (f'Нашли! {parsed_name}{PRICE_FOUND}'
                                   f'{price:.4f}')
                        await bot.send_message(TELEGRAM_CHAT_ID, message)

        except Exception as err:
            log_handler.logger.exception(err)

        finally:
            await asyncio.sleep(DURATION_IN_SECONDS)


if __name__ == '__main__':
    asyncio.run(main())
