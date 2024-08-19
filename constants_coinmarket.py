import os

from dotenv import load_dotenv

load_dotenv()

LISTING_ENDPOINT_ALL_CRYPTOS = ('https://pro-api.coinmarketcap.com/v1/'
                                'cryptocurrency/listings/latest')

COINMARKET_API_KEY = os.getenv('COINMARKET_API_KEY')

# LISTING_ENDPOINT_ALL_CRYPTOS = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

HEADERS_COINMARKET = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': os.getenv('COINMARKET_API_KEY'),
}

PARAMS_COINMARKET = {
    'start': 1,
    'limit': 5000,
}
