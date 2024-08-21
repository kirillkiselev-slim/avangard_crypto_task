import os
import sqlite3
import sys
import asyncio
from typing import List, Dict

import requests
from dotenv import load_dotenv

from exception_handling import check_each_token, check_response_status
from exceptions import TokensNotPresentError, SelectUserCryptoError
from constants.constants_coinmarket import (API_KEY, HEADERS_COINMARKET,
                                            QUOTES_ENDPOINT)
from constants.constants_telegram import PRICE_FOUND, DELETE_CRYPTO
from constants.constants_queries import SELECT_USER_CRYPTO
from logging_crypto import log_handler
from sqlite_tables.create_sql_tables import sql_main
from crypto_bot.telegram_handler import bot, crypto_bot_main
from shared_state import username_instance

load_dotenv()

DURATION_IN_SECONDS = 300

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

db_path = os.path.join(os.getenv('DB_DIR', 'data'), 'crypto_checker.db')


def check_tokens():
    """Проверяет наличие необходимых токенов."""
    try:
        check_each_token((API_KEY, TELEGRAM_TOKEN))
    except TokensNotPresentError as err:
        log_handler.logger.critical(err)
        sys.exit()


async def send_telegram_message(chat_id, message_text):
    await bot.send_message(chat_id, message_text)


def select_user_crypto(user: str) -> Dict:
    """Выбираем из базы данных всю инфу по крипте у пользователя."""
    try:

        with sqlite3.connect(db_path) as con:
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
    """Делаем запрос в CoinMarketCap с криптовалютами."""
    params = {'slug': users_crypto_names}
    response = requests.get(QUOTES_ENDPOINT, headers=HEADERS_COINMARKET,
                            params=params)
    crypto = check_response_status(response=response)
    return crypto


def parse_crypto(quotes: Dict) -> List:
    """Обрабатываем данные полученные с запроса выше."""
    result = []
    crypto_data = quotes.get('data')

    for crypto in crypto_data.values():
        slug = crypto.get('slug')

        price = crypto.get('quote').get('USD').get('price')
        result.append({'slug': slug, 'price': price})
    return result


async def crypto_main():
    """
    Основная функция для отслеживания криптовалют.
    Она вызывает вспомогательные функции для проверки токенов,
    работы с базой данных и выполнения основного цикла проверки цен криптовалют.

    В ходе работы функции:
    - Проверяются токены.
    - Создаем таблицы crypto и user (если они уже не созданы).
    - Получается имя пользователя и связанные с ним криптовалюты.
    - Полученные данные сравниваются с текущими ценами криптовалют.
    - Если цена криптовалюты попадает в заданный диапазон (максимум и минимум),
      пользователю отправляется уведомление.
    - После успешной отправки уведомления, данные криптовалюты могут быть очищены.

    Логирование используется для отслеживания ошибок и успешных операций.
    """

    success_message_sent = False
    check_tokens()

    try:
        sql_main()
    except Exception as err:
        log_handler.logger.critical(err)

    while True:
        try:
            username = username_instance.get_username()
            user_id = username_instance.get_user_id()
            current_user_data = select_user_crypto(username)

            if not current_user_data or not username:
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
                                   f'{price:.4f} USD')
                        log_handler.logger.debug(
                            f'Пользователь: {username} получил сообщение'
                            f' о криптовалюте {parsed_name}')

                        await bot.send_message(user_id, message)
                        success_message_sent = True

        except Exception as err:
            log_handler.logger.exception(err)

        finally:
            if success_message_sent:
                await bot.send_message(TELEGRAM_CHAT_ID, DELETE_CRYPTO)
                success_message_sent = False

            await asyncio.sleep(DURATION_IN_SECONDS)


async def main():
    """
    Функция для запуска основных задач программы.

    Она создает два параллельных задания:
    1. crypto_bot_main() — запускает бота для обработки команд и сообщений.
    2. crypto_main() — выполняет основное отслеживание криптовалют.

    Оба задания выполняются параллельно с помощью asyncio.gather().
    """

    bot_task = asyncio.create_task(crypto_bot_main())
    main_task = asyncio.create_task(crypto_main())

    await asyncio.gather(bot_task, main_task)


if __name__ == '__main__':
    asyncio.run(main())
