import os

from dotenv import load_dotenv

load_dotenv()

LISTING_ENDPOINT_ALL_CRYPTOS = ('https://pro-api.coinmarketcap.com/v1/'
                                'cryptocurrency/listings/latest')
QUOTES_ENDPOINT = ('https://pro-api.coinmarketcap.com/v2/'
                   'cryptocurrency/quotes/latest')

API_KEY = os.getenv('API_KEY')

HEADERS_COINMARKET = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}

PARAMS_COINMARKET = {
    'start': 1,
    'limit': 5000,
}
