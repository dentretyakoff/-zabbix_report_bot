"""Получение отчета по текущим проблеммам в заббиксе."""
from utils.handlers import get_api_answer, make_report
from configs.logs import logger


def report(update, context) -> None:
    """Отправляет список актуальных проблем в мониторинге Zabbix."""
    try:
        if update.effective_chat is not None:
            # Делаем запрос к API
            response = get_api_answer()
            user_name = update.message.from_user.username
            message = make_report(response, user_name)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode='HTML'
            )
            logger.debug(f'Бот отправил сообщение {message}')
        else:
            logger.warning('Не получен ID чата при запросе /report.')
    except Exception as error:
        message = f'Сбой в работе программы: {error}'
        logger.error(message)
