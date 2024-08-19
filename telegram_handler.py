import asyncio
import os
import re
import sqlite3

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from aiogram.utils.formatting import Text, Bold

from constants_telegram import (START_MESSAGE, EXAMPLE_FORMAT_MESSAGE, COPY_ME, REGEX,
                                NOT_VALID_FORMAT, CRYPTO_IS_NOT_VALID)
from constants_queries import CHECK_CRYPTO_EXISTENCE

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
    users_message = message.text

    user_crypto_dict = {}
    message_is_valid = validate_users_input(message=users_message)
    if not message_is_valid:
        await message.answer(NOT_VALID_FORMAT)

    for crypto in users_message:
        crypto_name, max_val, min_val = crypto
        user_crypto_dict[crypto_name] = {
            'max': float(max_val),
            'min': float(min_val)
        }

    for user_crypto, values in user_crypto_dict:
        with sqlite3.connect('crypto_checker.db') as con:
            con.cursor()
            query = con.execute(CHECK_CRYPTO_EXISTENCE, user_crypto)
            if not query:
                print(f'{user_crypto}{CRYPTO_IS_NOT_VALID}')
    print(f'Вы отслеживаете:\n {user_crypto_dict.keys()} - '
          f'Максимум: {values['max']}, '
          f'Минимум: {values['min']}\n')


def validate_users_input(message: str) -> bool:
    regex = re.compile(REGEX)
    matches = regex.findall(message.strip())
    if not matches:
        return False
    if len(matches) != 2:
        return False
    return True


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
