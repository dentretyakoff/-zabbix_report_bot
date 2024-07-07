"""Стартовая команда бота."""
from telegram import ReplyKeyboardMarkup

from configs.logs import logger


def start(update, context) -> None:
    """Логика команды /start."""
    try:
        if update.effective_chat is not None:
            message: str = (
                'Показываю отчет по актуальным проблемам в заббиксе.'
                '\n======<b>Доступные команды</b>======\n'
                '- /start - приветственная информация\n'
                '- /report - список активных проблем\n'
                '- /vpn - список активных подключений vpn'
            )
            button = ReplyKeyboardMarkup([['/report'], ['/vpn']],
                                         resize_keyboard=True)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message, parse_mode='HTML',
                reply_markup=button
            )
        else:
            logger.warning('Не получен ID чата при запросе /start.')
    except Exception as error:
        message = f'Сбой в работе программы: {error}'
        logger.error(message)
