"""Кастомные классы обработки ошибок."""


class MissingVariable(Exception):
    """Исключение для проверки обязательных переменных окружения."""

    def __init__(self, name_env):
        self.name_env = name_env

    def __str__(self):
        return (f'MissingVariable: Отсутствует переменная окружения: '
                f'{self.name_env}')
