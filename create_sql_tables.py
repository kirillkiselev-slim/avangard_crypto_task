import sqlite3

import requests
from requests.exceptions import (ConnectionError, RequestException,
                                 TooManyRedirects, Timeout)

from constants_queries import (CREATE_CRYPTO_TABLE,
                               INSERT_CRYPTO_SLUG_NAMES, CREATE_USER_TABLE)
from constants_coinmarket import (LISTING_ENDPOINT_ALL_CRYPTOS,
                                  HEADERS_COINMARKET, PARAMS_COINMARKET)

con = sqlite3.connect('crypto_checker.db')


def create_crypto_table():
    try:
        con.execute(CREATE_CRYPTO_TABLE)
    except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
        print(e)


def create_user_table():
    try:
        con.execute(CREATE_USER_TABLE)
    except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
        print(e)


def insert_into_crypto():
    with con:
        listings = get_crypto_response()
        data_crypto = listings.get('data')
        sql_data = ((crypto.get('slug'),) for crypto in data_crypto)
        try:
            con.executemany(INSERT_CRYPTO_SLUG_NAMES, list(sql_data))
        except sqlite3.Error as e:
            print(e)


def get_crypto_response():
    try:
        response = requests.get(
            LISTING_ENDPOINT_ALL_CRYPTOS, headers=HEADERS_COINMARKET,
            params=PARAMS_COINMARKET)
        return response.json()
    except (ConnectionError, Timeout,
            TooManyRedirects, RequestException) as e:
        print(e)


if __name__ == '__main__':
    create_crypto_table()
    create_user_table()
    insert_into_crypto()
    con.close()


