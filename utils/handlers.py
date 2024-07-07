"""Обработчики параметров."""
import sys
import os
import re

import telegram
import paramiko
from dotenv import load_dotenv
from pyzabbix import ZabbixAPI

from exceptions.exceptions import MissingVariable
from configs.logs import logger
from configs.base import VPN_LIST, TEMP_DIR, COMMAND_MIKROTIK


# Загружаем переменные среды
load_dotenv()
envs = {
    'TELEGRAM_TOKEN': os.getenv('TELEGRAM_TOKEN'),
    'TELEGRAM_CHAT_ID': os.getenv('TELEGRAM_CHAT_ID'),
    'ZABBIX_USER': os.getenv('ZABBIX_USER'),
    'ZABBIX_PASSWORD': os.getenv('ZABBIX_PASSWORD'),
    'ZABBIX_SERVER': os.getenv('ZABBIX_SERVER'),
    'MIKROTIK_USER': os.getenv('MIKROTIK_USER'),
    'MIKROTIK_PASSWORD': os.getenv('MIKROTIK_PASSWORD'),
    'MIKROTIK_HOSTNAME': os.getenv('MIKROTIK_HOSTNAME')
}

# Создаем каталог для временных файлов
os.makedirs(TEMP_DIR, exist_ok=True)


def check_tokens() -> None:
    """Проверка переменных оркужения."""
    errors = False

    for key, env in envs.items():
        try:
            if env is None:
                raise MissingVariable(key)
        except MissingVariable:
            errors = True
            logger.critical(f'Отсутствует переменная окружения {key}')

    if errors:
        logger.info('Бот остановлен')
        sys.exit()


def get_api_answer() -> dict:
    """Обращение к API заббикса, для получения количества проблем."""
    zapi = ZabbixAPI(envs['ZABBIX_SERVER'])
    zapi.login(envs['ZABBIX_USER'], envs['ZABBIX_PASSWORD'])
    try:
        response = zapi.trigger.get(only_true=1,
                                    skipDependent=1,
                                    monitored=1,
                                    active=1,
                                    selectHosts=['host', 'name'],
                                    expandDescription=True
                                    )
        logger.debug('Получен ответ от сервара Zabbix.')
    except Exception as error:
        raise Exception(f'Ошибка выполнения HTTP-запроса: {error}')
    return response


def make_report(response, client):
    """Формирует отчет для отправки."""
    triggers = ''
    for num, trigger in enumerate(response, 1):
        trigger_name = trigger.get('description')
        host_name = trigger.get('hosts')[0].get('name')
        triggers += f' {num}. {trigger_name}\n    - {host_name}\n'

    # Отправляем сообщение в Телеграмм
    logger.debug('Сформирован отчет для отправки.')
    return (f'\nОтчет для {client}\n'
            f'<b>Количество проблем: {len(response)}</b>\n'
            '----------------------------\n'
            f'{triggers}'
            '----------------------------')


def daily_report(context):
    """Отправляет отчет по расписанию."""
    response = get_api_answer()
    message = make_report(response, 'Bot')
    try:
        context.bot.send_message(
            chat_id=envs['TELEGRAM_CHAT_ID'],
            text=message,
            parse_mode='HTML')
        logger.debug(f'Бот отправил сообщение {message}')
    except telegram.error.TelegramError as error:
        logger.debug(f'Бот пытался отправить сообщение: {message}')
        logger.error(f'Ошибка отправки сообщения: {error}')


def get_sessions() -> None:
    """Получает активные сессии из микротика."""
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(envs['MIKROTIK_HOSTNAME'],
                           username=envs['MIKROTIK_USER'],
                           password=envs['MIKROTIK_PASSWORD'])
        stdin, stdout, stderr = ssh_client.exec_command(COMMAND_MIKROTIK)
        output = stdout.read().decode('ISO-8859-1')

        # Сохраняем полученный список в файл
        with open(VPN_LIST, 'w', encoding='utf-8') as file:
            file.write(output)
        logger.debug(
            f'Данные с устройства {envs["MIKROTIK_HOSTNAME"]} получены.')
    except Exception as e:
        logger.debug(f'Ошибка получения данных - {e}')
        raise Exception('Ошибка в работе функции get_sessions.')
    finally:
        ssh_client.close()


def make_pretty_text() -> dict:
    """Ищет по ключевым словам login, uptime и ip.

    Формирует из полученных данных словарь.
    """
    pretty_text = {}
    try:
        with open(VPN_LIST, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                name_match = re.search(r'name=([^ ]+)', line)
                uptime_match = re.search(r'uptime=([^ ]+)', line)
                caller_id = re.search(r'caller-id=([^ ]+)', line)
                if name_match and uptime_match and caller_id:
                    pretty_text[name_match.group(1)] = {
                        'uptime': uptime_match.group(1),
                        'ip': caller_id.group(1)}
        logger.debug('Файл успешно обработан.')
    except Exception as e:
        logger.debug(f'Ошибка обработки файла - {e}')
    return pretty_text
