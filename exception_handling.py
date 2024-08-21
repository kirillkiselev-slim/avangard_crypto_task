from typing import Tuple, Dict

import requests

from exceptions import TokensNotPresentError, EndpointQuotesError

TOKEN_NAMES = ('API_KEY', 'TELEGRAM_TOKEN')


def check_each_token(tokens: Tuple[str]):
    """Проверяет наличие каждого токена."""
    for token, token_name in zip(tokens, TOKEN_NAMES):
        if token is None:
            raise TokensNotPresentError(f'Отсутствует обязательная '
                                        f'переменная окружения: "{token_name}".'
                                        f'Программа принудительно'
                                        f' остановлена')


def check_response_status(response: requests.Response) -> Dict:
    """Проверяет код ответа от Coinmarketcap."""
    if response.status_code != 200:
        raise EndpointQuotesError(f'Эндпоинт недоступен со статусом'
                                  f' {response.status_code}: {response.text}')
    return response.json()
