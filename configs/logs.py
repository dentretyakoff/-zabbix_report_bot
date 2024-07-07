"""Настройка логирования."""
import logging
from logging.handlers import TimedRotatingFileHandler
from os import makedirs

# Каталог для логов
makedirs('logs', exist_ok=True)

# Создаем логгер
logger = logging.getLogger('zabbix-report')
logger.setLevel(logging.DEBUG)

# Создаем обработчики
log_file = './logs/log.log'
file_handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1)

# Создаем форматтер для сообщений лога
formatter = logging.Formatter(
    '%(asctime)s\t%(levelname)s\t%(message)s',
    '%Y-%m-%d %H:%M:%S'
)

# Настраиваем форматтеры для обработчиков
file_handler.setFormatter(formatter)

# Добавляем обработчики к логгеру
logger.addHandler(file_handler)
