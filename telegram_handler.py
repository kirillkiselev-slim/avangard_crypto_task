import asyncio
import os
import re
import sqlite3
from typing import Tuple

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from aiogram.utils.formatting import Text, Bold

from constants_telegram import (START_MESSAGE, EXAMPLE_FORMAT_MESSAGE,
                                COPY_ME, REGEX, NOT_VALID_FORMAT,
                                CRYPTO_IS_NOT_VALID,
                                INCORRECT_MAX_AND_MIN_VALUES,
                                JUST_ONE_CRYPTO)
from constants_queries import CHECK_CRYPTO_EXISTENCE, INSERT_USER_CRYPTO

bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: types.Message) -> None:
    content = Text(
        'Привет, ',
        Bold(message.from_user.full_name)
    )
    await message.answer(**content.as_kwargs())
    await message.answer(START_MESSAGE)


@dp.message(Command('format'))
async def cmd_format(message: types.Message) -> None:
    await message.answer(COPY_ME)
    await message.answer(
        EXAMPLE_FORMAT_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2)


@dp.message()
async def handle_input(message: types.Message):
    accepted_cryptos = []
    message_is_valid = validate_users_input(message=message.text)

    if not message_is_valid[1]:
        warning_message = message_is_valid[0]
        return await message.answer(warning_message)

    user_input = message_is_valid[0]

    with sqlite3.connect('crypto_checker.db') as con:
        cur = con.cursor()

        for crypto in user_input:
            crypto_name, max_val, min_val = crypto
            lower_crypto_name = crypto_name.lower()
            query = cur.execute(
                CHECK_CRYPTO_EXISTENCE, (lower_crypto_name,))
            if float(max_val) <= float(min_val):
                return await message.answer(
                    f'Для криптовалюты "{crypto_name}"'
                    f'{INCORRECT_MAX_AND_MIN_VALUES}')
            if query.fetchone() is None:
                return await message.answer(
                    f'Криптовалюты "{crypto_name}"{CRYPTO_IS_NOT_VALID}')

            cur.execute(
                INSERT_USER_CRYPTO,
                (message.from_user.username, lower_crypto_name,
                 max_val, min_val))
            accepted_cryptos.append(crypto_name)
        return await message.answer(
            f'"{"и ".join([crypto for crypto in accepted_cryptos])} сохранили.')


def validate_users_input(message: str) -> Tuple:
    regex = re.compile(REGEX)
    matches = regex.findall(message.strip())

    if not matches:
        return NOT_VALID_FORMAT, False
    if len(matches) != 2:
        return JUST_ONE_CRYPTO, False

    return matches, True


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
