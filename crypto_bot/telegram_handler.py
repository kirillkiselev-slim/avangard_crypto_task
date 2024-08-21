# import asyncio
import os
import re
# import sqlite3
from datetime import datetime
from typing import Tuple
import aiosqlite

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from aiogram.utils.formatting import Text, Bold

from constants.constants_telegram import (START_MESSAGE,
                                          EXAMPLE_FORMAT_MESSAGE,
                                          COPY_ME, REGEX, NOT_VALID_FORMAT,
                                          CRYPTO_IS_NOT_VALID,
                                          INCORRECT_MAX_AND_MIN_VALUES,
                                          JUST_ONE_CRYPTO, CRYPTO_SAVED)
from constants.constants_queries import (CHECK_CRYPTO_EXISTENCE,
                                         INSERT_USER_CRYPTO,
                                         DELETE_USER_CRYPTO)
from shared_state import username_instance

db_path = os.path.abspath('crypto_checker.db')
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


@dp.message(Command('stop'))
async def cmd_stop(message: types.Message) -> None:
    username = message.from_user.username
    async with aiosqlite.connect(db_path) as con:
        await con.execute(DELETE_USER_CRYPTO, (username,))
        await con.commit()
    await message.answer(f'Остановили отслеживание.')


@dp.message(Command('format'))
async def cmd_format(message: types.Message) -> None:
    await message.answer(COPY_ME)
    await message.answer(
        EXAMPLE_FORMAT_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2)


@dp.message()
async def handle_input(message: types.Message):
    message_is_valid = validate_users_input(message=message.text)

    if not message_is_valid[1]:
        warning_message = message_is_valid[0]
        return await message.answer(warning_message)

    user_input = message_is_valid[0]

    accepted_cryptos = []
    username = message.from_user.username
    username_instance.set_username(username)

    date_added = datetime.now().isoformat()

    async with aiosqlite.connect(db_path) as con:
        await con.execute(DELETE_USER_CRYPTO, (username,))
        await con.commit()

        for crypto in user_input:
            crypto_name, max_val, min_val = crypto
            lower_crypto_name = crypto_name.lower()

            async with con.execute(CHECK_CRYPTO_EXISTENCE, (lower_crypto_name,)) as cursor:
                query = await cursor.fetchone()
                if float(max_val) <= float(min_val):
                    return await message.answer(
                        f'Для криптовалюты "{crypto_name}"'
                        f'{INCORRECT_MAX_AND_MIN_VALUES}'
                    )
                if query is None:
                    return await message.answer(
                        f'Криптовалюты "{crypto_name}"{CRYPTO_IS_NOT_VALID}'
                    )

            await con.execute(
                INSERT_USER_CRYPTO,
                (username, lower_crypto_name, max_val, min_val, date_added)
            )
            accepted_cryptos.append(crypto_name)

        await con.commit()

        return await message.answer(
            f'{" и ".join([crypto for crypto in accepted_cryptos])}'
            f'{CRYPTO_SAVED}'
        )


def validate_users_input(message: str) -> Tuple:
    regex = re.compile(REGEX)
    matches = regex.findall(message.strip())

    if not matches:
        return NOT_VALID_FORMAT, False
    if len(matches) != 2:
        return JUST_ONE_CRYPTO, False

    return matches, True


async def crypto_bot_main():
    await dp.start_polling(bot)
