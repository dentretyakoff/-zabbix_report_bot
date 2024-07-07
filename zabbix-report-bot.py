"""Основная логика бота и его запуск."""
import datetime as dt
from os import getenv

import pytz
from telegram.ext import CommandHandler, Updater

from configs.logs import logger
from utils.handlers import check_tokens, daily_report
from bot_commands.report import report
from bot_commands.start import start
from bot_commands.sent_image import sent_image
from configs.base import TIMEZONE, PROXY_URL


# Проверяем наличие переменных окружения
check_tokens()
TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')
TIME_ZONE = pytz.timezone(TIMEZONE)


def main():
    """Основная логика работы бота."""
    logger.info('Бот запущен')

    # Создаем бота
    application = Updater(token=TELEGRAM_TOKEN,
                          request_kwargs={'proxy_url': PROXY_URL})

    # Обработчики команд
    start_handler = CommandHandler('start', start)
    application.dispatcher.add_handler(start_handler)

    start_handler = CommandHandler('report', report)
    application.dispatcher.add_handler(start_handler)

    start_handler = CommandHandler('vpn', sent_image)
    application.dispatcher.add_handler(start_handler)

    # Задания по расписанию
    application.job_queue.run_daily(daily_report,
                                    time=dt.time(hour=7, minute=0,
                                                 second=0, tzinfo=TIME_ZONE))
    application.job_queue.run_daily(daily_report,
                                    time=dt.time(hour=21, minute=0,
                                                 second=0, tzinfo=TIME_ZONE))

    application.start_polling(poll_interval=20.0)

    application.idle()


if __name__ == '__main__':
    main()
