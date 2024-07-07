"""Получение отчета по текущим проблеммам в заббиксе."""
from configs.logs import logger
from configs.base import VPN_IMAGE
from utils.handlers import get_sessions, make_pretty_text
from utils.make_image_report_vpn import make_image


def sent_image(update, context) -> None:
    """Отправляет отчет о подключенныхъ VPN-соединениях."""
    try:
        if update.effective_chat is not None:
            # Получаем список текущих подключений
            logger.debug('Получаем список подключений.')
            get_sessions()

            # Получаем имя, ip-адрес и uptime
            logger.debug('Формируем словарь из нужных данных.')
            pretty_text = make_pretty_text()

            # Формируем изображение
            logger.debug('Формируем изображение с табличным отчетом.')
            make_image(pretty_text)

            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=open(VPN_IMAGE, 'rb')
            )
            logger.debug(
                f'Бот отправил отчет VPN для {update.effective_chat.id}')
        else:
            logger.warning('Не получен ID чата при запросе /sent_image.')
    except Exception as error:
        message = f'Ошибка отправки отчета VPN: {error}'
        logger.error(message)
