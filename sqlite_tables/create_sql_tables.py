import sqlite3

import requests
from requests.exceptions import (ConnectionError, RequestException,
                                 TooManyRedirects, Timeout)

from constants.constants_queries import (CREATE_CRYPTO_TABLE,
                                         INSERT_CRYPTO_SLUG_NAMES,
                                         CREATE_USER_TABLE)
from constants.constants_coinmarket import (LISTING_ENDPOINT_ALL_CRYPTOS,
                                            HEADERS_COINMARKET,
                                            PARAMS_COINMARKET)
from exceptions import (CryptoTableError,
                        EndpointListingError, InputCryptoError)

con = sqlite3.connect('../crypto_checker.db')


def create_tables():
    try:
        con.execute(CREATE_CRYPTO_TABLE)
        con.execute(CREATE_USER_TABLE)
    except sqlite3.Error as err:
        raise CryptoTableError('Не смогли создать таблицу для криптовалюты'
                               ' или пользователя, она уже существует.') from err


def insert_into_crypto():
    with con:
        listings = get_crypto_response()
        data_crypto = listings.get('data')
        sql_data = ((crypto.get('slug'),) for crypto in data_crypto)
        try:
            con.executemany(INSERT_CRYPTO_SLUG_NAMES, list(sql_data))
        except sqlite3.Error as err:
            raise InputCryptoError('Ошибка наполнения таблицы crypto') from err


def get_crypto_response():
    try:
        response = requests.get(
            LISTING_ENDPOINT_ALL_CRYPTOS, headers=HEADERS_COINMARKET,
            params=PARAMS_COINMARKET)
        return response.json()
    except (ConnectionError, Timeout,
            TooManyRedirects, RequestException) as err:
        raise EndpointListingError('Ошибка при попытке получить'
                                   ' листинг всех криптовалют.') from err


def sql_main():
    create_tables()
    insert_into_crypto()
    con.close()
