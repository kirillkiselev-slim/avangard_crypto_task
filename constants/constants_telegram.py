from dotenv import load_dotenv

load_dotenv()


REGEX = (r'([a-zA-Z0-9-]+):\s*max:\s*(\d*\.?\d{1,8}?)'
         r'\s*min:\s*(\d*\.?\d{1,8}?)')

START_MESSAGE = (
    'Введите 2 криптовалюты (одним сообщением), которые нужно отслеживать, а также максимальное'
    ' и минимальное пороговое значение для каждой из них.\U0001F4B2\n'
    'Нажмите на /format, чтобы скопировать нужный шаблон для сообщения. '
    'Просто скопируй сообщение и замени жирный текст на свои значения.'
)

COPY_ME = '\u2B07\uFE0FСкопируй это сообщение\u2B07\uFE0F'

EXAMPLE_FORMAT_MESSAGE = (
    '***Криптовалюта №1***:\n'
    'max: ***Макс\\. пороговое значение для крипты №1***\n'
    'min: ***Мин\\. пороговое значение для крипты №1***\n\n'
    '***Криптовалюта №2***:\n'
    'max: ***Макс\\. пороговое значение для крипты №2***\n'
    'min: ***Мин\\. пороговое значение для крипты №2***'
)

NOT_VALID_FORMAT = ('Убедитесь, что вводите криптовалюту в правильном формате. '
                    'Используйте /format как шаблон.')

JUST_ONE_CRYPTO = ('Убедитесь, что ввели обе криптовалюты и их'
                   ' значения в одном сообщении.')

INCORRECT_MAX_AND_MIN_VALUES = (' макс. пороговое значение не может быть'
                                ' меньше или ровно мин. значения.'
                                ' Исправьте, пожалуйста и пришлите '
                                'сообщение еще раз.')

CRYPTO_IS_NOT_VALID = (' не существует, либо она некорректно указана. '
                       'Исправьте, пожалуйста и пришлите сообщение еще раз.')

CRYPTO_SAVED = (' сохранили. Сообщим вам, '
                'если будет достигнуто одно из значений.')
